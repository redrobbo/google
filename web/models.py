#-----------------------------------------------------------------------------------------------------------------------
# Script | models.py
# Author | Jonathan Cox
# Date   | 18 / 3 / 18
#-----------------------------------------------------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------------------------------------------------

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from web import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin

#-----------------------------------------------------------------------------------------------------------------------
# User Class
#-----------------------------------------------------------------------------------------------------------------------

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#-----------------------------------------------------------------------------------------------------------------------

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    img_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.img_file}')" # This may produce error if version is less than 3.6 and IDE's that dont support it

#-----------------------------------------------------------------------------------------------------------------------
# Post Class
#-----------------------------------------------------------------------------------------------------------------------

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_name = db.Column(db.String(30), nullable=False,default='Unnammed')
    animal_type = db.Column(db.String(30), nullable=False)
    animal_gender = db.Column(db.String(30), nullable=False)
    animal_breed = db.Column(db.String(30), nullable=False)
    animal_color = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(30))
    animal_pic = db.Column(db.String(20), nullable=False, default='animal.jpg')
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.animal_name}', '{self.animal_type}', '{self.animal_breed}', '{self.animal_color}', '{self.date}')" # This may produce error if version is less than 3.6 and IDE's that dont support it