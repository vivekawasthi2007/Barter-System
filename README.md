# 🚀 BarterX — Peer-to-Peer Barter & Exchange Marketplace

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flask Version](https://img.shields.io/badge/Flask-2.x%20%7C%203.x-black?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Database](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Frontend](https://img.shields.io/badge/Frontend-HTML5%20%7C%20CSS3%20%7C%20JS-E34F26?logo=html5&logoColor=white)](https://developer.mozilla.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **"Exchange items without money 💱"**  
> **BarterX** is a modern, responsive, full-stack peer-to-peer barter marketplace web application built with **Python**, **Flask**, and **JavaScript**. It enables users to trade, swap, and exchange pre-owned goods directly without using traditional cash currency.

---

## ✨ Features

### 💱 Cashless Barter Trading
- **Browse & Buy/Swap Goods:** Explore a wide array of goods listed across multiple categories (Electronics, Fashion, Sports, Home, Lifestyle, etc.).
- **Sell / Post Items for Trade:** List items with title, category, estimated valuation, and photo upload.
- **Client-Side Live Search:** Instantly filter listed items in real-time as you type without reloading the page.

### 💬 In-App Trade Chat & Messaging
- **Direct Negotiation:** Send and receive direct messages between users to propose trade deals and negotiate swaps.
- **Message History:** View incoming trade proposals per user (`/messages/<user_id>`).

### ❤️ Wishlist System
- **Save Favorites:** Bookmark interesting items to a personal wishlist.
- **Wishlist Dashboard:** View all saved items in one convenient place to plan your future trades.

### 🔐 Authentication & Security
- **OTP Verification Flow:** Sign up with mock OTP generation and verification for account validation.
- **Password Hashing:** Passwords securely hashed and verified with `werkzeug.security` (`generate_password_hash`, `check_password_hash`).
- **Session & Token Management:** LocalStorage-based auth state and JWT-ready endpoints.

### 🎨 Modern Glassmorphic UI
- **Glassmorphism Design:** Gradient backgrounds, frosted glass cards (`backdrop-filter: blur(10px)`), and smooth micro-animations.
- **Dark & Light Mode:** One-click instant theme toggle for comfortable viewing day or night.
- **Responsive Layout:** Grid layout adapting seamlessly across mobile, tablet, and desktop screens.

### 👤 User Profile & Inventory Management
- **Profile Dashboard:** Update contact details and manage account preferences.
- **Personal Inventory:** Review all products you have listed, with one-click deletion of traded or inactive items.

### ⚡ Built-In Database Seeder
- Includes a `/seed_items` endpoint to pre-populate 10 realistic sample products (iPhone 13, Gaming Mouse, Running Shoes, etc.) for instant testing.

---

## 🛠️ Tech Stack

| Layer | Technology | Details |
|---|---|---|
| **Backend** | Python 3.10+, Flask | RESTful API endpoints & template rendering |
| **Database** | SQLite (`barter_market.db` / `barterx.db`) | Lightweight relational storage |
| **Security & Auth** | Werkzeug Security, Flask-JWT-Extended | Secure password hashing & token authentication |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript | Responsive grid, Glassmorphism, Dark Mode, Async Fetch API |
| **CORS** | Flask-CORS | Cross-origin resource sharing support |

---

## 📂 Project Structure

```text
Barter-System/
├── python/
│   ├── app.py                   # Main Flask application & API routes
│   ├── barter_market.db         # SQLite database file
│   ├── requirements.txt         # Project dependencies
│   ├── barterx/                 # Modular Blueprint architecture (Advanced)
│   │   ├── app/
│   │   │   ├── __init__.py      # App factory & extension initialization
│   │   │   ├── models.py        # SQLAlchemy models (User, Item, Wishlist, Message)
│   │   │   ├── utils.py
│   │   │   └── routes/          # Modular blueprints (auth, items, users, chat, wishlist)
│   │   ├── config.py            # App configurations
│   │   ├── requirements.txt
│   │   └── run.py               # Blueprint runner
│   ├── static/                  # Static assets
│   │   ├── script.js            # Client-side API integration & DOM logic
│   │   ├── style.css            # Stylesheets
│   │   └── uploads/             # Uploaded product images
│   └── templates/               # Frontend HTML pages
│       ├── home.html            # Landing page
│       ├── index.html           # Main marketplace (Buy, Sell, Search, Dark Mode)
│       ├── login.html           # User login page
│       ├── register.html        # User registration with OTP
│       └── profile.html         # User profile & inventory
├── .gitignore
├── LICENSE                      # MIT License
├── requirements.txt             # Root requirements
└── README.md                    # Project Documentation
```

---

## 🚀 Getting Started

Follow these steps to run BarterX locally on your machine:

### 1. Clone the Repository
```bash
git clone https://github.com/vivekawasthi2007/Barter-System.git
cd Barter-System/python
```

### 2. Create & Activate Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```
*(Or install manually):*
```bash
pip install Flask Flask-Cors Flask-SQLAlchemy Flask-JWT-Extended Werkzeug
```

### 4. Run the Application

Start the Flask development server:
```bash
python app.py
```

The application will start at: **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

---

## 🗺️ Key Application Routes

### Frontend Pages
| Route | Description |
|---|---|
| `/` | Landing page (`home.html`) |
| `/index.html` | Main marketplace dashboard (Buy & Sell goods, Search) |
| `/login.html` | User login portal |
| `/register.html` | User sign-up page with OTP verification |
| `/profile.html` | User profile, inventory management & personal items |

### API Endpoints
| Endpoint | Method | Description |
|---|---|---|
| `/register` | `POST` | Register a new user with hashed password |
| `/login` | `POST` | Authenticate user credentials & return session ID |
| `/users` | `GET` | List registered users |
| `/update_user` | `POST` | Update user contact information |
| `/items` | `GET` | Fetch all available barter items |
| `/add` | `POST` | List a new item with image upload |
| `/my_items/<user_id>` | `GET` | Retrieve items listed by a specific user |
| `/delete_item/<id>` | `DELETE` | Remove a listed item |
| `/seed_items` | `GET / POST`| Pre-populate 10 sample marketplace items |
| `/wishlist` | `POST` | Add item to user wishlist |
| `/wishlist/<user_id>` | `GET` | Retrieve all items on a user's wishlist |
| `/send_message` | `POST` | Send trade negotiation message |
| `/messages/<user_id>` | `GET` | Get received messages for trade coordination |

---

## 🛡️ Database Schema Overview

The SQLite database (`barter_market.db`) contains four core tables:

- **`users`**: `id`, `email`, `password` (hashed), `contact`
- **`items`**: `id`, `user_id`, `title`, `category`, `price`, `image`, `created_at`
- **`wishlist`**: `id`, `user_id`, `item_id`
- **`messages`**: `id`, `sender_id`, `receiver_id`, `message`

---

## 🤝 Contributing

Contributions, feature suggestions, and pull requests are welcome!
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/NewFeature`)
3. Commit your Changes (`git commit -m 'Add some NewFeature'`)
4. Push to the Branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

---

## 📜 License

Distributed under the **MIT License**. See the [`LICENSE`](LICENSE) file for more details.

---

### 👨‍💻 Author
Developed with ❤️ by **[Vivek Awasthi](https://github.com/vivekawasthi2007)**.
