from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "bhaiyaji_secret_key"


# YOUR PRODUCTS LIST HERE
products = [
    {
        "name": "English Willow Bat",
        "price": "₹8,999",
        "image": "english_bat.jpg",
        "description": "Premium English Willow cricket bat for professional players."
    },
    {
        "name": "Kashmir Willow Bat",
        "price": "₹2,999",
        "image": "kashmir_bat.jpg",
        "description": "Strong Kashmir Willow bat perfect for practice and beginners."
    },
    {
        "name": "Cricket Ball",
        "price": "₹399",
        "image": "ball.jpg",
        "description": "Premium leather cricket ball for matches and practice."
    },
    {
        "name": "Batting Pads",
        "price": "₹2,499",
        "image": "pads.jpg",
        "description": "Lightweight and comfortable batting pads for protection."
    },
    {
        "name": "Batting Gloves",
        "price": "₹1,799",
        "image": "gloves.jpg",
        "description": "High quality batting gloves with better grip and comfort."
    },
    {
        "name": "Thigh Pad",
        "price": "₹699",
        "image": "thigh_pad.jpg",
        "description": "Strong thigh protection for batsmen."
    },
    {
        "name": "Elbow Guard",
        "price": "₹599",
        "image": "elbow_guard.jpg",
        "description": "Lightweight elbow protection for safe batting."
    },
    {
        "name": "Cricket Helmet",
        "price": "₹2,299",
        "image": "helmet.jpg",
        "description": "Strong cricket helmet with comfortable fitting."
    },
    {
        "name": "Wicket Keeping Gloves",
        "price": "₹3,999",
        "image": "keeping_gloves.jpg",
        "description": "Professional wicket keeping gloves for wicket keepers."
    },
    {
        "name": "Cricket Stumps Set",
        "price": "₹999",
        "image": "stumps.jpg",
        "description": "Complete cricket stumps set for matches and practice."
    },
    {
        "name": "Cricket Shoes",
        "price": "₹3,499",
        "image": "shoes.jpg",
        "description": "Comfortable cricket shoes with excellent grip and performance."
    },
    {
        "name": "Cricket Kit Bag",
        "price": "₹2,499",
        "image": "kitbag.jpg",
        "description": "Large cricket kit bag to carry all cricket equipment."
    }
]

def create_table():

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()


create_table()



# Home Page

@app.route("/")
def home():

    search = request.args.get("search", "")

    if search:
        products_list = [
            p for p in products
            if search.lower() in p["name"].lower()
        ]
    else:
        products_list = products


    return render_template(
        "index.html",
        products=products_list,
        user=session.get("username")
    )



# Product Details

@app.route("/product/<int:id>")
def product_detail(id):

    return render_template(
        "detail.html",
        product=products[id]
    )



# Signup

@app.route("/signup", methods=["GET","POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"]

        password = generate_password_hash(
            request.form["password"]
        )


        conn = sqlite3.connect("users.db")
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users(username,password) VALUES(?,?)",
            (username,password)
        )

        conn.commit()
        conn.close()


        return redirect("/login")


    return render_template("signup.html")



# Login

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]


        conn = sqlite3.connect("users.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        )

        user = cur.fetchone()

        conn.close()


        if user and check_password_hash(user[2], password):

            session["username"] = username

            return redirect("/")


    return render_template("login.html")



# Logout

@app.route("/logout")
def logout():

    session.pop("username", None)

    return redirect("/")



if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=4000,
        debug=True
    )