from flask import Blueprint, jsonify, request
from ..models.aluno import Aluno
from ..models.turma import Turma

bp = Blueprint("api", __name__)

@bp.get("/alunos")
def api_alunos():
    alunos = Aluno.query.all()
    return jsonify([{"id":a.id,"nome":a.nome,"email":a.email,"matricula":a.matricula} for a in alunos])

@bp.get("/turmas")
def api_turmas():
    turmas = Turma.query.all()
    return jsonify([{"id":t.id,"nome":t.nome,"turno":t.turno,"ano":t.ano} for t in turmas])
