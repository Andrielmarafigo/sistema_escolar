import os
from flask import Flask
from .extensions import db, migrate, login_manager
from .config import DevConfig
from .models.user import User

def create_app(config_object=DevConfig):
    app = Flask(__name__, static_folder="static")
    app.config.from_object(config_object)

    # Ensure upload folder exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # register blueprints
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
