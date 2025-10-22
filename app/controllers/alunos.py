import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_from_directory
from flask_login import login_required
from ..extensions import db
from ..models.aluno import Aluno

bp = Blueprint("alunos", __name__, template_folder="../templates/alunos")

@bp.route("/")
@login_required
def lista():
    q = request.args.get("q","").strip()
    if q:
        alunos = Aluno.query.filter(Aluno.nome.ilike(f"%{q}%")).all()
    else:
        alunos = Aluno.query.order_by(Aluno.id.desc()).all()
    return render_template("alunos/list.html", alunos=alunos, q=q)

@bp.route("/novo", methods=["GET","POST"])
@login_required
def novo():
    if request.method == "POST":
        nome = request.form.get("nome","").strip()
        email = request.form.get("email","").strip()
        matricula = request.form.get("matricula","").strip()
        if not nome or not email or not matricula:
            flash("Preencha todos os campos obrigatórios.", "warning"); return redirect(request.url)
        if Aluno.query.filter((Aluno.email==email)|(Aluno.matricula==matricula)).first():
            flash("E-mail ou matrícula já cadastrados.", "warning"); return redirect(request.url)
        a = Aluno(nome=nome, email=email, matricula=matricula)

        # upload opcional
        f = request.files.get("documento")
        if f and f.filename:
            filename = f"{matricula}_{f.filename}".replace(" ","_")
            path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            f.save(path)
            a.documento = filename

        db.session.add(a); db.session.commit()
        flash("Aluno cadastrado!", "success")
        return redirect(url_for("alunos.lista"))
    return render_template("alunos/form.html", aluno=None)

@bp.route("/<int:id>/editar", methods=["GET","POST"])
@login_required
def editar(id):
    a = Aluno.query.get_or_404(id)
    if request.method == "POST":
        nome = request.form.get("nome","").strip()
        email = request.form.get("email","").strip()
        matricula = request.form.get("matricula","").strip()
        if not nome or not email or not matricula:
            flash("Preencha todos os campos obrigatórios.", "warning"); return redirect(request.url)
        a.nome, a.email, a.matricula = nome, email, matricula

        f = request.files.get("documento")
        if f and f.filename:
            filename = f"{matricula}_{f.filename}".replace(" ","_")
            path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            f.save(path)
            a.documento = filename

        db.session.commit()
        flash("Aluno atualizado!", "success")
        return redirect(url_for("alunos.lista"))
    return render_template("alunos/form.html", aluno=a)

@bp.route("/<int:id>/excluir", methods=["POST"])
@login_required
def excluir(id):
    a = Aluno.query.get_or_404(id)
    db.session.delete(a); db.session.commit()
    flash("Aluno removido.", "info")
    return redirect(url_for("alunos.lista"))

@bp.route("/download/<nome_arquivo>")
@login_required
def download(nome_arquivo):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], nome_arquivo, as_attachment=True)
