from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/book'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Contact(db.Model):
    __tablename__ = 't_user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=True)
    password = db.Column(db.String(30), nullable=True)
    password2 = db.Column(db.String(30), nullable=True)

    def __repr__(self):
        return '<Contacts %r>' % self.name

class User():
    id = 1
    username = 'admin'
    password = 'na'
    is_active = True
    is_authenticated = True

    def get_id(id):
        return 1

class Company():
    name = ''
    city = ''
    date = ''

class Trans():
    name = ''
    date = ''
    number = ''
    price = ''

class Inquery():
    name = ''
    date = ''
    subject = ''

