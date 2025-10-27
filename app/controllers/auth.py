from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from flask_mail import Message
from ..extensions import db, mail
from ..models.user import User
import secrets

bp = Blueprint("auth", __name__, template_folder="../templates/auth")

# ===== LOGIN =====
@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "").strip()
        remember = bool(request.form.get("remember"))
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(senha):
            login_user(user, remember=remember)
            return redirect(url_for("public.home"))

        flash("Credenciais inválidas.", "danger")
    return render_template("auth/login.html")


# ===== REGISTRO =====
@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "").strip()

        if not nome or not email or not senha:
            flash("Preencha todos os campos.", "warning")
            return redirect(request.url)

        if User.query.filter_by(email=email).first():
            flash("E-mail já cadastrado.", "warning")
            return redirect(request.url)

        novo_usuario = User(nome=nome, email=email)
        novo_usuario.set_password(senha)
        db.session.add(novo_usuario)
        db.session.commit()

        flash("Cadastro concluído! Faça login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


# ===== LOGOUT =====
@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("public.home"))


# ===== ESQUECEU SENHA (com Flask-Mail) =====
@bp.route("/forgot", methods=["GET", "POST"])
def forgot_password():
    """Página para o usuário solicitar redefinição de senha."""
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("E-mail não encontrado.", "danger")
            return redirect(request.url)

        # Gera um token único e salva
        token = secrets.token_urlsafe(16)
        user.reset_token = token
        db.session.commit()

        # Gera link de redefinição
        reset_link = url_for("auth.reset_password", token=token, _external=True)

        # Monta o e-mail com template HTML
        msg = Message(
            subject="🔐 Redefinição de Senha - Sistema Escolar",
            recipients=[user.email],
            sender=("Sistema Escolar", "seuemail@gmail.com")
        )
        msg.body = f"""
        Olá {user.nome},

        Você solicitou a redefinição da sua senha no Sistema Escolar.
        Para redefinir, clique no link abaixo:

        {reset_link}

        Caso não tenha sido você, ignore este e-mail.
        """
        msg.html = render_template("emails/reset_password.html", user=user, link=reset_link)

        try:
            mail.send(msg)
            flash("Um e-mail com instruções de redefinição foi enviado!", "info")
        except Exception as e:
            print(f"⚠️ Erro ao enviar e-mail: {e}")
            flash("Erro ao enviar o e-mail. Tente novamente mais tarde.", "danger")

        return redirect(request.url)

    return render_template("auth/forgot_password.html")


# ===== REDEFINIR SENHA =====
@bp.route("/reset/<token>", methods=["GET", "POST"])
def reset_password(token):
    """Página para o usuário redefinir a senha com o token."""
    user = User.query.filter_by(reset_token=token).first()

    if not user:
        flash("Token inválido ou expirado.", "danger")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        nova_senha = request.form.get("senha", "").strip()

        if not nova_senha:
            flash("Digite uma nova senha.", "warning")
            return redirect(request.url)

        user.set_password(nova_senha)
        user.reset_token = None
        db.session.commit()

        flash("Senha redefinida com sucesso! Faça login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/reset_password.html")
