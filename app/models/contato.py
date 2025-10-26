from app.extensions import db

class Contato(db.Model):
    __tablename__ = "contato"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    data_envio = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"<Contato {self.nome}>"
