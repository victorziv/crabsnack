from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from config import config
from dbadmin import DBAdmin

mail = Mail()
moment = Moment()
db = DBAdmin()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

# ______________________________________


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    app.logger.info("PROJECT: %r", app.config['PROJECT'])

    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # Setting app context specific configuration
    config[config_name].init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    from .ibox_install import ibox_install as ibox_install_blueprint
    app.register_blueprint(ibox_install_blueprint, url_prefix='/ibox')

    return app
