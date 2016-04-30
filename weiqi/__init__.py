from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from . import settings

app = Flask(__name__)
app.config.from_object('weiqi.settings')
app.secret_key = settings.SECRET_KEY

db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO()
login_manager = LoginManager()

from . import views, models, login


def init_app():
    db.init_app(app)
    #db.app = app
    migrate.init_app(app, db)
    socketio.init_app(app)
    login_manager.init_app(app)
