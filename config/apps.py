import os


class Base:
    APP_NAME = "api_saya"
    DB_NAME = "zulu"
    REDIS_DB = 1

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSIONS_TIMEOUT = 1440  # for minutes
    SECRET_KEY = '53402c9953aaeb9fb30cf23284f2e919'
    DEBUG_SECRET = 'a6855948ae0826588eb99a03b3dfb8dd'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Base):
    DB_USER = 'root'
    DB_PASS = ''
    DB_HOST = '127.0.0.1'
    DB_PORT = '3307'
    REDIS_URL = "localhost"

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + DB_USER + \
                              ':' + DB_PASS + '@' + DB_HOST + ':' + DB_PORT + '/' + Base.DB_NAME


class ProductionConfig(Base):
    DB_USER = str(os.environ.get("DB_USER"))
    DB_PASS = str(os.environ.get("LIVE_DB_PASSWORD"))
    DB_HOST = str(os.environ.get("LIVE_DB_HOST"))
    DB_PORT = str(os.environ.get("DB_PORT"))
    DB_NAME = str(os.environ.get("DB_NAME", Base.DB_NAME))

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + DB_USER + \
                              ':' + DB_PASS + '@' + DB_HOST + ':' + DB_PORT + '/' + DB_NAME
    REDIS_URL = os.environ.get('REDIS_HOST')


setup = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
