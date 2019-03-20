#-----------------------------------------------------------------------------------------------------------------------
# Script | init.py
# Author | Jonathan Cox
# Date   | 18 / 3 / 18
#-----------------------------------------------------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------------------------------------------------

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

#-----------------------------------------------------------------------------------------------------------------------
# Main
#-----------------------------------------------------------------------------------------------------------------------

app = Flask(__name__)
app.config['SECRET_KEY'] = '3L?vW+kaBk7jsydCnRXM%ut?dKu?Tv$DwZvG&bBFsm=97zF3Rf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

#-----------------------------------------------------------------------------------------------------------------------
# Mail
#-----------------------------------------------------------------------------------------------------------------------

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'PetsMail001@gmail.com'
app.config['MAIL_PASSWORD'] = 'MailPets!001'
mail = Mail(app)

from web import routes