from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from config import Config
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
jwt = JWTManager(app)
bcrypt = Bcrypt()

from routes import api_v1

app.register_blueprint(api_v1, url_prefix='/api/v1')

