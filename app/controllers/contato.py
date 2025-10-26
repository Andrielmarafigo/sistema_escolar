from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models.contato import Contato

bp = Blueprint("contato", __name__, template_folder="../templates/public")

@bp.route("/contato", methods=["GET"])
def contato():
    return render_template("public/contato.html")

@bp.route("/contato/enviar", methods=["POST"])
def enviar():
    nome = request.form.get("nome")
    email = request.form.get("email")
    mensagem = request.form.get("mensagem")

    # Validação básica
    if not nome or not email or not mensagem:
        flash("Por favor, preencha todos os campos.", "warning")
        return redirect(url_for("contato.contato"))

    # Cria um novo registro no banco
    novo = Contato(nome=nome, email=email, mensagem=mensagem)
    db.session.add(novo)
    db.session.commit()

    flash("✅ Mensagem enviada com sucesso!", "success")
    return redirect(url_for("contato.contato"))
