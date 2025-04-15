from flask import Flask
from config import *
from flask_migrate import Migrate
from redis import StrictRedis
from models import db
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Configs
app.config["SECRET_KEY"] = RANDOM_SECRET
app.config['FLASK_PYDANTIC_VALIDATION_ERROR_RAISE'] = True
# app.config['JSON_AS_ASCII'] = False
app.config['JWT_SECRET_KEY'] = 'very_secret_config'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=30)


# DB init
app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES_CONN
migrate = Migrate(app, db)
db.init_app(app)

redis_client = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)

jwt = JWTManager(app)
