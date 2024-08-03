class Config:
    SECRET_KEY = 'mysupersecretkey'

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'mich'
    MYSQL_PASSWORD = 'mich'
    MYSQL_DB = 'db_clinic'
    MYSQL_UNIX_SOCKET = '//opt/lampp/var/mysql/mysql.sock'

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}