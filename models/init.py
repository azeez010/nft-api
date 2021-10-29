from flask_sqlalchemy import SQLAlchemy

from flask import Flask

# template_url = os.path.join(os.path.abspath("."), "templates")
# static_url = static_folder=os.path.join(os.path.abspath("."), "static")

app = Flask(__name__)

import pymysql

pymysql.install_as_MySQLdb()

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://turkeyapp:azeez007@turkeyapp.mysql.pythonanywhere-services.com/turkeyapp$turkeyapp'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://azeez:azeez007@localhost/nft'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SECRET_KEY'] = "d27e0926-13d9-11eb-900d-18f46ae7891e"
app.config['SQLALCHEMY_POOL_RECYCLE'] = 280
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20
app.config['TOKEN_EXPIRY_TIME'] = "10"

# mail config
db = SQLAlchemy(app)
