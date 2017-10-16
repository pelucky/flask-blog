#!/usr/bin/env python
# -*- coding=utf-8 -*-

from app import create_app, db
from flask_migrate import Migrate
from flaskext.markdown import Markdown
import os


if os.path.exists('.env'):
    print('Importing environment from .evn...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]


app = create_app(os.getenv('FLASK_CONFIG') or 'DEFAULT')
migrate = Migrate(app, db)
Markdown(app)


if __name__ == "__main__":
    app.run(debug=app.debug)
