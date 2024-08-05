# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from flask_migrate import Migrate
from flask_minify import Minify
from sys import exit

from apps.config import config_dict
from apps import create_app, db

# Determine if running in DEBUG mode
DEBUG = (os.getenv('DEBUG', 'False') == 'True')

# Select configuration mode
get_config_mode = 'Debug' if DEBUG else 'Production'

try:
    app_config = config_dict[get_config_mode.capitalize()]
except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production]')

app = create_app(app_config)
Migrate(app, db)

# Minify HTML in production
if not DEBUG:
    Minify(app=app, html=True, js=False, cssless=False)

# Log configuration details
if DEBUG:
    app.logger.info('DEBUG            = ' + str(DEBUG))
    app.logger.info('FLASK_ENV        = ' + os.getenv('FLASK_ENV'))
    app.logger.info('Page Compression = ' + ('FALSE' if DEBUG else 'TRUE'))
    app.logger.info('DBMS             = ' + app_config.SQLALCHEMY_DATABASE_URI)
    app.logger.info('ASSETS_ROOT      = ' + app_config.ASSETS_ROOT)

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

if __name__ == "__main__":
    app.run()
