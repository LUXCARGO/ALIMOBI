from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DB = "shop.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price INTEGER,
        description TEXT,
        image TEXT
    )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return "Shop API is running"

@app.route("/api/products")
def get_products():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    rows = c.fetchall()
    conn.close()

    products = []
    for r in rows:
        products.append({
            "id": r[0],
            "name": r[1],
            "price": r[2],
            "description": r[3],
            "image": r[4]
        })

    return jsonify(products)

@app.route("/api/add", methods=["POST"])
def add_product():
    data = request.json
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(
        "INSERT INTO products (name, price, description, image) VALUES (?, ?, ?, ?)",
        (data["name"], data["price"], data["description"], data["image"])
    )
    conn.commit()
    conn.close()
    return {"status": "success"}
@app.route("/admin")
def admin_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin Panel</title>
    </head>
    <body>
        <h2>Добавить товар</h2>

        <input id="name" placeholder="Название"><br><br>
        <input id="price" placeholder="Цена"><br><br>
        <input id="image" placeholder="Ссылка на фото"><br><br>
        <textarea id="desc" placeholder="Описание"></textarea><br><br>

        <button onclick="addProduct()">Добавить</button>

        <script>
        function addProduct() {
            fetch("/api/add", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    name: document.getElementById("name").value,
                    price: document.getElementById("price").value,
                    description: document.getElementById("desc").value,
                    image: document.getElementById("image").value
                })
            })
            .then(res => res.json())
            .then(data => alert("Товар добавлен!"));
        }
        </script>
    </body>
    </html>
    """
if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
