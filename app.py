import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

import numpy as np
import pandas as pd
import plotly
import plotly.express as px

from helpers import apology, login_required, admin_required, is_admin, get_class_from_code, get_pset_from_id

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///pguide.db")

# auto reload templates
app.config['TEMPLATES_AUTO_RELOAD'] = True

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
    # check class code
    if not request.args.get("code"):
        return apology("Must provide class code.", 403)

    # get class
    class_ = get_class_from_code(request.args.get("code"))
    if class_ is None:
        return apology("Invalid class code.", 403)

    # get PSET data and overall PSET statistics for selected class
    psets = db.execute("SELECT * FROM psets WHERE class_id = ?", class_["id"])
    stats = db.execute("SELECT * FROM feedback JOIN psets ON feedback.pset_id = psets.id WHERE psets.class_id = ?", class_["id"])

    if len(stats) == 0:
        return render_template("class.html", class_ = class_, psets=psets, analysis=[])

    # convert stats to DataFrame and create new DataFrame for analysis
    df = pd.DataFrame(stats)
    df_analysis = pd.DataFrame()

    # get all the unique pset_ids for the class
    pset_ids = df["pset_id"].unique()
        
    for pset_id in pset_ids:
        # filter stats by each PSET
        df_pset = df[df['pset_id'] == pset_id]

        # add stats to analysis DataFrame
        new_row = pd.Series({'pset_id':pset_id, 'pset_name':df_pset['name'].tolist()[0], 'avg_rating':df_pset['rating'].mean(), 'avg_hours':df_pset['hours_spent'].mean(), 'avg_difficulty':df_pset['difficulty'].mean(), 'avg_enjoyment':df_pset['enjoyment'].mean()})
        df_analysis = pd.concat([df_analysis, new_row.to_frame().T], ignore_index=True)

        print(df_pset.describe())
    
    for property in ["avg_rating", "avg_difficulty", "avg_enjoyment", "avg_hours"]:
        # convert visualization to image
        display_name = property.split('_')[1].capitalize()
        fig = px.bar(df_analysis, x='pset_name', y=property, labels={'pset_name': 'PSET Name', property: f"Average {display_name}"}, title=f'{class_["name"]} PSET Ratings')
        fig.update_layout(title={'text': f'Average {class_["name"]} PSET {display_name}', 'y':0.9, 'x':0.5})
        if property != 'avg_hours':
            fig.update_layout(yaxis=dict(range=[0,10]))

        # save as html
        plotly.offline.plot(fig, filename=f'templates/plots/{class_["code"]}-{property}.html', auto_open=False)

    # convert analysis DataFrame to list of dictionaries
    dict_analysis = df_analysis.to_dict('records')

    return render_template("class.html", class_ = class_, psets=psets, analysis=dict_analysis)


@app.route("/create", methods=["GET", "POST"])
@login_required
@admin_required
def create():
    # return create page
    if request.method == "GET":
        return render_template("create.html")
    
    # get code and name
    code = request.form.get("code")
    name = request.form.get("name")

    if code is None or name is None:
        return apology("Must provide class code and name.", 403)

    # check class
    class_ = get_class_from_code(code)

    if class_ is not None:
        return apology("Class code already exists.", 403)
    
    # insert new class into classes table
    db.execute("INSERT INTO classes (code, name) VALUES (?, ?)", code, name)

    # get class id
    class_id = db.execute("SELECT MAX(id) FROM classes")[0]["MAX(id)"]

    # get pset count
    try:
        psets = int(request.form.get("psets"))
    except:
        return apology("# of PSETs must be a value.", 403)

    # populate pset name and description
    for i in range(psets):
        name = request.form.get(f"name_{i+1}")
        description = request.form.get(f"description_{i+1}")

        if name is None or description is None:
            return apology("Must provide name and description.", 403)
        
        # insert pset into psets table with corresponding class_id
        db.execute("INSERT INTO psets (class_id, name, description) VALUES (?, ?, ?)", class_id, name, description)
    
    return redirect("/")



