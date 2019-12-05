class Config(object):
    DEBUG = False
    ERROR_404_HELP = False
    REDIS_URL = "redis://:@localhost:6379/0"


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
