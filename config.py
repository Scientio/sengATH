class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'mysql://root:Fierlefran7@localhost/survey'

class ProductionConfig(Config):
    SECRET_KEY="98d0s809SD990AS)(dS&A&*d78(*&ASD08A"
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    ENV="development"
    SECRET_KEY="9as8df(*S*8(das0ˆSˆD%5a67900SA(D*00"
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
