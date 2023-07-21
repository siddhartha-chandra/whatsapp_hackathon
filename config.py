from decouple import config


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = config("SECRET_KEY", default="guess-me")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_POOL_RECYCLE = 299


class ProductionConfig(Config):
    DEBUG = False
    DEBUG_TB_ENABLED = False
    username = "siddharthachandr"
    password = "helloSq1"
    hostname = "siddharthachandra.mysql.pythonanywhere-services.com"
    dbname = "siddharthachandr$hackathon"
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{username}:{password}@{hostname}/{dbname}"


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    username = "siddhartha"
    password = "helloSq1"
    hostname = "localhost"
    dbname = "hackathon"
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{username}:{password}@{hostname}/{dbname}"
    
