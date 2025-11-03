from ..extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):  # 🔹 Herda de UserMixin
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(200), nullable=False)

    # 🔹 Campo para recuperação de senha
    reset_token = db.Column(db.String(100), nullable=True)

    def set_password(self, senha):
        """Gera e armazena o hash seguro da senha."""
        self.senha_hash = generate_password_hash(senha)

    def check_password(self, senha):
        """Verifica se a senha informada corresponde ao hash salvo."""
        return check_password_hash(self.senha_hash, senha)

    def __repr__(self):
        return f"<User {self.nome}>"
