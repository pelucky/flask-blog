#!/usr/bin/env python
# -*- coding=utf-8 -*-

from app import create_app, db
from flask_migrate import Migrate
from flaskext.markdown import Markdown
import os


application = create_app(os.getenv('FLASK_CONFIG') or 'DEFAULT')
migrate = Migrate(application, db)
Markdown(application)


if __name__ == "__main__":
    application.run(debug=application.debug)
