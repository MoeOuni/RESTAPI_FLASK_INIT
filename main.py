from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from dotenv import load_dotenv

from db import db

import os
import datetime

from resources.todo import todo
from resources.user import user

# INITIALIZATIONS
app = Flask(__name__)

CORS(app)
# LOAD ENVIRONMENT VARIABLES
load_dotenv()

# CONFIGURATION FOR DATABASE VARIABLES
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(
    days=30)  # should be changed/ default 15min!/ it should be 2h

api = Api(app)

# DATABASE INIT
db.init_app(app)

# JWT SECRET AND INITIALIZATION

app.secret_key = os.getenv("SECRET_KEY")
JWTManager(app)

# ROUTES REGESTRATION
app.register_blueprint(todo)
app.register_blueprint(user)


@app.before_first_request
def create_tables():
    db.create_all()


# LAUNCHIN APP
if __name__ == "__main__":
    app.run(debug=True)
