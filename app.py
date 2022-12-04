import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

import numpy as np
import pandas as pd
import plotly.express as px

from helpers import apology, login_required, admin_required, is_login, is_admin, get_class_from_code

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///pguide.db")

@app.after_request
def after_request(response):
    """ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    # get classes
    classes = db.execute("SELECT * FROM classes")

    return render_template("index.html", classes=classes, is_admin=is_admin())

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # get inputs
        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')

        # check if inputs are populated
        if "" in [username, password, confirmation]:
            return apology("Username, password, or confirmation missing.")

        # check if username already exists
        if len(db.execute("SELECT * FROM users WHERE username = ?",  username)) != 0:
            return apology("Username already exists.")

        # check if passwords do not match
        if password != confirmation:
            return apology("Passwords do not match.")

        # generate password hash
        hashed_password = generate_password_hash(password)

        # add username and hashed password into db
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashed_password)

        # redirect to homepage
        return redirect("/")

    # return register template
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username.", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password.", 403)

        # Query database for username
        users = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(users) != 1 or not check_password_hash(users[0]["hash"], request.form.get("password")):
            return apology("Invalid username and/or password.", 403)

        # Remember which user has logged in
        session["user_id"] = users[0]["id"]

        # Redirect user to dashboard
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/class")
def class_():
    if not request.args.get("code"):
        return apology("Must provide class code.", 403)

    class_ = get_class_from_code(request.args.get("code"))
    if class_ is None:
        return apology("Invalid class code.", 403)

    # TODO: statistics

    psets = db.execute("SELECT * FROM psets WHERE class_id = ?", class_["id"])

    return render_template("class.html", class_ = class_, psets=psets, is_login=is_login())

@login_required
@admin_required
@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return render_template("create.html")
    
    code = request.form.get("code")
    name = request.form.get("name")

    if code is None or name is None:
        return apology("Must provide class code and name.", 403)

    class_ = get_class_from_code(code)

    if class_ is not None:
        return apology("Class code already exists.", 403)
    
    db.execute("INSERT INTO classes (code, name) VALUES (?, ?)", code, name)

    class_id = db.execute("SELECT MAX(id) FROM classes")[0]["MAX(id)"]

    psets = int(request.form.get("psets"))
    
    for i in range(psets):
        name = request.form.get(f"name_{i+1}")
        description = request.form.get(f"description_{i+1}")

        if name is None or description is None:
            return apology("Must provide name and description.", 403)
        
        db.execute("INSERT INTO psets (class_id, name, description) VALUES (?, ?, ?)", class_id, name, description)
    
    return redirect("/")



@login_required
@admin_required
@app.route("/edit",  methods=["GET", "POST"])
def edit():
    if request.method == "GET":
        code = request.args.get("code")
        if not code:
            return apology("Must provide class code.", 403)

        class_ = get_class_from_code(code)
        if class_ is None:
            return apology("Invalid class code.", 403)

        psets = db.execute("SELECT * FROM psets WHERE class_id = ?", class_["id"])

        return render_template("edit.html", psets=psets, code=code)
    
    
    edit_method = request.form.get("method")
    if edit_method is None:
        return apology("Must provide edit method.", 403)

    code = request.form.get("code")
    if code is None:
        return apology("Must provide class code.")

    class_ = get_class_from_code(code)
    if class_ is None:
        return apology("Invalid class code.", 403)
    
    if edit_method == "create":
        name = request.form.get("name")
        description = request.form.get("description")
        if name is None or description is None:
            return apology("Must provide name and description.")
        
        code = request.form.get("code")
        if code is None:
            return apology("Invalid class code.", 403)

        class_ = get_class_from_code(code)
        if class_ is None:
            return apology("Invalid class code.", 403)
        

        db.execute("INSERT INTO psets (class_id, name, description) VALUES (?, ?, ?)", class_["id"], name, description)
    
    elif edit_method == "delete":
        id = request.form.get("id")
        if id is None:
            return apology("Must provide PSET id.")
        
        db.execute("DELETE FROM psets WHERE id = ?", id)
    
    elif edit_method == "update":
        name = request.form.get("name")
        description = request.form.get("description")
        if name is None or description is None:
            return apology("Must provide name and description.")

        id = request.form.get("id")
        if id is None:
            return apology("Must provide PSET id.")
        
        db.execute("UPDATE psets SET name = ?, description = ? WHERE id = ?", name, description, id)
    
    else:
        apology("Invalid ")
    return redirect(f"/edit?code={code}")

@login_required
@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "GET":
        id = request.args.get("id")
        if not id:
            return apology("Must provide PSET id.", 403)

        psets = db.execute("SELECT * FROM psets WHERE id = ?", id)

        if len(psets) == 0:
            return apology("Invalid PSET id.", 403)
        
        pset = psets[0]

        return render_template("feedback.html", pset=pset)
    
    # TODO: get form input
    # TODO: add feedback to database (make sure to overwrite existing feedback if a user resubmits for same PSET)
        rating = request.form.get("rating")
        difficulty = request.form.get("difficulty")
        enjoyment = request.form.get("enjoyment")
        hours = request.form.get("hours")
        comments = request.form.get("comments")

        if rating is None or difficulty is None or enjoyment is None or hours is None or comments is None:
            return apology("Must complete all fields.", 403)