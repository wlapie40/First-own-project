from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
app = Flask(__name__)


app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] =  r'sqlite:///db\Litchi.db'
db = SQLAlchemy(app)

# Many-to-Many Relationships
SPORT_MEMBERS = db.Table('SPORT_MEMBERS',
                db.Column('ID_SPORT',db.Integer,db.ForeignKey('SPORT.ID_SPORT')),
                db.Column('ID_FIGHTER',db.Integer,db.ForeignKey('FIGHTER.ID_FIGHTER')))

# Tabela laczaca zawodnika z walka
FIGHTER_FIGHTS = db.Table('FIGHTER_FIGHTS',
                          db.Column('ID_FIGHTER', db.Integer, db.ForeignKey('FIGHTER.ID_FIGHTER')),
                          db.Column('ID_FIGHT', db.Integer, db.ForeignKey('FIGHT.ID_FIGHT')))

# # Tabela laczaca zawodnika z menagerem
FIGHTER_MANAGER = db.Table('FIGHTER_MANAGER',
                           db.Column('ID_FIGHTER', db.Integer, db.ForeignKey('FIGHTER.ID_FIGHTER')),
                           db.Column('ID_MANAGER',db.Integer,db.ForeignKey('MANAGER.ID_MANAGER')))

class USER(UserMixin, db.Model):
    __tablename__ = 'USER'
    id = db.Column(db.Integer, primary_key=True)
    USERNAME = db.Column(db.String(15), unique=True)
    EMAIL = db.Column(db.String(50), unique=True)
    PASSWORD = db.Column(db.String(80))
    ACCOUNT_TYPE = db.Column(db.String(15))
    CREATION_DATE = db.Column(db.String(10))
    CREATE_TIME = db.Column(db.String(8))
    # One-to-One Relationships
    FIGHTER = db.relationship('FIGHTER', backref='USER', uselist=False)
    FEDERATION = db.relationship('FEDERATION', backref='USER', uselist=False)
    MANAGER = db.relationship('MANAGER', backref='USER', uselist=False)

class FIGHTER(db.Model):
    __tablename__ = 'FIGHTER'
    ID_FIGHTER = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(45))
    SURNAME = db.Column(db.String(45))
    NICKNAME = db.Column(db.String(45))
    CREATION_DATE = db.Column(db.String(10))
    CREATE_TIME = db.Column(db.String(8))
    OUT_OF_DATE = db.Column(db.String(10))
    ID_DOCUMENT = db.Column(db.String(45))
    # One-to-One Relationships
    USER_id = db.Column(db.Integer, db.ForeignKey('USER.id'))
    # One-to-Many Relationships
    ADDRESS = db.relationship('ADDRESS', backref='FIGHTER', lazy='dynamic')
    FIGHTER_DETAILS = db.relationship('FIGHTER_DETAILS', backref='FIGHTER',lazy='dynamic')
    CONTACT = db.relationship('CONTACT',backref='FIGHTER',lazy='dynamic')
    ID_FEDERATION = db.Column(db.Integer, db.ForeignKey('FEDERATION.ID_FEDERATION'))
    # # Many-to-Many Relationships
    SPORT_MEMBERS = db.relationship('SPORT', secondary=SPORT_MEMBERS, backref=db.backref('SPORT_MEMEBER', lazy='dynamic'))
    FIGHTS = db.relationship('FIGHT',secondary=FIGHTER_FIGHTS,backref=db.backref('FIGHTER_FIGHT', lazy='dynamic'))


class CONTACT(db.Model):
    __tablename__ = 'CONTACT'
    ID_CONTACT = db.Column(db.Integer, primary_key=True)
    PHONE_NUMBER = db.Column(db.String(20))
    PHONE_NUMBER2 = db.Column(db.String(20))
    E_MAIL = db.Column(db.String(45))
    # One-to-Many Relationdhips
    ID_FIGHTER = db.Column(db.Integer, db.ForeignKey('FIGHTER.ID_FIGHTER'))
    ID_FEDERATION = db.Column(db.Integer, db.ForeignKey('FEDERATION.ID_FEDERATION'))
    ID_MANAGER = db.Column(db.Integer, db.ForeignKey('MANAGER.ID_MANAGER'))

