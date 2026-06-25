from flask import Flask, render_template, request, redirect, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "blog123"

def init_db():

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS posts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT,
        user_id INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS comments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        comment TEXT,
        post_id INTEGER,
        user_id INTEGER
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():

    conn=sqlite3.connect("database.db")
    cur=conn.cursor()

    cur.execute("SELECT * FROM posts")

    posts=cur.fetchall()

    conn.close()

    return render_template("home.html",posts=posts)

@app.route('/register',methods=['GET','POST'])
def register():

    if request.method=="POST":

        username=request.form['username']
        password=request.form['password']

        conn=sqlite3.connect("database.db")
        cur=conn.cursor()

        try:

            cur.execute(
            "INSERT INTO users(username,password) VALUES(?,?)",
            (username,password)
            )

            conn.commit()

            flash("Registration Successful")

            return redirect('/login')

        except:

            flash("Username Already Exists")

    return render_template("register.html")

@app.route('/login',methods=['GET','POST'])

def login():

    if request.method=="POST":

        username=request.form['username']
        password=request.form['password']

        conn=sqlite3.connect("database.db")
        cur=conn.cursor()

        cur.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username,password)
        )

        user=cur.fetchone()

        if user:

            session["user"]=user[0]

            return redirect('/dashboard')

        flash("Invalid Login")

    return render_template("login.html")

@app.route('/dashboard')

def dashboard():

    if "user" not in session:

        return redirect('/login')

    conn=sqlite3.connect("database.db")
    cur=conn.cursor()

    cur.execute(
    "SELECT * FROM posts WHERE user_id=?",
    (session["user"],)
    )

    posts=cur.fetchall()

    return render_template("dashboard.html",posts=posts)

@app.route('/create',methods=['POST'])

def create():

    title=request.form['title']
    content=request.form['content']

    conn=sqlite3.connect("database.db")
    cur=conn.cursor()

    cur.execute(
    "INSERT INTO posts(title,content,user_id) VALUES(?,?,?)",
    (title,content,session["user"])
    )

    conn.commit()

    return redirect('/dashboard')

@app.route('/logout')

def logout():

    session.clear()

    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)
