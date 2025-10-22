from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from ..extensions import db
from ..models.user import User

bp = Blueprint("auth", __name__, template_folder="../templates/auth")

@bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email","").strip()
        senha = request.form.get("senha","").strip()
        remember = bool(request.form.get("remember"))
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(senha):
            login_user(user, remember=remember)
            return redirect(url_for("public.home"))
        flash("Credenciais inválidas.", "danger")
    return render_template("auth/login.html")

@bp.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        nome = request.form.get("nome","").strip()
        email = request.form.get("email","").strip()
        senha = request.form.get("senha","").strip()
        if not nome or not email or not senha:
            flash("Preencha todos os campos.", "warning"); return redirect(request.url)
        if User.query.filter_by(email=email).first():
            flash("E-mail já cadastrado.", "warning"); return redirect(request.url)
        u = User(nome=nome, email=email); u.set_password(senha)
        db.session.add(u); db.session.commit()
        flash("Cadastro concluído! Faça login.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html")

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("public.home"))
