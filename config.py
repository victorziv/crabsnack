import os
import logging
# ===================================


class Config:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT = 'krabs'
    PROJECT_USER = 'krabs'
    APP = 'crabtest'
    SECRET_KEY = os.environ.get('SECRET_KEY') \
        or 'comment aller a la gare central'
    CRAB_ADMIN = os.environ.get('CRAB_ADMIN') \
        or '%s@nowhere.com' % PROJECT_USER

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    MAIL_SUBJECT_PREFIX = '[%s]' % PROJECT.capitalize()
    MAIL_SENDER = 'Admin %s' % CRAB_ADMIN
    TEST_OWNER_DEFAULT = '%s@nowhere.com' % PROJECT_USER

    DBHOST = 'localhost'
    DBPORT = 5432
    DBUSER = PROJECT_USER
    DBPASSWORD = PROJECT_USER

    DB_CONNECTION_PARAMS = dict(
        dbhost=DBHOST,
        dbport=DBPORT,
        dbuser=DBUSER,
        dbpassword=DBPASSWORD
    )

    DB_URI_FORMAT = 'postgresql://{dbuser}:{dbpassword}@{dbhost}:{dbport}/{dbname}'

    DBNAME_ADMIN = 'postgres'
    DB_CONN_URI_ADMIN = DB_URI_FORMAT.format(
        dbname=DBNAME_ADMIN,
        **DB_CONNECTION_PARAMS
    )

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    DB_TABLES_BASELINE = ['changelog', 'roles', 'users']

    AUTH_TOKEN_EXPIRATION = 3600
    LOGGING_FORMAT = '\t'.join([
        '%(asctime)s',
        '%(levelname)s',
        '%(process)d',
        '%(module)s',
        '%(funcName)s',
        '%(lineno)d'
    ])

    LOGGING_FORMAT += '\t\t%(message)s'

    OAUTH_CREDENTIALS = {
        "facebook": {},
        "twitter": {
            "id": "zwY4WSnGxv9nLz0RZnBsMpQPH",
            "secret": "wiekiIXApl03P47xGSLFezJb6rzTvQdEL4mQJ3Fim7fNJNN344"
        },
        "google": {
            "id": "261888576370-pn751o1qrqbcu662nmr3a24nr9cf3eku.apps.googleusercontent.com",
            "secret": "TDwCUl-WzhOjGw6x_P5bYxtH"
        }
    }

    POSTS_PER_PAGE = 10

    # ___________________________________________

    @staticmethod
    def init_logging(app, logpath, logfile, loglevel):
        log = '%s/%s' % (logpath, logfile)

        if not os.path.exists(logpath):
            os.mkdir(logpath)

        from logging.handlers import RotatingFileHandler
        handler = RotatingFileHandler(log)
        formatter = logging.Formatter(Config.LOGGING_FORMAT)
        handler.setFormatter(formatter)
        handler.setLevel(getattr(logging, loglevel))
        app.logger.setLevel(getattr(logging, loglevel))
        app.logger.addHandler(handler)
        return app
    # ___________________________________________

    @staticmethod
    def init_app(app):
        pass
# ===================================


class DevelopmentConfig(Config):
    DEBUG = True
    DBNAME = "%sdev" % Config.PROJECT
    DB_CONN_URI = Config.DB_URI_FORMAT.format(
        dbname=DBNAME,
        **Config.DB_CONNECTION_PARAMS
    )

    # ________________________________

    @staticmethod
    def init_logging(app):
        logpath = 'logs'
        logfile = '%s.log' % Config.PROJECT
        loglevel = 'DEBUG'
        return Config.init_logging(app, logpath, logfile, loglevel)
    # ________________________________

    @staticmethod
    def init_app(app):
        app = DevelopmentConfig.init_logging(app)
        return app
# ===================================


class TestingConfig(Config):
    TESTING = True
    SERVER_NAME = 'localhost'
    DBNAME = "%stest" % Config.PROJECT
    DB_CONN_URI = Config.DB_URI_FORMAT.format(
        dbname=DBNAME,
        **Config.DB_CONNECTION_PARAMS
    )

    @staticmethod
    def init_app(app):
        pass

# ===================================


class ProductionConfig(Config):

    DBNAME = Config.PROJECT
    SQLALCHEMY_DATABASE_URI = Config.DB_URI_FORMAT.format(
        dbname=DBNAME,
        **Config.DB_CONNECTION_PARAMS
    )
    # _____________________________

    @classmethod
    def init_app(cls, app):

        # email errors to the administrator
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)

        if getattr(cls, 'MAIL_USE_TLS', None):
            secure = ()

        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.IVT_MAIL_SENDER,
            toaddrs=[cls.IVT_ADMIN],
            subject='%s Application Error' % cls.IVT_MAIL_SUBJECT_PREFIX,
            credentials=credentials, secure=secure
        )

        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

# ===================================


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
