from app import db
from datetime import datetime

#User table definition
class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    #transactions = db.relationship('Transaction', backref='user', lazy='dynamic')

    def __repr__(self):
        return "<User {}".format(self.username)

'''
class Transaction(db.Model):
    __tablename__ = 'transaction'
    transaction_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    date_ingested = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    date_transaction = db.Column(db.DateTime, index=True)
    #account_id = db.Column(db.Integer, ForeignKey('account.account_id'))
    #merchant_id = db.Column(db.Integer, ForeignKey('merchant.merchant_id'))
    desc = db.Column(db.String(120))

    def __repr__(self):
        return "<Transaction {}".format(self.date_transaction, self.desc)

Class Account(db.Model):
    __tablename__ = 'account'
    account_id = db.Column(db.Integer, primary_key=True)
    #institution_id = db.Column(db.Integer, ForeignKey('institution.institution_id'))
    #type_id = db.Column(db.Integer, ForeignKey('account_type.acount_type_id'))

Class Instutition(db.Model):
    __tablename__ = 'institution'
    institution_id = db.Column(db.integer, primary_key=True)
    #institution_name = db.Column(db.String(64), index=True)

Class AccountType(db.Model):
    __tablename__ = 'account_type'
    account_type_id = db.Column(db.integer, primary_key=True)
    #account_type = db.Column(db.String(64), index=True)

Class TransactionTag(db.Model)
    __tablename__ = 'transaction_tag'
    tag_id = db.Column(db.Integer, primary_key=True)
    #transaction_id = db.Column(db.Integer, ForeignKey('transaction.transaction_id'))
    #tag_main_type_id = db.Column(db.Integer, ForeignKey('tag_main_type.tag_main_type.id'))
    #tag = db.Column(db.String(64))

Class Merchant(db.Model)
    __tablename__ = 'merchant'
    merchant_id = db.Column(db.String(64), primary_key=True)

'''