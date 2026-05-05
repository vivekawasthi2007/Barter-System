const BASE_URL = "http://127.0.0.1:5000";

/* ================= SAFE FETCH ================= */
async function safeFetch(url, options={}){
    try{
        let res = await fetch(url, options);

        if(!res.ok){
            let text = await res.text();
            console.error("SERVER ERROR:", text);
            throw new Error("Server error");
        }

        return await res.json();

    }catch(err){
        alert("Server not reachable ❌");
        console.error(err);
        throw err;
    }
}

/* ================= OTP ================= */
let generatedOTP = null;

function generateOTP(){
    generatedOTP = Math.floor(1000 + Math.random()*9000);
    alert("Your OTP is: " + generatedOTP);
}

/* ================= REGISTER ================= */
async function register(){
    let emailVal = document.getElementById("email").value;
    let passwordVal = document.getElementById("password").value;
    let contactVal = document.getElementById("contact").value;
    let otpVal = document.getElementById("otp").value;

    if(otpVal != generatedOTP){
        document.getElementById("msg").innerText = "Invalid OTP ❌";
        return;
    }

    await safeFetch(BASE_URL + "/register", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({
            email: emailVal,
            password: passwordVal,
            contact: contactVal
        })
    });

    alert("Registration Successful ✅");
    window.location = "login.html";
}

/* ================= LOGIN ================= */
async function login(){
    try{
        let res = await fetch(BASE_URL+"/login",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({
                email: document.getElementById("email").value,
                password: document.getElementById("password").value
            })
        });
// Line 67 ke baad yeh likhein:
console.log("Requesting URL:", BASE_URL + "/login");
console.log("Response Status:", res.status); 

if (!res.ok) {
    const errorText = await res.text(); // JSON ki jagah text read karein agar error hai
    console.error("Server Error Response:", errorText);
    return;
}

 // Yeh line tabhi chalegi jab status 200 (OK) hoga
        let data = await res.json();   // ✅ FIXED

        console.log("LOGIN RESPONSE:", data);

        // Purana code: if(data.token)
// Naya code (is response ke hisaab se):
if (data.status === "success") {
    // Agar token 'data' field ke andar hai:
    localStorage.setItem("token", data.data.token); 
    window.location = "index.html";
} else {
    alert("Login failed ❌");
}

    }catch(err){
        console.error("LOGIN ERROR:", err);
        alert("Something went wrong ❌");
    }
}

/* ================= ADD ITEM ================= */
async function addItem(){

    let user_id = localStorage.getItem("user_id");
    let titleVal = document.getElementById("title").value;
    let categoryVal = document.getElementById("category").value;
    let priceVal = document.getElementById("price").value;

    if(!titleVal || !categoryVal || !priceVal){
        alert("Fill all fields ❌");
        return;
    }

    let formData = new FormData();
    formData.append("user_id", user_id);
    formData.append("title", titleVal);
    formData.append("category", categoryVal);
    formData.append("price", priceVal);

    let file = document.getElementById("image").files[0];
    if(file){
        formData.append("image", file);
    }

    let res = await fetch(BASE_URL + "/add", {
        method:"POST",
        body:formData
    });

    let text = await res.text();
    console.log("ADD RESPONSE:", text);
    alert("Item Added ✅");
    loadItems();
}
/* ================= DELETE ITEM ================= */
async function deleteItem(id){
    if(!confirm("Delete this item?")) return;

    await fetch(BASE_URL + "/delete_item/" + id, {
        method:"DELETE",
        headers:{
            "Authorization": "Bearer " + localStorage.getItem("token")
        }
    });

    alert("Item deleted 🗑️");
    loadItems();
}

/* ================= WISHLIST ================= */
async function addToWishlist(id){
    await safeFetch(BASE_URL+"/wishlist",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({
            user_id: localStorage.getItem("user_id"),
            item_id: id
        })
    });

    alert("Added to wishlist ❤️");
}

/* ================= CHAT ================= */
async function sendMessage(receiver){
    let msg = prompt("Enter message:");
    if(!msg) return;

    await safeFetch(BASE_URL+"/send_message",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({
            sender: localStorage.getItem("user_id"),
            receiver: receiver,
            message: msg
        })
    });

    alert("Message sent 💬");
}

/* ================= LOAD ITEMS ================= */
async function loadItems() {
    try {
        let res = await fetch(BASE_URL + "/items");
        let data = await res.json();
        
        console.log("ITEMS:", data);
        let html = "";

        // YAHAN CHANGE HAI: data ki jagah data.data use karein
        data.data.forEach(i => {
             let img = i.image 
        ? BASE_URL + "/static/uploads/" + i.image 
        : "https://via.placeholder.com/200";
 // safety check
            // loop ke andar jahan html += `...` likha hai:
html += `
    <div class="card">
        <img src="${img}">
        <div class="content">
            <h3>${i.title}</h3>
            <p>₹${i.price}</p>
            
            <div class="action-buttons">
                <button class="cart-btn" onclick="addToCart(${i.id})">Add to Cart 🛒</button>
                <button class="buy-btn" onclick="buyNow(${i.id}, ${i.price})">Buy Now ⚡</button>
            </div>

            <div class="small-actions">
                <button onclick="addToWishlist(${i.id})">❤️</button>
                <button onclick="sendMessage(${i.user_id})">💬</button>
                <button class="delete-btn" onclick="deleteItem(${i.id})">🗑️</button>
            </div>
        </div>
    </div>`;
        });

        document.getElementById("items").innerHTML = html;

        let emptyEl = document.getElementById("empty");
        if(emptyEl) {
            // YAHAN BHI CHANGE: data.data.length
            emptyEl.innerText = data.data.length === 0 
                ? "No items available 🟡" 
                : "";
        }

    } catch(err) {
        console.error("LOAD ERROR:", err);
        let emptyEl = document.getElementById("empty");
        if(emptyEl) {
            emptyEl.innerText = "Error loading items ❌";
        }
    }
}
function buyNow(id, price) {
    // Basic confirmation
    const confirmPay = confirm(`Proceed to pay ₹${price} for this item?`);
    
    if (confirmPay) {
        // Yahan aap payment gateway ka code daal sakte hain
        // Abhi ke liye hum success alert dikhayenge
        alert("Redirecting to Secure Payment Gateway...");
        
        // Mock success
        setTimeout(() => {
            alert(`Payment of ₹${price} Successful! 🎉 Your order ID is: #ORD${Math.floor(Math.random()*1000)}`);
        }, 2000);
    }
}
function addToCart(id) {
    let cart = JSON.parse(localStorage.getItem("cart") || "[]");
    
    if (cart.includes(id)) {
        alert("Item already in cart! 🛒");
    } else {
        cart.push(id);
        localStorage.setItem("cart", JSON.stringify(cart));
        alert("Item added to cart! 🛒");
        // Aap cart count update karne ka logic bhi yahan daal sakte hain
    }
}
