from flask import Flask, flash, redirect, render_template, request, session

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("admin.html")