@app.route("/edit",  methods=["GET", "POST"])
@login_required
@admin_required
def edit():
    if request.method == "GET":
        # get class code
        code = request.args.get("code")
        if not code:
            return apology("Must provide class code.", 403)

        # get class
        class_ = get_class_from_code(code)
        if class_ is None:
            return apology("Invalid class code.", 403)
        
        # get psets for class
        psets = db.execute("SELECT * FROM psets WHERE class_id = ?", class_["id"])

        # return edit page
        return render_template("edit.html", psets=psets, code=code)
    
    # get edit method: "create", "delete", or "update"
    edit_method = request.form.get("method")
    if edit_method is None:
        return apology("Must provide edit method.", 403)

    # get code
    code = request.form.get("code")
    if code is None:
        return apology("Must provide class code.")

    # get class
    class_ = get_class_from_code(code)
    if class_ is None:
        return apology("Invalid class code.", 403)
    
    if edit_method == "create":
        # get name and description
        name = request.form.get("name")
        description = request.form.get("description")
        if name is None or description is None:
            return apology("Must provide name and description.")
        
        # get code
        code = request.form.get("code")
        if code is None:
            return apology("Invalid class code.", 403)

        # get class
        class_ = get_class_from_code(code)
        if class_ is None:
            return apology("Invalid class code.", 403)
        
        # insert new pset into table
        db.execute("INSERT INTO psets (class_id, name, description) VALUES (?, ?, ?)", class_["id"], name, description)
    
    elif edit_method == "delete":
        # get pset id
        id = request.form.get("id")
        if id is None:
            return apology("Must provide PSET id.")
        
        # delete pset
        db.execute("DELETE FROM psets WHERE id = ?", id)
    
    elif edit_method == "update":
        # get updated name and descrption
        name = request.form.get("name")
        description = request.form.get("description")
        if name is None or description is None:
            return apology("Must provide name and description.")

        # get pset id
        id = request.form.get("id")
        if id is None:
            return apology("Must provide PSET id.")
        
        # update pset record in table
        db.execute("UPDATE psets SET name = ?, description = ? WHERE id = ?", name, description, id)
    
    else:
        apology("Invalid edit method.")
    
    # redirect back to edit page with class code
    return redirect(f"/edit?code={code}")

@app.route("/feedback", methods=["GET", "POST"])
@login_required
def feedback():
    if request.method == "GET":
        # get pset id
        id = request.args.get("id")
        if not id:
            return apology("Must provide PSET id.", 403)

        # get pset
        pset = get_pset_from_id(id)
        if pset is None:
            return apology("Invalid PSET id.", 403)
        
        # return feedback page for pset
        return render_template("feedback.html", pset=pset)
        
    if request.method == "POST":
        # get feedback fields
        id = request.form.get("id")
        rating = request.form.get("rating")
        difficulty = request.form.get("difficulty")
        enjoyment = request.form.get("enjoyment")
        hours = request.form.get("hours")
        comments = request.form.get("comments")

        feedback_fields = [id, rating, difficulty, enjoyment, hours, comments]

        if None in feedback_fields:
            return apology("Must provide all necessary fields.", 403)

        # get pset
        pset = get_pset_from_id(id)
        if pset is None:
            return apology("Invalid PSET id.", 403)

        # check to see if there already exists feedback for specific user and pset
        current_feedback = db.execute("SELECT id FROM feedback WHERE user_id = ? AND pset_id = ?", session["user_id"], pset["id"])

        # if current feedback doesn't exist, add new record into feedback table
        if len(current_feedback) == 0:
            db.execute("INSERT INTO feedback (user_id, pset_id, rating, hours_spent, difficulty, enjoyment, comments) VALUES (?, ?, ?, ?, ?, ?, ?)", session["user_id"], id, rating, hours, difficulty, enjoyment, comments)
        # otherwise, update the existing record for user and pset
        else:
            db.execute("UPDATE feedback SET rating = ?, hours_spent = ?, difficulty = ?, enjoyment = ?, comments = ? WHERE user_id = ? AND pset_id = ?", rating, hours, difficulty, enjoyment, comments, session["user_id"], id)

        # get class id and class code
        class_id = pset["class_id"]
        class_code = db.execute("SELECT code FROM classes WHERE id = ?", class_id)[0]["code"]

        # redirect back to class page with class code
        return redirect(f"/class?code={class_code}")
