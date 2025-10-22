from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from ..extensions import db
from ..models.turma import Turma

bp = Blueprint("turmas", __name__, template_folder="../templates/turmas")

@bp.route("/")
@login_required
def lista():
    q = request.args.get("q","").strip()
    if q:
        items = Turma.query.filter(Turma.nome.ilike(f"%{q}%")).all()
    else:
        items = Turma.query.order_by(Turma.id.desc()).all()
    return render_template("turmas/list.html", turmas=items, q=q)

@bp.route("/nova", methods=["GET","POST"])
@login_required
def nova():
    if request.method == "POST":
        nome = request.form.get("nome","").strip()
        turno = request.form.get("turno","").strip()
        ano = request.form.get("ano","").strip()
        if not nome or not turno or not ano:
            flash("Preencha todos os campos.", "warning"); return redirect(request.url)
        try:
            ano_i = int(ano)
        except:
            flash("Ano inválido.", "warning"); return redirect(request.url)

        t = Turma(nome=nome, turno=turno, ano=ano_i)
        db.session.add(t); db.session.commit()
        flash("Turma criada!", "success")
        return redirect(url_for("turmas.lista"))
    return render_template("turmas/form.html", turma=None)

@bp.route("/<int:id>/editar", methods=["GET","POST"])
@login_required
def editar(id):
    t = Turma.query.get_or_404(id)
    if request.method == "POST":
        nome = request.form.get("nome","").strip()
        turno = request.form.get("turno","").strip()
        ano = request.form.get("ano","").strip()
        if not nome or not turno or not ano:
            flash("Preencha todos os campos.", "warning"); return redirect(request.url)
        try:
            t.ano = int(ano)
        except:
            flash("Ano inválido.", "warning"); return redirect(request.url)
        t.nome, t.turno = nome, turno
        db.session.commit()
        flash("Turma atualizada!", "success")
        return redirect(url_for("turmas.lista"))
    return render_template("turmas/form.html", turma=t)

@bp.route("/<int:id>/excluir", methods=["POST"])
@login_required
def excluir(id):
    t = Turma.query.get_or_404(id)
    db.session.delete(t); db.session.commit()
    flash("Turma removida.", "info")
    return redirect(url_for("turmas.lista"))
