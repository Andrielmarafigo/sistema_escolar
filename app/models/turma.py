from ..extensions import db

class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    turno = db.Column(db.String(40), nullable=False) 
    ano = db.Column(db.Integer, nullable=False)