class EVENTS(db.Model):
    __tablename__ = 'EVENTS'
    ID_EVENT = db.Column(db.Integer, primary_key=True)
    EVENT_NAME = db.Column(db.String(50))
    CITY = db.Column(db.String(45))
    CONTINENT = db.Column(db.String(15))
    COUNTRY = db.Column(db.String(45))
    ZIP_CODE = db.Column(db.String(7))
    NUMBER_OF_FIGHTS = db.Column(db.String(2))
    STREET = db.Column(db.String(45))
    STREET_NUMBER = db.Column(db.String(10))
    DATE = db.Column(db.String(10))
    TIME = db.Column(db.String(8))
    NEED_FIGHTER_STATUS = db.Column(db.Boolean)
    CREATION_DATE = db.Column(db.String(10))
    CREATE_TIME = db.Column(db.String(8))
    EVENT_STATUS = db.Column(db.String(8))
    RECORD_UPDATED = db.Column(db.String(1))
    # One-to-many Relationships
    ID_FEDERATION = db.Column(db.Integer, db.ForeignKey('FEDERATION.ID_FEDERATION'))
    ID_MANAGER = db.Column(db.Integer,db.ForeignKey('MANAGER.ID_MANAGER'))
    ID_FIGHTER = db.Column(db.Integer, db.ForeignKey('FIGHTER.ID_FIGHTER'))
    ID_FIGHT = db.relationship('FIGHT', backref='EVENTS', lazy='dynamic')

class FIGHT(db.Model):
    __tablename__ = 'FIGHT'
    ID_FIGHT = db.Column(db.Integer, primary_key=True)
    ID_FIGHTER_1 = db.Column(db.String(6))
    ID_FIGHTER_2 = db.Column(db.String(6))
    WEIGHT_CATEGORY = db.Column(db.String(6))
    CREATION_DATE = db.Column(db.String(10))
    CREATE_TIME = db.Column(db.String(8))
    FIGHT_STATUS = db.Column(db.String(8))
    # One-to-many Relationships
    ID_EVENT = db.Column(db.Integer,db.ForeignKey(EVENTS.ID_EVENT))
    FEDERATION_ID = db.Column(db.Integer, db.ForeignKey('FEDERATION.ID_FEDERATION'))
    FIGHTER_ID = db.Column(db.Integer, db.ForeignKey('FIGHTER.ID_FIGHTER'))
    # Many-to-Many Relationships


class MANAGER(db.Model):
    __tablename__ = 'MANAGER'
    ID_MANAGER = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(45))
    SURNAME = db.Column(db.String(45))
    SPORT = db.Column(db.String(8))
    JOB_FIGHTER = db.Column(db.String(3))
    JOB_FIGHT = db.Column(db.String(3))
    CREATION_DATE = db.Column(db.String(10))
    CREATE_TIME = db.Column(db.String(8))
    # One-to-One Relationdhips
    USER_id = db.Column(db.Integer, db.ForeignKey('USER.id'))

    # One-to-Many Relationdhips
    ADDRESS = db.relationship('ADDRESS', backref='MANAGER', lazy='dynamic')
    CONTACT = db.relationship('CONTACT', backref='MANAGER', lazy='dynamic')

    # # Many-to-Many Relatios
    FIGHTER_MANAGER = db.relationship('FIGHTER', secondary=FIGHTER_MANAGER,
                                    backref=db.backref('FIGHTER_MENAGO', lazy='dynamic'))


class ADDRESS(db.Model):
    __tablename__ = 'ADDRESS'
    ID_ADDRESS = db.Column(db.Integer, primary_key=True)
    CONTINENT = db.Column(db.String(15))
    COUNTRY = db.Column(db.String(45))
    CITY = db.Column(db.String(45))
    ZIP_CODE = db.Column(db.String(7))
    STREET = db.Column(db.String(45))
    STREET_NUMBER = db.Column(db.String(10))
    # One-to-Many Relationdhips
    ID_FIGHTER = db.Column(db.Integer, db.ForeignKey('FIGHTER.ID_FIGHTER'))
    ID_MANAGER = db.Column(db.Integer, db.ForeignKey('MANAGER.ID_MANAGER'))
    ID_FEDERATION = db.Column(db.Integer,db.ForeignKey('FEDERATION.ID_FEDERATION'))

