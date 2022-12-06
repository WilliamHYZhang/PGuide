from cs50 import SQL

from flask import redirect, render_template, request, session
from functools import wraps

db = SQL("sqlite:///pguide.db")

def apology(message, code=400):
    """Render message as an apology to user."""
    return render_template("apology.html", top=code, bottom=message), code


def login_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print('called')
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def is_login():
    # return if user is logged in
    return session.get("user_id") is not None

def admin_required(f):
    """
    Decorate routes to require admin.
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get("user_id")
        if user_id is None:
            return redirect("/login")
        
        user = db.execute("SELECT * FROM users WHERE id = ?", user_id)[0]
        if not user["is_admin"]:
            return apology("Must be admin.", 403)

        return f(*args, **kwargs)
    return decorated_function

def is_admin():
    # return if user is admin
    user_id = session.get("user_id")
    if user_id is None:
        return False

    user = db.execute("SELECT * FROM users WHERE id = ?", user_id)[0]

    return user["is_admin"]

def get_class_from_code(code):
    # get class from code
    classes = db.execute("SELECT * FROM classes WHERE code = ?", code)
    return classes[0] if len(classes) == 1 else None

def get_pset_from_id(id):
    # get pset from id
    psets = db.execute("SELECT * FROM psets WHERE id = ?", id)
    return psets[0] if len(psets) == 1 else None
