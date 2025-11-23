from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from ..extensions import db
from ..models.professor import Professor

bp = Blueprint("professores", __name__, template_folder="../templates/professores")

@bp.route("/")
@login_required
def lista():
    q = request.args.get("q","").strip()
    if q:
        items = Professor.query.filter(Professor.nome.ilike(f"%{q}%")).all()
    else:
        items = Professor.query.order_by(Professor.id.desc()).all()

    return render_template("professores/list.html", professores=items, q=q)


@bp.route("/novo", methods=["GET","POST"])
@login_required
def novo():
    if request.method == "POST":
        nome = request.form.get("nome","").strip()
        email = request.form.get("email","").strip()
        area = request.form.get("area","").strip()

        if not nome or not email or not area:
            flash("Preencha todos os campos.", "warning")
            return redirect(request.url)

        # 🔥 Verifica se já existe professor com este e-mail
        existente = Professor.query.filter_by(email=email).first()
        if existente:
            flash("Já existe um professor com esse e-mail.", "danger")
            return redirect(request.url)

        p = Professor(nome=nome, email=email, area=area)
        db.session.add(p)
        db.session.commit()

        flash("Professor cadastrado!", "success")
        return redirect(url_for("professores.lista"))

    return render_template("professores/form.html", professor=None)


@bp.route("/<int:id>/editar", methods=["GET","POST"])
@login_required
def editar(id):
    p = Professor.query.get_or_404(id)

    if request.method == "POST":
        nome = request.form.get("nome","").strip()
        email = request.form.get("email","").strip()
        area = request.form.get("area","").strip()

        if not nome or not email or not area:
            flash("Preencha todos os campos.", "warning")
            return redirect(request.url)

        # 🔥 Verifica email duplicado com exceção do próprio professor
        existente = Professor.query.filter(Professor.email == email, Professor.id != id).first()
        if existente:
            flash("Este e-mail já está sendo usado por outro professor.", "danger")
            return redirect(request.url)

        p.nome = nome
        p.email = email
        p.area = area

        db.session.commit()

        flash("Professor atualizado!", "success")
        return redirect(url_for("professores.lista"))

    return render_template("professores/form.html", professor=p)


@bp.route("/<int:id>/excluir", methods=["POST"])
@login_required
def excluir(id):
    p = Professor.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()

    flash("Professor removido.", "info")
    return redirect(url_for("professores.lista"))
