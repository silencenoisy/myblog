from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_pagedown import PageDown
from flask_redis import FlaskRedis
from flask_wtf import CSRFProtect



app = Flask(__name__)
app.config.from_object(Config)
app.debug = True
db = SQLAlchemy(app)
rd = FlaskRedis(app,decode_responses=True)
# csrf = CSRFProtect(app)

pagedown = PageDown()
pagedown.init_app(app)

from app.home import home
from app.admin import admin
from app.api import api

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(home)
app.register_blueprint(api,url_prefix='/api')
