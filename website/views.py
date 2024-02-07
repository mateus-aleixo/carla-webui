from flask import Blueprint, render_template, redirect, url_for

views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("home.html")


@views.route("/test", methods=["POST"])
def test():
    from subprocess import run

    run(["python", "test.py"], cwd=".\\src")

    return redirect(url_for("views.home"))
