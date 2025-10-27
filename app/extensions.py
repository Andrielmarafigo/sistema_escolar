from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

# ======= Instâncias Globais ======= #
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()

# ======= Configurações do Flask-Login ======= #
login_manager.login_view = "auth.login"
login_manager.login_message = "Por favor, faça login para acessar esta página."
login_manager.login_message_category = "info"


# ======= Função para inicializar todas as extensões ======= #
def init_extensions(app):
    """Inicializa todas as extensões Flask integradas no projeto."""
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    login_manager.init_app(app)
