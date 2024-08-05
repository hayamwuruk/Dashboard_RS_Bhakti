import os

class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Set up the App SECRET_KEY
    SECRET_KEY = os.getenv('SECRET_KEY', 'S#perS3crEt_007')

    # Database setup
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False 

    # Assets Management
    ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')

    # Upload Folder Configuration
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', os.path.join(basedir, 'uploads'))  # Default to a local 'uploads' directory

class ProductionConfig(Config):
    DEBUG = False
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', '/var/www/uploads')  # Override for production

class DebugConfig(Config):
    DEBUG = True
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', os.path.join(Config.basedir, 'uploads_debug'))  # Override for debugging

# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug'     : DebugConfig
}
