import os
from flask import Flask
from .extensions import db, migrate, login_manager, mail
from .config import DevConfig
from .models.user import User


def create_app(config_object=DevConfig):
    """Cria e configura a aplicação Flask."""
    app = Flask(__name__, static_folder="static")
    app.config.from_object(config_object)

    # Garante que a pasta de uploads exista
    os.makedirs(app.config.get("UPLOAD_FOLDER", "app/static/uploads"), exist_ok=True)

    # Configuração do Flask-Mail (📧 ajuste com seu e-mail real)
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = "andrielmarafigo1403@gmail.com"
    app.config["MAIL_PASSWORD"] = "povc ydkf xyjp pcbk"
    app.config["MAIL_DEFAULT_SENDER"] = ("Sistema Escolar", "andrielmarafigo1403@gmail.com")

    # Inicializa extensões
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    # Configuração de login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Por favor, faça login para acessar esta página."
    login_manager.login_message_category = "info"

    # Importa e registra os blueprints
    from .controllers.public import bp as public_bp
    from .controllers.auth import bp as auth_bp
    from .controllers.alunos import bp as alunos_bp
    from .controllers.professores import bp as professores_bp
    from .controllers.turmas import bp as turmas_bp
    from .controllers.api import bp as api_bp
    from .controllers.contato import bp as contato_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(alunos_bp, url_prefix="/alunos")
    app.register_blueprint(professores_bp, url_prefix="/professores")
    app.register_blueprint(turmas_bp, url_prefix="/turmas")
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(contato_bp)

    return app
