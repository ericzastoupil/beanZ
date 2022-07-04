from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from time import time
import jwt
from app import db, login
from flask import current_app

#User table definition
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    transactions = db.relationship('Transaction', backref='user', lazy='dynamic')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow())
    desc = db.Column(db.String(240))

    def __repr__(self):
        return f"<User {self.username}- email: {self.email}"
    
    #Sets password in registration
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    #Checks submitted password against the password hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    #Gets the user a password reset token
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in}, current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

#Transaction table definition
class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_ingested = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    date_transaction = db.Column(db.DateTime, index=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchant.id'))
    desc = db.Column(db.String(240))

    def __repr__(self):
        return f"<Transaction {self.date_transaction}- {self.desc}>"
        
#Account table definition
class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    account_owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('account_type.id'))
    institution_id = db.Column(db.Integer, db.ForeignKey('institution.id'))
    account_name = db.Column(db.String(120))
    transactions = db.relationship('Transaction', backref='account', lazy='dynamic') #one account can have many transactions.
    desc = db.Column(db.String(240))

    def __repr__(self):
        return f"Account {self.account_name}"

#Institution table definition
class Institution(db.Model):
    __tablename__ = 'institution'
    id = db.Column(db.Integer, primary_key=True)
    institution_name = db.Column(db.String(64), index=True)
    desc = db.Column(db.String(240))
    

    def __repr__(self):
        return f"Institution {self.institution_name}"

#AccountType table definition
class AccountType(db.Model):
    __tablename__ = 'account_type'
    id = db.Column(db.Integer, primary_key=True)
    account_type = db.Column(db.String(64), index=True)
    desc = db.Column(db.String(240))

    def __repr__(self):
        return f"AccountType {self.account_type}"

#TransactionTag table definition
class TransactionTag(db.Model):
    __tablename__ = 'transaction_tag'
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'))
    tag = db.Column(db.String(64))
    desc = db.Column(db.String(240))

    def __repr__(self):
        return f"TransactionTag {self.tag}"

#Merchant table definition
class Merchant(db.Model):
    __tablename__ = 'merchant'
    id = db.Column(db.Integer, primary_key=True)
    merchant_name = db.Column(db.String(120))
    desc = db.Column(db.String(240))

    def __repr__(self):
        return f"Merchant {self.merchant_name}"

@login.user_loader
def load_user(id):
    return User.query.get(int(id))