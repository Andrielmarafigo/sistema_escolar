from flask import Blueprint, render_template

bp = Blueprint("public", __name__)

@bp.route("/")
def home():
    return render_template("public/home.html")

@bp.route("/sobre")
def sobre():
    return render_template("public/sobre.html")

@bp.route("/contato")
def contato():
    return render_template("public/contato.html")
