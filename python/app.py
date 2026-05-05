from flask import Flask, request, jsonify, render_template
import sqlite3
import os
from werkzeug.utils import secure_filename
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

# ================= CONFIG =================
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ================= DATABASE =================
db = sqlite3.connect("barter_market.db", check_same_thread=False)
db.row_factory = sqlite3.Row
cursor = db.cursor()

# ================= TABLES =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    password TEXT,
    contact TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS items(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT,
    category TEXT,
    price INTEGER,
    image TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS wishlist(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    item_id INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS messages(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER,
    receiver_id INTEGER,
    message TEXT
)
""")

db.commit()

# ================= HELPERS =================
def success(data):
    return jsonify({"status": "success", "data": data})

def error(msg):
    return jsonify({"status": "error", "message": msg})

# ================= AUTH =================

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    contact = data.get('contact', '')


    hashed = generate_password_hash(data['password'])

    cursor.execute("""
    INSERT INTO users (email, password, contact)
    VALUES (?,?,?)
    """, (data['email'], hashed, data['contact']))

    db.commit()

    return success("Registered")

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        cursor.execute("SELECT * FROM users WHERE email=?", (data['email'],))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], data['password']):
            return jsonify({
                "status": "success",
                "data": {"user_id": user['id']}
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Invalid credentials"
            })

    except Exception as e:
        print("LOGIN ERROR:", e)   # 🔥 THIS WILL SHOW REAL ERROR
        return jsonify({
            "status": "error",
            "message": "Server error"
        }), 500
# ================= USERS =================

@app.route('/users', methods=['GET'])
def get_users():
    cursor.execute("SELECT id,email,contact FROM users")
    rows = cursor.fetchall()
    return success([dict(row) for row in rows])

@app.route('/update_user', methods=['POST'])
def update_user():
    data = request.json
    cursor.execute("UPDATE users SET contact=? WHERE id=?",
                   (data['contact'], data['id']))
    db.commit()
    return success("Updated")

# ================= ITEMS =================

@app.route('/add', methods=['POST'])
def add_item():
    try:
        user_id = request.form['user_id']
        title = request.form['title']
        category = request.form['category']
        price = request.form['price']

        filename = None

        if 'image' in request.files:
            file = request.files['image']
            if file.filename != "":
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        cursor.execute("""
        INSERT INTO items (user_id, title, category, price, image)
        VALUES (?,?,?,?,?)
        """, (user_id, title, category, price, filename))

        db.commit()
        print("Item received:", title, category, price)
        print("DATA:", user_id, title, category, price)
        return success("Item added")

    except Exception as e:
        return error(str(e))
    
    
@app.route('/seed_items', methods=['GET', 'POST'])
def seed_items():
    try:
        sample_data = [
            (1, "iPhone 13", "Electronics", 45000, "default.png"),
            (1, "Gaming Mouse", "Electronics", 1500, "default.png"),
            (1, "Cotton T-Shirt", "Fashion", 500, "default.png"),
            (1, "Running Shoes", "Sports", 2500, "default.png"),
            (1, "Study Lamp", "Home", 800, "default.png"),
            (1, "Keyboard", "Electronics", 1200, "default.png"),
            (1, "Leather Wallet", "Accessories", 600, "default.png"),
            (1, "Water Bottle", "Lifestyle", 300, "default.png"),
            (1, "Backpack", "Travel", 1800, "default.png"),
            (1, "Sun Glasses", "Fashion", 900, "default.png")
        ]

        for user_id, title, category, price, image in sample_data:
            cursor.execute(
                "INSERT INTO items (user_id, title, category, price, image) VALUES (?, ?, ?, ?, ?)",
                (user_id, title, category, price, image)
            )
        
        db.commit()
        return "10 Items added successfully! Refresh your page."
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/items', methods=['GET'])
def get_items():
    cursor.execute("SELECT * FROM items")
    rows = cursor.fetchall()
    return success([dict(row) for row in rows])

@app.route('/my_items/<int:user_id>')
def my_items(user_id):
    cursor.execute("SELECT * FROM items WHERE user_id=?", (user_id,))
    rows = cursor.fetchall()
    return success([dict(row) for row in rows])

@app.route('/delete_item/<int:id>', methods=['DELETE'])
def delete_item(id):
    cursor.execute("DELETE FROM items WHERE id=?", (id,))
    db.commit()
    return success("Deleted")

# ================= WISHLIST =================

@app.route('/wishlist', methods=['POST'])
def add_wishlist():
    data = request.json
    cursor.execute("INSERT INTO wishlist (user_id, item_id) VALUES (?,?)",
                   (data['user_id'], data['item_id']))
    db.commit()
    return success("Added to wishlist")

@app.route('/wishlist/<int:user_id>')
def get_wishlist(user_id):
    cursor.execute("""
    SELECT items.* FROM wishlist 
    JOIN items ON items.id = wishlist.item_id
    WHERE wishlist.user_id=?
    """, (user_id,))
    rows = cursor.fetchall()
    return success([dict(row) for row in rows])

# ================= CHAT =================

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    cursor.execute("""
    INSERT INTO messages (sender_id, receiver_id, message)
    VALUES (?,?,?)
    """, (data['sender'], data['receiver'], data['message']))
    db.commit()
    return success("Message sent")

@app.route('/messages/<int:user_id>')
def get_messages(user_id):
    cursor.execute("SELECT * FROM messages WHERE receiver_id=?", (user_id,))
    rows = cursor.fetchall()
    return success([dict(row) for row in rows])

# ================= ROUTES =================

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login.html')
def login_page():
    return render_template("login.html")

@app.route('/register.html')
def register_page():
    return render_template("register.html")

@app.route('/index.html')
def index():
    return render_template("index.html")

@app.route('/profile.html')
def profile():
    return render_template("profile.html")

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)