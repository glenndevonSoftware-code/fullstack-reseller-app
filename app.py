from flask import Flask, render_template, request, redirect, url_for 
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("inventory.db")
 
    conn.execute("""
         CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            purchase_price REAL NOT NULL,
            listing_price REAL NOT NULL
        )
    """)

    conn.close()


@app.route("/")
def home():
    conn = sqlite3.connect("inventory.db")
    conn.row_factory = sqlite3.Row

    items = conn.execute(
        "SELECT * FROM inventory ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template("index.html", items=items)

@app.route("/add-item", methods=["POST"])
def add_item():
    item_name = request.form["item_name"]
    purchase_price = float(request.form["purchase_price"])
    listing_price = float(request.form["listing_price"])

    conn = sqlite3.connect("inventory.db")

    conn.execute(
        """
        INSERT INTO inventory (item_name, purchase_price, listing_price)
        VALUES (?, ?, ?)
        """,
        (item_name, purchase_price, listing_price)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("home"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)