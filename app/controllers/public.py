from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

bp = Blueprint("public", __name__)

@bp.route("/")
def home():
    
    if current_user.is_authenticated:
        return redirect(url_for("alunos.lista"))
    return render_template("public/home.html")


@bp.route("/sobre")
def sobre():
    return render_template("public/sobre.html")
    
@bp.route("/contato")
def contato():
    return render_template("public/contato.html")