class FIGHTER_DETAILS(db.Model):
    __tablename__ = 'FIGHTER_DETAILS'
    ID_FIGHTER_DETAILS = db.Column(db.Integer, primary_key=True)
    WEIGHT_CATEGORY = db.Column(db.String(25))
    SPORT = db.Column(db.String(45))
    WEIGHT = db.Column(db.String(25))
    HEIGHT = db.Column(db.String(5))
    DATE_OF_BIRTH = db.Column(db.String(10))
    HEALTH_STATUS = db.Column(db.String(25))
    READY_TO_FIGHT_DATE = db.Column(db.String(25))
    HEALTH_DESCRIPTION = db.Column(db.String(300))
    FIGHT_STATUS = db.Column(db.String(30))
    FIGHT_STYLE = db.Column(db.String(8))
    NUMBER_OF_WINS = db.Column(db.String(3))
    NUMBER_OF_LOSS = db.Column(db.String(3))
    NUMBER_OF_DRAW = db.Column(db.String(2))
    NUMBER_OF_NC = db.Column(db.String(2))
    FREE_AGENT = db.Column(db.String(8))
    URL = db.Column(db.String(50))
    MANAGER_NEED = db.Column(db.String(1))
    # One-to-One Relationdhips
    ID_FIGHTER = db.Column(db.Integer, db.ForeignKey('FIGHTER.ID_FIGHTER'))

class FEDERATION(db.Model):
    __tablename__ = 'FEDERATION'
    ID_FEDERATION = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(45))
    SURNAME = db.Column(db.String(45))
    FEDERATION_NAME = db.Column(db.String(45))
    FEDERATION_CREATED_DATE = db.Column(db.String(45))
    FEDERATION_RANGE = db.Column(db.String(45))
    CREATION_DATE = db.Column(db.String(10))
    CREATE_TIME = db.Column(db.String(8))
    # One-to-One Relationships
    USER_id = db.Column(db.Integer, db.ForeignKey('USER.id'))


    # One-to-Many Relationdhips
    FIGHT = db.relationship('FIGHT',backref='FEDERATION',lazy='dynamic')
    ADDRESS = db.relationship('ADDRESS', backref='FEDERATION', lazy='dynamic')

    CONTACT = db.relationship('CONTACT', backref='FEDERATION', lazy='dynamic')
    FIGHTER = db.relationship('FIGHTER', backref='FEDERATION', lazy='dynamic')
    EVENTS = db.relationship('EVENTS', backref='FEDERATION', lazy='dynamic')


class SPORT(db.Model):
    __tablename__ = 'SPORT'
    ID_SPORT = db.Column(db.Integer, primary_key=True)
    SPORT_NAME = db.Column(db.String(45))

class AREA(db.Model):
    __tablename__ = 'AREA'
    ID = db.Column(db.Integer, primary_key=True)
    CONTINENT = db.Column(db.String(45))
    COUNTRY = db.Column(db.String(45))
    CITY = db.Column(db.String(45))

class LOCALIZATION(db.Model):
    __tablename__ = 'LOCALIZATION'
    ID = db.Column(db.Integer, primary_key=True)
    CONTINENT = db.Column(db.String(45))
    COUNTRY = db.Column(db.String(45))
    CITY = db.Column(db.String(45))

class FIGHT_REQUEST(db.Model):
    __tablename__ = 'FIGHT_REQUEST'
    ID_REQUEST = db.Column(db.Integer, primary_key=True)
    ID_FIGHTER = db.Column(db.String(6))
    ID_MANAGER = db.Column(db.String(6))
    WEIGHT_CATEGORY = db.Column(db.String(25))
    SPORT = db.Column(db.String(45))
    FIGHT_STYLE = db.Column(db.String(8))
    CONTINENT = db.Column(db.String(15))
    COUNTRY = db.Column(db.String(45))
    CITY = db.Column(db.String(45))

class NewPN(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    File = db.Column(db.String(300),unique=True)

class UPDATE_RECORDS(db.Model):
    __tablename__ = 'UPDATE_RECORDS'
    ID_EVENT = db.Column(db.String(4))
    ID_FIGHTER = db.Column(db.String(6))
    SCORE = db.Column(db.String(1))