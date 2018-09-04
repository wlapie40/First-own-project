from flask import Flask, render_template, request, url_for, redirect, session, flash, jsonify, send_file
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextField, DateField, TextAreaField, \
    DateTimeField, SubmitField, HiddenField, widgets, SelectMultipleField, RadioField
from wtforms_components import TimeField
from wtforms.validators import InputRequired, Email, Length, NumberRange
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from base64 import b64encode
from io import BytesIO
from wtforms.fields.html5 import DateField
import gc
import base64
import requests
#  database action
import time
import datetime
from dateutil.parser import parse
# has password
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, logout_user, login_required, current_user, user_logged_out, login_user
from flask_mail import Mail
from flask_mail import Message
import os
from account_type import FIGHTERS_LIST, MANAGERS_LIST, FEDERATIONS_LIST

# from functions import Id_Fighter
app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///db\Litchi.db'
db = SQLAlchemy(app)

# Mail send settings

app.config.update(dict(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='wlapie40@gmail.com',
    MAIL_PASSWORD='dnlspjggxjxtlyrc',
))
mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Many-to-Many Relationships
SPORT_MEMBERS = db.Table('SPORT_MEMBERS',
                         db.Column('ID_SPORT', db.Integer, db.ForeignKey('SPORT.ID_SPORT')),
                         db.Column('ID_FIGHTER', db.Integer, db.ForeignKey('FIGHTER.ID_FIGHTER')))

# Tabela laczaca zawodnika z walka
FIGHTER_FIGHTS = db.Table('FIGHTER_FIGHTS',
                          db.Column('ID_FIGHTER', db.Integer, db.ForeignKey('FIGHTER.ID_FIGHTER')),
                          db.Column('ID_FIGHT', db.Integer, db.ForeignKey('FIGHT.ID_FIGHT')))

# # Tabela laczaca zawodnika z menagerem
FIGHTER_MANAGER = db.Table('FIGHTER_MANAGER',
                           db.Column('ID_FIGHTER', db.Integer, db.ForeignKey('FIGHTER.ID_FIGHTER')),
                           db.Column('ID_MANAGER', db.Integer, db.ForeignKey('MANAGER.ID_MANAGER')))
FIGHTER_FEDERATION = db.Table('FIGHTER_FEDERATION',
                              db.Column('ID_FIGHTER', db.Integer, db.ForeignKey('FIGHTER.ID_FIGHTER')),
                              db.Column('ID_FEDERATION', db.Integer, db.ForeignKey('FEDERATION.ID_FEDERATION')))

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
    FIGHTER_DETAILS = db.relationship('FIGHTER_DETAILS', backref='FIGHTER', lazy='dynamic')
    MESSAGES = db.relationship('MESSAGES', backref='FIGHTER', lazy='dynamic')
    CONTACT = db.relationship('CONTACT', backref='FIGHTER', lazy='dynamic')
    ID_FEDERATION = db.Column(db.Integer, db.ForeignKey('FEDERATION.ID_FEDERATION'))

    # # Many-to-Many Relationships
    SPORT_MEMBERS = db.relationship('SPORT', secondary=SPORT_MEMBERS,
                                    backref=db.backref('SPORT_MEMEBER', lazy='dynamic'))
    FIGHTS = db.relationship('FIGHT', secondary=FIGHTER_FIGHTS, backref=db.backref('FIGHTER_FIGHT', lazy='dynamic'))


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
    DATE = db.Column(db.DATE)
    TIME = db.Column(db.TIME)
    NEED_FIGHTER_STATUS = db.Column(db.Boolean)
    CREATION_DATE = db.Column(db.String(25))
    CREATION_TIME = db.Column(db.String(25))
    EVENT_STATUS = db.Column(db.String(8))
    # One-to-many Relationships
    ID_FEDERATION = db.Column(db.Integer, db.ForeignKey('FEDERATION.ID_FEDERATION'))
    ID_MANAGER = db.Column(db.Integer, db.ForeignKey('MANAGER.ID_MANAGER'))
    ID_FIGHTER = db.Column(db.Integer, db.ForeignKey('FIGHTER.ID_FIGHTER'))
    ID_FIGHT = db.relationship('FIGHT', backref='EVENTS', lazy='dynamic')


class FIGHT(db.Model):
    __tablename__ = 'FIGHT'
    ID_FIGHT = db.Column(db.Integer, primary_key=True)
    WEIGHT_CATEGORY = db.Column(db.String(6))
    CREATION_DATE = db.Column(db.String(10))
    CREATE_TIME = db.Column(db.String(8))
    FIGHT_STATUS = db.Column(db.String(8))
    # One-to-many Relationships
    ID_EVENT = db.Column(db.Integer, db.ForeignKey(EVENTS.ID_EVENT))
    FEDERATION_ID = db.Column(db.Integer, db.ForeignKey('FEDERATION.ID_FEDERATION'))
    # Many-to-Many Relationships


class MANAGER(db.Model):
    __tablename__ = 'MANAGER'
    ID_MANAGER = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(45))
    SURNAME = db.Column(db.String(45))
    SPORT = db.Column(db.String(8))
    JOB_FIGHTERS = db.Column(db.String(3))
    JOB_FIGHTS = db.Column(db.String(3))
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
    ID_FEDERATION = db.Column(db.Integer, db.ForeignKey('FEDERATION.ID_FEDERATION'))


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
    NUMBER_OF_WINS = db.Column(db.String(8))
    NUMBER_OF_LOSS = db.Column(db.String(8))
    FREE_AGENT = db.Column(db.String(8))
    URL = db.Column(db.String(50))
    MANAGER_NEED = db.Column(db.String(3))
    # One-to-One Relationdhips
    ID_FIGHTER = db.Column(db.Integer, db.ForeignKey('FIGHTER.ID_FIGHTER'))

class MESSAGES(db.Model):
    __tablename__ = 'MESSAGES'
    ID_MESSAGE = db.Column(db.Integer, primary_key=True)
    SUBJECT = db.Column(db.String(25))
    TEXT = db.Column(db.String(400))
    ID_MANAGER = db.Column(db.String(7))
    ID_FEDERATION = db.Column(db.String(7))
    ID_FIGHTER = db.Column(db.String(7))
    STATUS = db.Column(db.String(7))
    CONFIRMATION = db.Column(db.String(1))
    FEDERATION_VISIBLE= db.Column(db.String(1))
    FIGHTER_VISIBLE = db.Column(db.String(1))
    MANAGER_VISIBLE = db.Column(db.String(1))
    # CONFIRMATION 0-reuest czeka na decyzje 1-request potwierdzony 4-request nie aktualny
    # One-to-Many Relationdhips
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
    FIGHT = db.relationship('FIGHT', backref='FEDERATION', lazy='dynamic')
    ADDRESS = db.relationship('ADDRESS', backref='FEDERATION', lazy='dynamic')

    CONTACT = db.relationship('CONTACT', backref='FEDERATION', lazy='dynamic')
    FIGHTER = db.relationship('FIGHTER', backref='FEDERATION', lazy='dynamic')
    EVENTS = db.relationship('EVENTS', backref='FEDERATION', lazy='dynamic')

    # Many-to-Many Relationdhips
    FIGHTER_FEDERATION = db.relationship('FIGHTER', secondary=FIGHTER_FEDERATION,
                                         backref=db.backref('FIGHTER_FEDERO', lazy='dynamic'))


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

class OPINION(db.Model):
    __tablename__ = 'OPINION'
    ID_OPINION = db.Column(db.Integer, primary_key=True)
    ID_FIGHTER = db.Column(db.String(7))
    ID_MANAGER = db.Column(db.String(7))
    CONTACT_STARS = db.Column(db.String(1))
    PREAPARE_STARS = db.Column(db.String(1))
    TEXT = db.Column(db.String(250))

class IMAGES(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(300), unique=True)
    DATA = db.Column(db.BLOB)
    USERNAME = db.Column(db.String(15))


TupleEventStatus = [('Finished', 'Finished'), ('Pending', 'Pending'), ('Incoming', 'Incoming')]
TupleEventStatusSearch = [('%', 'All status'), ('Finished', 'Finished'), ('Pending', 'Pending'),
                          ('Incoming', 'Incoming')]
TupleSport = [('MMA', 'MMA'), ('K1', 'K1'), ('Boxing', 'Boxing'), ('Kick-Boxing', 'Kick-Boxing')]
TupleContinentSearch = [('%', 'All'), ('Asia', 'Asia'), ('Africa', 'Africa'), ('Australia', 'Australia'),
                        ('Europe', 'Europe'), ('North America', 'North America'), ('South America', 'South America')]
TupleContinent = [('Asia', 'Asia'), ('Africa', 'Africa'), ('Australia', 'Australia'), ('Europe', 'Europe'),
                  ('North America', 'North America'), ('South America', 'South America')]
TuplePreferFightStyle = [('Striker', 'Striker'), ('Grappler', 'Grappler'), ('Wrestler', 'Wrestler')]
TuplePreferFightStyleSearch = [('%', 'All'), ('Striker', 'Striker'), ('Grappler', 'Grappler'), ('Wrestler', 'Wrestler')]
TupleACCOUNT_TYPE = [('Standard user', 'Standard user'), ('Fighter', 'Fighter'), ('Manager', 'Manager'),
                     ('Federation', 'Federation')]
TupleWeightCatMenSearch = [('%', 'All'), ('Strawweight', 'Strawweight'), ('Bantamweight', 'Bantamweight'),
                           ('Featherweight', 'Featherweight'), ('Welterweight', 'Welterweight'),
                           ('Middleweight', 'Middleweight'), ('Light heavyweight', 'Light heavyweight'),
                           ('Heavyweight', 'Heavyweight')]
TupleWeightCatMen = [('Strawweight', 'Strawweight'), ('Bantamweight', 'Bantamweight'),
                     ('Featherweight', 'Featherweight'), ('Welterweight', 'Welterweight'),
                     ('Middleweight', 'Middleweight'), ('Light heavyweight', 'Light heavyweight'),
                     ('Heavyweight', 'Heavyweight')]
TupleWeightCatWom = [('Strawweight', 'Strawweight'), ('Bantamweight', 'Bantamweight'),
                     ('Featherweight', 'FEATHERWEIGHT')]
TupleHealthCondition = [('Healthy', 'Healthy'), ('Light injury', 'Light injury'), ('Serious injury', 'Serious injury')]
TupleFightStatus = [('Looking for fight', 'Looking for fight'), ('Maybe in the future', 'Maybe in the future'),
                    ('No fight', 'No fight')]
TupleCountrySearch = [('%', 'All'), ('Afghanistan', 'Afghanistan'),
                      ('Aland Islands', 'Aland Islands'),
                      ('Albania', 'Albania'),
                      ('Algeria', 'Algeria'),
                      ('American Samoa', 'American Samoa'),
                      ('Andorra', 'Andorra'),
                      ('Angola', 'Angola'),
                      ('Anguilla', 'Anguilla'),
                      ('Antarctica', 'Antarctica'),
                      ('Antigua and Barbuda', 'Antigua and Barbuda'),
                      ('Argentina', 'Argentina'),
                      ('Armenia', 'Armenia'),
                      ('Aruba', 'Aruba'),
                      ('Australia', 'Australia'),
                      ('Austria', 'Austria'),
                      ('Azerbaijan', 'Azerbaijan'),
                      ('Bahamas', 'Bahamas'),
                      ('Bahrain', 'Bahrain'),
                      ('Bangladesh', 'Bangladesh'),
                      ('Barbados', 'Barbados'),
                      ('Belarus', 'Belarus'),
                      ('Belgium', 'Belgium'),
                      ('Belize', 'Belize'),
                      ('Benin', 'Benin'),
                      ('Bermuda', 'Bermuda'),
                      ('Bhutan', 'Bhutan'),
                      ('Bolivia', 'Bolivia'),
                      ('Bosnia and Herzegovina', 'Bosnia and Herzegovina'),
                      ('Botswana', 'Botswana'),
                      ('Bouvet Island', 'Bouvet Island'),
                      ('Brazil', 'Brazil'),
                      ('British Virgin Islands', 'British Virgin Islands'),
                      ('British Indian Ocean Territory', 'British Indian Ocean Territory'),
                      ('Brunei Darussalam', 'Brunei Darussalam'),
                      ('Bulgaria', 'Bulgaria'),
                      ('Burkina Faso', 'Burkina Faso'),
                      ('Burundi', 'Burundi'),
                      ('Cambodia', 'Cambodia'),
                      ('Cameroon', 'Cameroon'),
                      ('Canada', 'Canada'),
                      ('Cape Verde', 'Cape Verde'),
                      ('Cayman Islands', 'Cayman Islands'),
                      ('Central African Republic', 'Central African Republic'),
                      ('Chad', 'Chad'),
                      ('Chile', 'Chile'),
                      ('China', 'China'),
                      ('Hong Kong, SAR China', 'Hong Kong, SAR China'),
                      ('Macao, SAR China', 'Macao, SAR China'),
                      ('Christmas Island', 'Christmas Island'),
                      ('Cocos (Keeling) Islands', 'Cocos (Keeling) Islands'),
                      ('Colombia', 'Colombia'),
                      ('Comoros', 'Comoros'),
                      ('Congo (Brazzaville)', 'Congo (Brazzaville)'),
                      ('Congo, (Kinshasa)', 'Congo, (Kinshasa)'),
                      ('Cook Islands', 'Cook Islands'),
                      ('Costa Rica', 'Costa Rica'),
                      ("Côte d'Ivoire", "Côte d'Ivoire"),
                      ('Croatia', 'Croatia'),
                      ('Cuba', 'Cuba'),
                      ('Cyprus', 'Cyprus'),
                      ('Czech Republic', 'Czech Republic'),
                      ('Denmark', 'Denmark'),
                      ('Djibouti', 'Djibouti'),
                      ('Dominica', 'Dominica'),
                      ('Dominican Republic', 'Dominican Republic'),
                      ('Ecuador', 'Ecuador'),
                      ('Egypt', 'Egypt'),
                      ('El Salvador', 'El Salvador'),
                      ('Equatorial Guinea', 'Equatorial Guinea'),
                      ('Eritrea', 'Eritrea'),
                      ('Estonia', 'Estonia'),
                      ('Ethiopia', 'Ethiopia'),
                      ('Falkland Islands (Malvinas)', 'Falkland Islands (Malvinas)'),
                      ('Faroe Islands', 'Faroe Islands'),
                      ('Fiji', 'Fiji'),
                      ('Finland', 'Finland'),
                      ('France', 'France'),
                      ('French Guiana', 'French Guiana'),
                      ('French Polynesia', 'French Polynesia'),
                      ('French Southern Territories', 'French Southern Territories'),
                      ('Gabon', 'Gabon'),
                      ('Gambia', 'Gambia'),
                      ('Georgia', 'Georgia'),
                      ('Germany', 'Germany'),
                      ('Ghana', 'Ghana'),
                      ('Gibraltar', 'Gibraltar'),
                      ('Greece', 'Greece'),
                      ('Greenland', 'Greenland'),
                      ('Grenada', 'Grenada'),
                      ('Guadeloupe', 'Guadeloupe'),
                      ('Guam', 'Guam'),
                      ('Guatemala', 'Guatemala'),
                      ('Guernsey', 'Guernsey'),
                      ('Guinea', 'Guinea'),
                      ('Guinea-Bissau', 'Guinea-Bissau'),
                      ('Guyana', 'Guyana'),
                      ('Haiti', 'Haiti'),
                      ('Heard and Mcdonald Islands', 'Heard and Mcdonald Islands'),
                      ('Holy See (Vatican City State)', 'Holy See (Vatican City State)'),
                      ('Honduras', 'Honduras'),
                      ('Hungary', 'Hungary'),
                      ('Iceland', 'Iceland'),
                      ('India', 'India'),
                      ('Indonesia', 'Indonesia'),
                      ('Iran, Islamic Republic of', 'Iran, Islamic Republic of'),
                      ('Iraq', 'Iraq'),
                      ('Ireland', 'Ireland'),
                      ('Isle of Man', 'Isle of Man'),
                      ('Israel', 'Israel'),
                      ('Italy', 'Italy'),
                      ('Jamaica', 'Jamaica'),
                      ('Japan', 'Japan'),
                      ('Jersey', 'Jersey'),
                      ('Jordan', 'Jordan'),
                      ('Kazakhstan', 'Kazakhstan'),
                      ('Kenya', 'Kenya'),
                      ('Kiribati', 'Kiribati'),
                      ('Korea (North)', 'Korea (North)'),
                      ('Korea (South)', 'Korea (South)'),
                      ('Kuwait', 'Kuwait'),
                      ('Kyrgyzstan', 'Kyrgyzstan'),
                      ('Lao PDR', 'Lao PDR'),
                      ('Latvia', 'Latvia'),
                      ('Lebanon', 'Lebanon'),
                      ('Lesotho', 'Lesotho'),
                      ('Liberia', 'Liberia'),
                      ('Libya', 'Libya'),
                      ('Liechtenstein', 'Liechtenstein'),
                      ('Lithuania', 'Lithuania'),
                      ('Luxembourg', 'Luxembourg'),
                      ('Macedonia, Republic of', 'Macedonia, Republic of'),
                      ('Madagascar', 'Madagascar'),
                      ('Malawi', 'Malawi'),
                      ('Malaysia', 'Malaysia'),
                      ('Maldives', 'Maldives'),
                      ('Mali', 'Mali'),
                      ('Malta', 'Malta'),
                      ('Marshall Islands', 'Marshall Islands'),
                      ('Martinique', 'Martinique'),
                      ('Mauritania', 'Mauritania'),
                      ('Mauritius', 'Mauritius'),
                      ('Mayotte', 'Mayotte'),
                      ('Mexico', 'Mexico'),
                      ('Micronesia, Federated States of', 'Micronesia, Federated States of'),
                      ('Moldova', 'Moldova'),
                      ('Monaco', 'Monaco'),
                      ('Mongolia', 'Mongolia'),
                      ('Montenegro', 'Montenegro'),
                      ('Montserrat', 'Montserrat'),
                      ('Morocco', 'Morocco'),
                      ('Mozambique', 'Mozambique'),
                      ('Myanmar', 'Myanmar'),
                      ('Namibia', 'Namibia'),
                      ('Nauru', 'Nauru'),
                      ('Nepal', 'Nepal'),
                      ('Netherlands', 'Netherlands'),
                      ('Netherlands Antilles', 'Netherlands Antilles'),
                      ('New Caledonia', 'New Caledonia'),
                      ('New Zealand', 'New Zealand'),
                      ('Nicaragua', 'Nicaragua'),
                      ('Niger', 'Niger'),
                      ('Nigeria', 'Nigeria'),
                      ('Niue', 'Niue'),
                      ('Norfolk Island', 'Norfolk Island'),
                      ('Northern Mariana Islands', 'Northern Mariana Islands'),
                      ('Norway', 'Norway'),
                      ('Oman', 'Oman'),
                      ('Pakistan', 'Pakistan'),
                      ('Palau', 'Palau'),
                      ('Palestinian Territory', 'Palestinian Territory'),
                      ('Panama', 'Panama'),
                      ('Papua New Guinea', 'Papua New Guinea'),
                      ('Paraguay', 'Paraguay'),
                      ('Peru', 'Peru'),
                      ('Philippines', 'Philippines'),
                      ('Pitcairn', 'Pitcairn'),
                      ('Poland', 'Poland'),
                      ('Portugal', 'Portugal'),
                      ('Puerto Rico', 'Puerto Rico'),
                      ('Qatar', 'Qatar'),
                      ('Réunion', 'Réunion'),
                      ('Romania', 'Romania'),
                      ('Russian Federation', 'Russian Federation'),
                      ('Rwanda', 'Rwanda'),
                      ('Saint-Barthélemy', 'Saint-Barthélemy'),
                      ('Saint Helena', 'Saint Helena'),
                      ('Saint Kitts and Nevis', 'Saint Kitts and Nevis'),
                      ('Saint Lucia', 'Saint Lucia'),
                      ('Saint-Martin (French part)', 'Saint-Martin (French part)'),
                      ('Saint Pierre and Miquelon', 'Saint Pierre and Miquelon'),
                      ('Saint Vincent and Grenadines', 'Saint Vincent and Grenadines'),
                      ('Samoa', 'Samoa'),
                      ('San Marino', 'San Marino'),
                      ('Sao Tome and Principe', 'Sao Tome and Principe'),
                      ('Saudi Arabia', 'Saudi Arabia'),
                      ('Senegal', 'Senegal'),
                      ('Serbia', 'Serbia'),
                      ('Seychelles', 'Seychelles'),
                      ('Sierra Leone', 'Sierra Leone'),
                      ('Singapore', 'Singapore'),
                      ('Slovakia', 'Slovakia'),
                      ('Slovenia', 'Slovenia'),
                      ('Solomon Islands', 'Solomon Islands'),
                      ('Somalia', 'Somalia'),
                      ('South Africa', 'South Africa'),
                      ('South Georgia and the South Sandwich Islands', 'South Georgia and the South Sandwich Islands'),
                      ('South Sudan', 'South Sudan'),
                      ('Spain', 'Spain'),
                      ('Sri Lanka', 'Sri Lanka'),
                      ('Sudan', 'Sudan'),
                      ('Suriname', 'Suriname'),
                      ('Svalbard and Jan Mayen Islands', 'Svalbard and Jan Mayen Islands'),
                      ('Swaziland', 'Swaziland'),
                      ('Sweden', 'Sweden'),
                      ('Switzerland', 'Switzerland'),
                      ('Syrian Arab Republic (Syria)', 'Syrian Arab Republic (Syria)'),
                      ('Taiwan, Republic of China', 'Taiwan, Republic of China'),
                      ('Tajikistan', 'Tajikistan'),
                      ('Tanzania, United Republic of', 'Tanzania, United Republic of'),
                      ('Thailand', 'Thailand'),
                      ('Timor-Leste', 'Timor-Leste'),
                      ('Togo', 'Togo'),
                      ('Tokelau', 'Tokelau'),
                      ('Tonga', 'Tonga'),
                      ('Trinidad and Tobago', 'Trinidad and Tobago'),
                      ('Tunisia', 'Tunisia'),
                      ('Turkey', 'Turkey'),
                      ('Turkmenistan', 'Turkmenistan'),
                      ('Turks and Caicos Islands', 'Turks and Caicos Islands'),
                      ('Tuvalu', 'Tuvalu'),
                      ('Uganda', 'Uganda'),
                      ('Ukraine', 'Ukraine'),
                      ('United Arab Emirates', 'United Arab Emirates'),
                      ('United Kingdom', 'United Kingdom'),
                      ('United States of America', 'United States of America'),
                      ('US Minor Outlying Islands', 'US Minor Outlying Islands'),
                      ('Uruguay', 'Uruguay'),
                      ('Uzbekistan', 'Uzbekistan'),
                      ('Vanuatu', 'Vanuatu'),
                      ('Venezuela (Bolivarian Republic)', 'Venezuela (Bolivarian Republic)'),
                      ('Viet Nam', 'Viet Nam'),
                      ('Virgin Islands, US', 'Virgin Islands, US'),
                      ('Wallis and Futuna Islands', 'Wallis and Futuna Islands'),
                      ('Western Sahara', 'Western Sahara'),
                      ('Yemen', 'Yemen'),
                      ('Zambia', 'Zambia'),
                      ('Zimbabwe', 'Zimbabwe')]

TupleCountry = [('', ''), ('Afghanistan', 'Afghanistan'),
                ('Aland Islands', 'Aland Islands'),
                ('Albania', 'Albania'),
                ('Algeria', 'Algeria'),
                ('American Samoa', 'American Samoa'),
                ('Andorra', 'Andorra'),
                ('Angola', 'Angola'),
                ('Anguilla', 'Anguilla'),
                ('Antarctica', 'Antarctica'),
                ('Antigua and Barbuda', 'Antigua and Barbuda'),
                ('Argentina', 'Argentina'),
                ('Armenia', 'Armenia'),
                ('Aruba', 'Aruba'),
                ('Australia', 'Australia'),
                ('Austria', 'Austria'),
                ('Azerbaijan', 'Azerbaijan'),
                ('Bahamas', 'Bahamas'),
                ('Bahrain', 'Bahrain'),
                ('Bangladesh', 'Bangladesh'),
                ('Barbados', 'Barbados'),
                ('Belarus', 'Belarus'),
                ('Belgium', 'Belgium'),
                ('Belize', 'Belize'),
                ('Benin', 'Benin'),
                ('Bermuda', 'Bermuda'),
                ('Bhutan', 'Bhutan'),
                ('Bolivia', 'Bolivia'),
                ('Bosnia and Herzegovina', 'Bosnia and Herzegovina'),
                ('Botswana', 'Botswana'),
                ('Bouvet Island', 'Bouvet Island'),
                ('Brazil', 'Brazil'),
                ('British Virgin Islands', 'British Virgin Islands'),
                ('British Indian Ocean Territory', 'British Indian Ocean Territory'),
                ('Brunei Darussalam', 'Brunei Darussalam'),
                ('Bulgaria', 'Bulgaria'),
                ('Burkina Faso', 'Burkina Faso'),
                ('Burundi', 'Burundi'),
                ('Cambodia', 'Cambodia'),
                ('Cameroon', 'Cameroon'),
                ('Canada', 'Canada'),
                ('Cape Verde', 'Cape Verde'),
                ('Cayman Islands', 'Cayman Islands'),
                ('Central African Republic', 'Central African Republic'),
                ('Chad', 'Chad'),
                ('Chile', 'Chile'),
                ('China', 'China'),
                ('Hong Kong, SAR China', 'Hong Kong, SAR China'),
                ('Macao, SAR China', 'Macao, SAR China'),
                ('Christmas Island', 'Christmas Island'),
                ('Cocos (Keeling) Islands', 'Cocos (Keeling) Islands'),
                ('Colombia', 'Colombia'),
                ('Comoros', 'Comoros'),
                ('Congo (Brazzaville)', 'Congo (Brazzaville)'),
                ('Congo, (Kinshasa)', 'Congo, (Kinshasa)'),
                ('Cook Islands', 'Cook Islands'),
                ('Costa Rica', 'Costa Rica'),
                ("Côte d'Ivoire", "Côte d'Ivoire"),
                ('Croatia', 'Croatia'),
                ('Cuba', 'Cuba'),
                ('Cyprus', 'Cyprus'),
                ('Czech Republic', 'Czech Republic'),
                ('Denmark', 'Denmark'),
                ('Djibouti', 'Djibouti'),
                ('Dominica', 'Dominica'),
                ('Dominican Republic', 'Dominican Republic'),
                ('Ecuador', 'Ecuador'),
                ('Egypt', 'Egypt'),
                ('El Salvador', 'El Salvador'),
                ('Equatorial Guinea', 'Equatorial Guinea'),
                ('Eritrea', 'Eritrea'),
                ('Estonia', 'Estonia'),
                ('Ethiopia', 'Ethiopia'),
                ('Falkland Islands (Malvinas)', 'Falkland Islands (Malvinas)'),
                ('Faroe Islands', 'Faroe Islands'),
                ('Fiji', 'Fiji'),
                ('Finland', 'Finland'),
                ('France', 'France'),
                ('French Guiana', 'French Guiana'),
                ('French Polynesia', 'French Polynesia'),
                ('French Southern Territories', 'French Southern Territories'),
                ('Gabon', 'Gabon'),
                ('Gambia', 'Gambia'),
                ('Georgia', 'Georgia'),
                ('Germany', 'Germany'),
                ('Ghana', 'Ghana'),
                ('Gibraltar', 'Gibraltar'),
                ('Greece', 'Greece'),
                ('Greenland', 'Greenland'),
                ('Grenada', 'Grenada'),
                ('Guadeloupe', 'Guadeloupe'),
                ('Guam', 'Guam'),
                ('Guatemala', 'Guatemala'),
                ('Guernsey', 'Guernsey'),
                ('Guinea', 'Guinea'),
                ('Guinea-Bissau', 'Guinea-Bissau'),
                ('Guyana', 'Guyana'),
                ('Haiti', 'Haiti'),
                ('Heard and Mcdonald Islands', 'Heard and Mcdonald Islands'),
                ('Holy See (Vatican City State)', 'Holy See (Vatican City State)'),
                ('Honduras', 'Honduras'),
                ('Hungary', 'Hungary'),
                ('Iceland', 'Iceland'),
                ('India', 'India'),
                ('Indonesia', 'Indonesia'),
                ('Iran, Islamic Republic of', 'Iran, Islamic Republic of'),
                ('Iraq', 'Iraq'),
                ('Ireland', 'Ireland'),
                ('Isle of Man', 'Isle of Man'),
                ('Israel', 'Israel'),
                ('Italy', 'Italy'),
                ('Jamaica', 'Jamaica'),
                ('Japan', 'Japan'),
                ('Jersey', 'Jersey'),
                ('Jordan', 'Jordan'),
                ('Kazakhstan', 'Kazakhstan'),
                ('Kenya', 'Kenya'),
                ('Kiribati', 'Kiribati'),
                ('Korea (North)', 'Korea (North)'),
                ('Korea (South)', 'Korea (South)'),
                ('Kuwait', 'Kuwait'),
                ('Kyrgyzstan', 'Kyrgyzstan'),
                ('Lao PDR', 'Lao PDR'),
                ('Latvia', 'Latvia'),
                ('Lebanon', 'Lebanon'),
                ('Lesotho', 'Lesotho'),
                ('Liberia', 'Liberia'),
                ('Libya', 'Libya'),
                ('Liechtenstein', 'Liechtenstein'),
                ('Lithuania', 'Lithuania'),
                ('Luxembourg', 'Luxembourg'),
                ('Macedonia, Republic of', 'Macedonia, Republic of'),
                ('Madagascar', 'Madagascar'),
                ('Malawi', 'Malawi'),
                ('Malaysia', 'Malaysia'),
                ('Maldives', 'Maldives'),
                ('Mali', 'Mali'),
                ('Malta', 'Malta'),
                ('Marshall Islands', 'Marshall Islands'),
                ('Martinique', 'Martinique'),
                ('Mauritania', 'Mauritania'),
                ('Mauritius', 'Mauritius'),
                ('Mayotte', 'Mayotte'),
                ('Mexico', 'Mexico'),
                ('Micronesia, Federated States of', 'Micronesia, Federated States of'),
                ('Moldova', 'Moldova'),
                ('Monaco', 'Monaco'),
                ('Mongolia', 'Mongolia'),
                ('Montenegro', 'Montenegro'),
                ('Montserrat', 'Montserrat'),
                ('Morocco', 'Morocco'),
                ('Mozambique', 'Mozambique'),
                ('Myanmar', 'Myanmar'),
                ('Namibia', 'Namibia'),
                ('Nauru', 'Nauru'),
                ('Nepal', 'Nepal'),
                ('Netherlands', 'Netherlands'),
                ('Netherlands Antilles', 'Netherlands Antilles'),
                ('New Caledonia', 'New Caledonia'),
                ('New Zealand', 'New Zealand'),
                ('Nicaragua', 'Nicaragua'),
                ('Niger', 'Niger'),
                ('Nigeria', 'Nigeria'),
                ('Niue', 'Niue'),
                ('Norfolk Island', 'Norfolk Island'),
                ('Northern Mariana Islands', 'Northern Mariana Islands'),
                ('Norway', 'Norway'),
                ('Oman', 'Oman'),
                ('Pakistan', 'Pakistan'),
                ('Palau', 'Palau'),
                ('Palestinian Territory', 'Palestinian Territory'),
                ('Panama', 'Panama'),
                ('Papua New Guinea', 'Papua New Guinea'),
                ('Paraguay', 'Paraguay'),
                ('Peru', 'Peru'),
                ('Philippines', 'Philippines'),
                ('Pitcairn', 'Pitcairn'),
                ('Poland', 'Poland'),
                ('Portugal', 'Portugal'),
                ('Puerto Rico', 'Puerto Rico'),
                ('Qatar', 'Qatar'),
                ('Réunion', 'Réunion'),
                ('Romania', 'Romania'),
                ('Russian Federation', 'Russian Federation'),
                ('Rwanda', 'Rwanda'),
                ('Saint-Barthélemy', 'Saint-Barthélemy'),
                ('Saint Helena', 'Saint Helena'),
                ('Saint Kitts and Nevis', 'Saint Kitts and Nevis'),
                ('Saint Lucia', 'Saint Lucia'),
                ('Saint-Martin (French part)', 'Saint-Martin (French part)'),
                ('Saint Pierre and Miquelon', 'Saint Pierre and Miquelon'),
                ('Saint Vincent and Grenadines', 'Saint Vincent and Grenadines'),
                ('Samoa', 'Samoa'),
                ('San Marino', 'San Marino'),
                ('Sao Tome and Principe', 'Sao Tome and Principe'),
                ('Saudi Arabia', 'Saudi Arabia'),
                ('Senegal', 'Senegal'),
                ('Serbia', 'Serbia'),
                ('Seychelles', 'Seychelles'),
                ('Sierra Leone', 'Sierra Leone'),
                ('Singapore', 'Singapore'),
                ('Slovakia', 'Slovakia'),
                ('Slovenia', 'Slovenia'),
                ('Solomon Islands', 'Solomon Islands'),
                ('Somalia', 'Somalia'),
                ('South Africa', 'South Africa'),
                ('South Georgia and the South Sandwich Islands', 'South Georgia and the South Sandwich Islands'),
                ('South Sudan', 'South Sudan'),
                ('Spain', 'Spain'),
                ('Sri Lanka', 'Sri Lanka'),
                ('Sudan', 'Sudan'),
                ('Suriname', 'Suriname'),
                ('Svalbard and Jan Mayen Islands', 'Svalbard and Jan Mayen Islands'),
                ('Swaziland', 'Swaziland'),
                ('Sweden', 'Sweden'),
                ('Switzerland', 'Switzerland'),
                ('Syrian Arab Republic (Syria)', 'Syrian Arab Republic (Syria)'),
                ('Taiwan, Republic of China', 'Taiwan, Republic of China'),
                ('Tajikistan', 'Tajikistan'),
                ('Tanzania, United Republic of', 'Tanzania, United Republic of'),
                ('Thailand', 'Thailand'),
                ('Timor-Leste', 'Timor-Leste'),
                ('Togo', 'Togo'),
                ('Tokelau', 'Tokelau'),
                ('Tonga', 'Tonga'),
                ('Trinidad and Tobago', 'Trinidad and Tobago'),
                ('Tunisia', 'Tunisia'),
                ('Turkey', 'Turkey'),
                ('Turkmenistan', 'Turkmenistan'),
                ('Turks and Caicos Islands', 'Turks and Caicos Islands'),
                ('Tuvalu', 'Tuvalu'),
                ('Uganda', 'Uganda'),
                ('Ukraine', 'Ukraine'),
                ('United Arab Emirates', 'United Arab Emirates'),
                ('United Kingdom', 'United Kingdom'),
                ('United States of America', 'United States of America'),
                ('US Minor Outlying Islands', 'US Minor Outlying Islands'),
                ('Uruguay', 'Uruguay'),
                ('Uzbekistan', 'Uzbekistan'),
                ('Vanuatu', 'Vanuatu'),
                ('Venezuela (Bolivarian Republic)', 'Venezuela (Bolivarian Republic)'),
                ('Viet Nam', 'Viet Nam'),
                ('Virgin Islands, US', 'Virgin Islands, US'),
                ('Wallis and Futuna Islands', 'Wallis and Futuna Islands'),
                ('Western Sahara', 'Western Sahara'),
                ('Yemen', 'Yemen'),
                ('Zambia', 'Zambia'),
                ('Zimbabwe', 'Zimbabwe')]


class FindFederation(FlaskForm):
    CONTINENT = SelectField(u'Continent', choices=TupleContinentSearch)
    COUNTRY = SelectField(u'Country', choices=TupleCountrySearch)
    CITY = StringField(u'City')


class LoginForm(FlaskForm):
    USERNAME = StringField('Username', validators=[InputRequired(), Length(min=3, max=15)])
    PASSWORD = PasswordField('Password', validators=[InputRequired(), Length(min=3, max=80)])
    REMEMBER = BooleanField('Remember me')


class RegisterForm(FlaskForm):
    EMAIL = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    USERNAME = StringField('Username', validators=[InputRequired(), Length(min=3, max=15)])
    PASSWORD = PasswordField('Password', validators=[InputRequired(), Length(min=3, max=80)])
    ACCOUNT_TYPE = SelectField(u'Choose correct account type', choices=TupleACCOUNT_TYPE)


# AccountForm jest dla managera,fightera i SEO
class FighterAccountForm(FlaskForm):
    NAME = StringField(u'Name', validators=[InputRequired(), Length(min=3, max=25)])
    NICKNAME = StringField(u'Nickname', validators=[Length(max=50)])
    SURNAME = StringField(u'Surname', validators=[InputRequired(), Length(min=1, max=45)])
    CONTINENT = SelectField(u'Choose continent', choices=TupleContinent)
    COUNTRY = SelectField(u'Country', choices=TupleCountry)
    CITY = StringField(u'City', validators=[InputRequired(), Length(min=1, max=45)])
    ZIP_CODE = StringField(u'Zip-code', validators=[InputRequired(), Length(min=1, max=7)])
    STREET = StringField(u'Street', validators=[InputRequired(), Length(min=1, max=45)])
    STREET_NUMBER = StringField(u'Street number', validators=[InputRequired(), Length(min=1, max=10)])
    PHONE_NUMBER = StringField(u'Phone number 1', validators=[InputRequired(), Length(min=6, max=20)])
    PHONE_NUMBER2 = StringField(u'Phone number 2 *')
    WEIGHT_CATEGORY = SelectField(u'Choose Your weight category *', choices=TupleWeightCatMen)
    WEIGHT = StringField(u'What is Your weight [lb] ? *')
    HEIGHT = StringField(u'Your height: *')
    SPORT = SelectField(u'Sport', choices=TupleSport)
    FIGHT_STYLE = SelectField(u'What kind of fight do You prefer?', choices=TuplePreferFightStyle)
    FIGHT_STATUS = SelectField(u'Are You looking for fight? *', choices=TupleFightStatus)
    NUMBER_OF_WINS = StringField(u'How many fights have You win ?')
    NUMBER_OF_LOSS = StringField(u'How many fights have You loss ?')
    FREE_AGENT = SelectField(u'Do You have any exclusive contract ?', choices=[('Yes', 'Yes'), ('No', 'No')])
    URL = StringField(u'Paste http link from Sherdog.com')


class FederationAccountForm(FlaskForm):
    NAME = StringField(u'Name', validators=[InputRequired(), Length(min=3, max=15)])
    SURNAME = StringField(u'Surname', validators=[InputRequired(), Length(min=1, max=45)])
    CONTINENT = SelectField(u'Choose continent', choices=TupleContinent)
    COUNTRY = SelectField(u'Country', choices=TupleCountry)
    CITY = StringField(u'City', validators=[InputRequired(), Length(min=1, max=45)])
    ZIP_CODE = StringField(u'Zip-code', validators=[InputRequired(), Length(min=1, max=7)])
    STREET = StringField(u'Street', validators=[InputRequired(), Length(min=1, max=45)])
    STREET_NUMBER = StringField(u'Street number', validators=[InputRequired(), Length(min=1, max=10)])
    PHONE_NUMBER = StringField(u'Phone number 1', validators=[InputRequired(), Length(min=6, max=20)])
    PHONE_NUMBER2 = StringField(u'Phone number 2 *')
    FEDERATION_NAME = StringField(u'What is Your federation name ?',
                                  validators=[InputRequired(), Length(min=2, max=50)])
    # FEDERATION_RANGE = SelectMultipleField(u'Where do You organise fights ?',choices=TupleContinent,default = ['1', '3'])
    FEDERATION_CREATED_DATE = StringField(u'Start yeaer')
    SPORT_NAME = SelectField(u'Choose sport', choices=TupleSport)


class ManagerAccountForm(FlaskForm):
    NAME = StringField(u'Name', validators=[InputRequired(), Length(min=3, max=15)])
    SURNAME = StringField(u'Surname', validators=[InputRequired(), Length(min=1, max=45)])
    CONTINENT = SelectField(u'Choose continent', choices=TupleContinent)
    COUNTRY = SelectField(u'Country', choices=TupleCountry)
    CITY = StringField(u'City', validators=[InputRequired(), Length(min=1, max=45)])
    ZIP_CODE = StringField(u'Zip-code', validators=[InputRequired(), Length(min=1, max=7)])
    STREET = StringField(u'Street', validators=[InputRequired(), Length(min=1, max=45)])
    STREET_NUMBER = StringField(u'Street number', validators=[InputRequired(), Length(min=1, max=10)])
    PHONE_NUMBER = StringField(u'Phone number 1', validators=[InputRequired(), Length(min=6, max=20)])
    PHONE_NUMBER2 = StringField(u'Phone number 2 *')
    SPORT_NAME = SelectField(u'Choose sport for which You deal with', choices=TupleSport)


ContinentList = []
CountryList = []
CityList = []


class Area(FlaskForm):
    CONTINENT = SelectField(u'Continent', choices=ContinentList)
    COUNTRY = SelectField(u'Country', choices=CountryList)
    CITY = SelectField(u'City', choices=CityList)


class SearchFormFindFighters(FlaskForm):
    WEIGHT_CATEGORY = SelectField(u'Choose weight category *', choices=TupleWeightCatMen)
    COUNTRY = SelectField(u'Country', choices=TupleCountry)


class Events(FlaskForm):
    EVENT_NAME = StringField(u'Event name', validators=[InputRequired(), Length(min=3, max=50)], id='EVENTS_NAME')
    CONTINENT = SelectField(u'Continent', choices=TupleContinent)
    CITY = StringField(u'City', validators=[InputRequired(), Length(min=1, max=50)])
    COUNTRY = SelectField(u'Country', choices=TupleCountry)
    ZIP_CODE = StringField(u'Zip-code', validators=[InputRequired(), Length(min=1, max=7)])
    STREET = StringField(u'Street', validators=[InputRequired(), Length(min=1, max=45)])
    STREET_NUMBER = StringField(u'Street number', validators=[InputRequired(), Length(min=1, max=10)])
    EVENT_DATE = DateField('Event Date', format='%Y-%m-%d')
    TIME = TimeField(u'Event start time (use format: H:M) ', validators=[InputRequired()], format='%H:%M')
    NEED_FIGHTER_STATUS = SelectField(u"""Do You need fighters ? Your event will be visible for managers""",choices=[('YES','YES'),('NO','NO')])


FIGHTERS = []
json_lists = []


class FIGHTS(FlaskForm):
    # EVENT_NAME = StringField(u'Choose event name')
    # ID_FIGHTER_1 = StringField(u'ID number for first fighter')
    # ID_FIGHTER_2 = StringField(u'ID number for second fighter')
    WEIGHT_CATEGORY = SelectField(u'Weight category', choices=TupleWeightCatMen)
    TIME = StringField(u'Round time')
    AMOUNT_OF_ROUNDS = StringField(u'Amount of rounds')


class SearchEvent(FlaskForm):
    CONTINENT = SelectField(u'Continent', choices=TupleContinentSearch)
    COUNTRY = SelectField(u'Country', choices=TupleCountrySearch)
    WEIGHT_CATEGORY = SelectField(u'Weight category', choices=TupleWeightCatMenSearch)
    dt = DateField('Pick a Date', format="%m/%d/%Y")


class ShowEvent(FlaskForm):
    CONTINENT = SelectField(u'Continent', choices=TupleContinentSearch)
    COUNTRY = SelectField(u'Country', choices=TupleCountry)
    CITY = StringField(u'City')
    EVENT_STATUS = SelectField(u'Event status', choices=TupleEventStatus)


class ShowFederationEvent(FlaskForm):
    CONTINENT = SelectField(u'Continent', choices=TupleContinentSearch)
    COUNTRY = SelectField(u'Country', choices=TupleCountry)
    CITY = StringField(u'City')
    EVENT_STATUS = SelectField(u'Event status', choices=TupleEventStatus)


class test120(FlaskForm):
    CONTINENT = SelectField(u'Continent', choices=TupleContinentSearch)
    COUNTRY = SelectField(u'Country', choices=TupleCountrySearch)
    CITY = StringField(u'City')
    EVENT_STATUS = SelectField(u'Event status', choices=TupleEventStatusSearch)


class SearchFighter(FlaskForm):
    CONTINENT = SelectField(u'Continent', choices=TupleContinentSearch)
    COUNTRY = SelectField(u'Country', choices=TupleCountrySearch)
    CITY = StringField(u'City')
    FREE_AGENT = SelectField(u'Free agent', choices=[('No', """No"""),
                                                                  ('Yes', 'Yes')])
    NEED_MANAGER = SelectField(u'Need manager status *', choices=[('No', 'Fighters which dont need managers'),
                                                                  ('Yes', 'Fighters which need managers'),
                                                                  ('Both', 'Both groups')])
    WEIGHT_CATEGORY = SelectField(u'Choose Your weight category *', choices=TupleWeightCatMenSearch)
    NUMBER_OF_FIGHTS = StringField(
        u'Point minimal number of fights which fighter should have (combine wins and losses)')
    FIGHT_STYLE = SelectField(u'What kind of fight do You prefer?', choices=TuplePreferFightStyleSearch)
    # AGE = StringField(u'Fighter should be not older')
    FIGHT_STATUS = SelectField(u'Fight status', choices=TupleFightStatus)
    HEALTH_STATUS = SelectField(u'Health status', choices=TupleHealthCondition)


class FightRequest(FlaskForm):
    ID_FIGHTER = StringField(u'ID_FIGHTER')
    CONTINENT = SelectField(u'Continent', choices=TupleContinent)
    COUNTRY = SelectField(u'Country', choices=TupleCountry)
    CITY = StringField(u'City')


class AddFighter(FlaskForm):
    ID_FIGHTER = StringField(u'ID_Fighter')
    TEXT = TextAreaField('Your job offer (payment,conditions etc) (max.400 characters)')


class CheckTeam(FlaskForm):
    FIGHT_STATUS = SelectField(u'Fight status', choices=TupleFightStatus)
    HEALTH_STATUS = SelectField(u'Health status', choices=TupleHealthCondition)

def CurrentAccountType (user):
    q = USER.query.filter_by(USERNAME=user).first()
    account_type = q.ACCOUNT_TYPE
    print("""[def CurrentAccountType] current user account type is: """+str(account_type))
    return account_type

@login_manager.user_loader
def load_user(user_id):
    return USER.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/UploadImages')
def UploadImages():
    return render_template('UploadImages.html')


@app.route('/uploadImages', methods=['POST'])
def uploadImages():
    name = current_user.USERNAME
    file = request.files['inputFile']
    newFile = IMAGES(
        NAME=file.filename,
        USERNAME=name,
        DATA=file.read()
    )
    db.session.add(newFile)
    db.session.commit()

    return 'Saved ' + file.filename + 'to the database !'


# jQuery/AJAX Automatyczne uzupelnianie listy (Search_by_FGSN_FGPN)
@app.route('/autocompleteEvent', methods=['GET'])
def autocompleteEvent():
    print('jsjon test')
    today = time.strftime("%m/%d/%Y")
    json_list = []
    name = current_user.USERNAME
    q = USER.query.filter_by(USERNAME=name).first()
    ID_FEDERATION = q.FEDERATION.ID_FEDERATION

    q = EVENTS.query.filter_by(ID_FEDERATION=ID_FEDERATION).all()
    for i in q:
        if i.DATE >= today:
            json_list.append(i.EVENT_NAME)
        else:
            continue
    print(json_list)
    return jsonify(json_list=json_list)


def AutocompleteFighters():
    name = current_user.USERNAME
    q = USER.query.filter_by(USERNAME=name).first()
    id_federation = q.FEDERATION.ID_FEDERATION
    # list1=[]
    # list = ['Strawweight','Bantamweight','Featherweight','Welterweight','Middleweight','Light heavyweight','Heavyweight']
    F5 = db.engine.execute("""SELECT ff.ID_FIGHTER,f.NAME,f.SURNAME,f.NICKNAME,fd.WEIGHT_CATEGORY FROM FIGHTER_FEDERATION ff
    INNER JOIN FIGHTER f ON ff.ID_FIGHTER=f.ID_FIGHTER
    INNER JOIN FIGHTER_DETAILS fd ON f.ID_FIGHTER=fd.ID_FIGHTER
    WHERE ff.ID_FEDERATION='""" + str(id_federation) + """'""")
    FighterList = [[i.ID_FIGHTER, i.NAME, i.SURNAME, i.NICKNAME, i.WEIGHT_CATEGORY] for i in F5]
    FighterList.append(['', 'TBA', '', '', 'Strawweight'])
    FighterList.append(['', 'TBA', '', '', 'Bantamweight'])
    FighterList.append(['', 'TBA', '', '', 'Featherweight'])
    FighterList.append(['', 'TBA', '', '', 'Welterweight'])
    FighterList.append(['', 'TBA', '', '', 'Middleweight'])
    FighterList.append(['', 'TBA', '', '', 'Light Heavyweight'])
    FighterList.append(['', 'TBA', '', '', 'Heavyweight'])
    print(FighterList)

    # list1=[( """{WeightCategory: '""" + str(i[4]) +"'," + 'Fighter: ' + "'" +str(i[1])+" "+str(i[3])+" "+str(i[2])+" "+"(ID:"+str(i[0])+""")',"""+ 'Fighter2: ' + "'" +str(i[1])+" "+str(i[3])+" "+str(i[2])+" "+"(ID:"+str(i[0])+""")'},""") for i in FighterList]

    list1 = [("""{WeightCategory: '""" + str(i[4]) + "'," + 'Fighter: ' + "'" + str(i[1]) + " " + str(i[3]) + " " + str(
        i[2]) + """',""" + 'Fighter2: ' + "'" + str(i[1]) + " " + str(i[3]) + " " + str(
        i[2]) + """'},""") for i in FighterList]
    s = ""

    list1 = sorted(list1)
    list1 = s.join(list1)
    list1 = list1[:-1]

    print(list1)
    return list1

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = USER.query.filter_by(USERNAME=form.USERNAME.data).first()
        if user:
            if check_password_hash(user.PASSWORD, form.PASSWORD.data):
                login_user(user, remember=form.REMEMBER.data)
                check_account_type = user.ACCOUNT_TYPE
                print(check_account_type)
                return redirect(url_for('dashboard'))
                # if check_account_type == "Federation":
                #     print('User ' + str(current_user.USERNAME) + ' has been logged in.')
                #     return redirect(url_for('dashboardfederation'))
                # elif check_account_type == "Standard urder":
                #     print('User ' + str(current_user.USERNAME) + ' has been logged in.')
                #     return redirect(url_for('dashboardfederation'))
                # elif check_account_type == "Fighter":
                #     print('User ' + str(current_user.USERNAME) + ' has been logged in.')
                #     return redirect(url_for('dashboardfighter'))
                # elif check_account_type == "Manager":
                #     print('User ' + str(current_user.USERNAME) + ' has been logged in.')
                #     return redirect(url_for('dashboardmanager'))

        return '<h1>Invalid username or password</h1>'
        # return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    CREATE_DATE = time.strftime("%d/%m/%Y")
    CREATE_TIME = time.strftime("%X")

    form = RegisterForm()
    USERNAME = form.USERNAME.data

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.PASSWORD.data, method='sha256')
        new_user = USER(
            USERNAME=form.USERNAME.data,
            EMAIL=form.EMAIL.data,
            PASSWORD=hashed_password,
            ACCOUNT_TYPE=form.ACCOUNT_TYPE.data,
            CREATION_DATE=CREATE_DATE,
            CREATE_TIME=CREATE_TIME)
        db.session.add(new_user)
        db.session.commit()
        print("New user has been added")

        return render_template('signup.html', form=form,
                               message=USERNAME + ' your account has been created successfully !')
        # return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)


# @app.route('/dashboardfederation')
# @login_required
# def dashboardfederation():
#     return render_template('dashboardfederation.html', current_user=current_user.USERNAME,FEDERATIONS_LIST=FEDERATIONS_LIST, MANAGERS_LIST=MANAGERS_LIST)
#
#
# @app.route('/dashboardfighter')
# @login_required
# def dashboardfighter():
#     return render_template('dashboardfighter.html', current_user=current_user.USERNAME,FEDERATIONS_LIST=FEDERATIONS_LIST, MANAGERS_LIST=MANAGERS_LIST)
#
#
# @app.route('/dashboardmanager')
# @login_required
# def dashboardmanager():
#     return render_template('dashboardmanager.html', current_user=current_user.USERNAME,FEDERATIONS_LIST=FEDERATIONS_LIST, MANAGERS_LIST=MANAGERS_LIST)


@app.route('/dashboard')
@login_required
def dashboard():
    UserAccountType=CurrentAccountType(current_user.USERNAME)
    return render_template('dashboard.html', UserAccountType=UserAccountType)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/FindFighters', methods=['GET', 'POST'])
@login_required
def FindFighters():
    UserAccountType = CurrentAccountType(current_user.USERNAME)
    form = SearchFighter()
    continent = form.CONTINENT.data,
    country = form.COUNTRY.data,
    city = form.CITY.data,
    weight_category = form.WEIGHT_CATEGORY.data,
    number_of_fights = form.NUMBER_OF_FIGHTS.data,
    need_manager = form.NEED_MANAGER.data,
    free_agent = form.FREE_AGENT.data,
    fight_style = form.FIGHT_STYLE.data,

    health_status = form.HEALTH_STATUS.data,
    fight_status = form.FIGHT_STATUS.data
    today = time.strftime("%d/%m/%Y")

    account=CurrentAccountType(current_user.USERNAME)

    if request.method == 'POST':
        if account=='Manager':
            if len(country[0]) == 0:
                country = ('%')
            if len(city[0]) == 0:
                city = ('%')
            if len(number_of_fights[0]) == 0:
                number_of_fights = ('0')
            if len(fight_status[0]) == 0:
                fight_status = ('%')
            if len(health_status[0]) == 0:
                health_status = ('%')
            if need_manager == 'Both':
                need_manager = """Yes','No"""
            F5 = db.engine.execute("""
            SELECT f.ID_FIGHTER,f.NAME,f.SURNAME,f.NICKNAME,
            CASE WHEN fd.WEIGHT_CATEGORY='' THEN '%' ELSE fd.WEIGHT_CATEGORY END
                ,fd.WEIGHT,fd.HEIGHT,fd.HEALTH_STATUS,fd.READY_TO_FIGHT_DATE,fd.FIGHT_STATUS,
            CASE WHEN fd.FIGHT_STYLE='' THEN '%' ELSE fd.FIGHT_STYLE END
                ,fd.NUMBER_OF_WINS,fd.NUMBER_OF_LOSS,a.CONTINENT,a.COUNTRY,a.CITY
            FROM FIGHTER f
            INNER JOIN FIGHTER_DETAILS fd ON f.ID_FIGHTER=fd.ID_FIGHTER
            INNER JOIN ADDRESS a ON a.ID_FIGHTER=f.ID_FIGHTER
                WHERE fd.WEIGHT_CATEGORY like """ + "'" + weight_category[0] + "'" + """
                AND fd.FIGHT_STYLE like """ + "'" + str(fight_style[0]) + "'" + """
                AND a.CONTINENT like """ + "'" + str(continent[0]) + "'" + """
                AND a.COUNTRY like """ + "'" + str(country[0]) + "'" + """
                AND a.CITY like """ + "'" + str(city[0]) + "'" + """
                AND fd.MANAGER_NEED in""" + "('" + need_manager[0] + "')" + """
                AND fd.NUMBER_OF_WINS >= """ + number_of_fights[0] + """
                AND fd.FIGHT_STATUS like""" + "'" + str(fight_status) + "'" + """
                AND fd.HEALTH_STATUS like""" + "'" + str(health_status[0]) + "' ORDER BY fd.WEIGHT_CATEGORY,fd.READY_TO_FIGHT_DATE"
                                   )
            list = [i for i in F5]
            print(list)
        elif account == 'Federation':
            print('Lecim z federacja')
            print("weight_category  "+str(weight_category[0]))
            print("fight style "+str(fight_style[0]))
            print("continent "+str(continent[0]))
            print("country "+str(country[0]))

            print("need manager "+need_manager[0])
            print("number of fights "+number_of_fights[0])
            print("fight status "+str(fight_status))
            print("health status "+str(health_status[0]))

            if len(country[0]) == 0:
                country = ('%')
            if len(city[0]) == 0:
                city = ('%')
            if len(number_of_fights[0]) == 0:
                number_of_fights = ('0')
            if len(fight_status[0]) == 0:
                fight_status = ('%')
            if len(health_status[0]) == 0:
                health_status = ('%')
            # if need_manager == 'Both':
            #     need_job = """Yes','No"""
            print("city " + str(city[0]))
            F5 = db.engine.execute("""
            SELECT f.ID_FIGHTER,f.NAME,f.SURNAME,f.NICKNAME,
            CASE WHEN fd.WEIGHT_CATEGORY='' THEN '%' ELSE fd.WEIGHT_CATEGORY END
                ,fd.WEIGHT,fd.HEIGHT,fd.HEALTH_STATUS,fd.READY_TO_FIGHT_DATE,fd.FIGHT_STATUS,
            CASE WHEN fd.FIGHT_STYLE='' THEN '%' ELSE fd.FIGHT_STYLE END
                ,fd.NUMBER_OF_WINS,fd.NUMBER_OF_LOSS,a.CONTINENT,a.COUNTRY,a.CITY
            FROM FIGHTER f
            INNER JOIN FIGHTER_DETAILS fd ON f.ID_FIGHTER=fd.ID_FIGHTER
            INNER JOIN ADDRESS a ON a.ID_FIGHTER=f.ID_FIGHTER
                WHERE fd.WEIGHT_CATEGORY like """ + "'" + weight_category[0] + "'" + """
                AND fd.FIGHT_STYLE like """ + "'" + str(fight_style[0]) + "'" + """
                AND a.CONTINENT like """ + "'" + str(continent[0]) + "'" + """
                AND a.COUNTRY like """ + "'" + str(country[0]) + "'" + """
                AND a.CITY like """ + "'" + str(city[0]) + "'" + """
                AND fd.FREE_AGENT in""" + "('" + free_agent[0] + "')" + """
                AND fd.NUMBER_OF_WINS >= """ + number_of_fights[0] + """
                AND fd.FIGHT_STATUS like""" + "'" + str(fight_status) + "'" + """
                AND fd.HEALTH_STATUS like""" + "'" + str(health_status[0]) + "' ORDER BY fd.WEIGHT_CATEGORY,fd.READY_TO_FIGHT_DATE"
                                   )
            list = [i for i in F5]
            print(list)

        return render_template('FindFighters.html', form=form, data=list,UserAccountType=UserAccountType)
    return render_template('FindFighters.html', form=form,UserAccountType=UserAccountType)


@app.route('/CreateFighterProfile', methods=['GET', 'POST'])
@login_required
def CreateFighterProfile():
    UserAccountType = CurrentAccountType(current_user.USERNAME)
    CREATE_DATE = time.strftime("%d/%m/%Y")
    CREATE_TIME = time.strftime("%X")

    form = FighterAccountForm()

    name = current_user.USERNAME
    query = USER.query.filter_by(USERNAME=name).first()

    if form.validate_on_submit():
        add_fighter = FIGHTER(
            NAME=form.NAME.data,
            SURNAME=form.SURNAME.data,
            NICKNAME=form.NICKNAME.data,
            CREATION_DATE=CREATE_DATE,
            CREATE_TIME=CREATE_TIME,
            USER_id=query.id)
        db.session.add(add_fighter)
        db.session.commit()

        NAME_ID = form.NAME.data
        query = FIGHTER.query.filter_by(NAME=NAME_ID).first()
        print(query.ID_FIGHTER)

        add_address = ADDRESS(
            COUNTRY=form.COUNTRY.data,
            CONTINENT=form.CONTINENT.data,
            CITY=form.CITY.data,
            ZIP_CODE=form.ZIP_CODE.data,
            STREET=form.STREET.data,
            STREET_NUMBER=form.STREET_NUMBER.data,
            ID_FIGHTER=query.ID_FIGHTER)
        db.session.add(add_address)
        db.session.commit()

        add_contact = CONTACT(
            PHONE_NUMBER=form.PHONE_NUMBER.data,
            PHONE_NUMBER2=form.PHONE_NUMBER2.data,
            ID_FIGHTER=query.ID_FIGHTER)
        db.session.add(add_contact)
        db.session.commit()

        add_fighter_details = FIGHTER_DETAILS(
            SPORT=form.SPORT.data,
            WEIGHT_CATEGORY=form.WEIGHT_CATEGORY.data,
            WEIGHT=form.WEIGHT.data,
            HEIGHT=form.HEIGHT.data,
            FIGHT_STATUS=form.FIGHT_STATUS.data,
            FIGHT_STYLE=form.FIGHT_STYLE.data,
            NUMBER_OF_WINS=form.NUMBER_OF_WINS.data,
            NUMBER_OF_LOSS=form.NUMBER_OF_LOSS.data,
            ID_FIGHTER=query.ID_FIGHTER,
            URL=form.URL.data,
            FREE_AGENT=form.FREE_AGENT.data)
        db.session.add(add_fighter_details)
        db.session.commit()

        return render_template('CreateFighterProfile.html', form=form,
                               message=current_user.USERNAME + ' You have just created Your own profile')

    return render_template('CreateFighterProfile.html', form=form, FIGHTERS_LIST=FIGHTERS_LIST,
                           FEDERATIONS_LIST=FEDERATIONS_LIST, MANAGERS_LIST=MANAGERS_LIST,UserAccountType=UserAccountType)


@app.route('/CreateFederationProfile', methods=['GET', 'POST'])
@login_required
def CreateFederationProfile():
    UserAccountType = CurrentAccountType(current_user.USERNAME)
    CREATE_DATE = time.strftime("%d/%m/%Y")
    CREATE_TIME = time.strftime("%X")

    form = FederationAccountForm()

    name = current_user.USERNAME
    query = USER.query.filter_by(USERNAME=name).first()

    form = FederationAccountForm()
    if form.validate_on_submit():
        add_federation = FEDERATION(
            NAME=form.NAME.data,
            SURNAME=form.SURNAME.data,
            FEDERATION_NAME=form.FEDERATION_NAME.data,
            FEDERATION_CREATED_DATE=form.FEDERATION_CREATED_DATE.data,
            CREATION_DATE=CREATE_DATE,
            CREATE_TIME=CREATE_TIME,
            USER_id=query.id)
        db.session.add(add_federation)
        db.session.commit()

        NAME_ID = form.NAME.data
        query = FEDERATION.query.filter_by(NAME=NAME_ID).first()
        # ID_FEDERATION=query.ID_FEDERATION
        # print('To jest id federacji: '+str(ID_FEDERATION))
        # query = FEDERATION.query.filter_by(ID_FEDERATION=ID_FEDERATION).all()

        add_address = ADDRESS(
            COUNTRY=form.COUNTRY.data,
            CONTINENT=form.CONTINENT.data,
            CITY=form.CITY.data,
            ZIP_CODE=form.ZIP_CODE.data,
            STREET=form.STREET.data,
            STREET_NUMBER=form.STREET_NUMBER.data,
            ID_FEDERATION=query.ID_FEDERATION)
        db.session.add(add_address)
        db.session.commit()

        add_contact = CONTACT(
            PHONE_NUMBER=form.PHONE_NUMBER.data,
            PHONE_NUMBER2=form.PHONE_NUMBER2.data,
            ID_FEDERATION=query.ID_FEDERATION)
        db.session.add(add_contact)
        db.session.commit()

        return render_template('CreateFederationProfile.html', form=form,
                               message=current_user.USERNAME + ' You have just created Your own profile', UserAccountType=UserAccountType)

    return render_template('CreateFederationProfile.html', form=form, UserAccountType=UserAccountType)


@app.route('/CreateManagerProfile', methods=['GET', 'POST'])
@login_required
def CreateManagerProfile():
    UserAccountType = CurrentAccountType(current_user.USERNAME)
    CREATE_DATE = time.strftime("%d/%m/%Y")
    CREATE_TIME = time.strftime("%X")

    form = ManagerAccountForm()

    name = current_user.USERNAME
    query = USER.query.filter_by(USERNAME=name).first()

    if form.validate_on_submit():
        add_manager = MANAGER(
            NAME=form.NAME.data,
            SURNAME=form.SURNAME.data,
            CREATION_DATE=CREATE_DATE,
            SPORT=form.SPORT_NAME.data,
            CREATE_TIME=CREATE_TIME,
            USER_id=query.id)
        db.session.add(add_manager)
        db.session.commit()

        NAME_ID = form.NAME.data
        query = MANAGER.query.filter_by(NAME=NAME_ID).first()
        print(query.ID_MANAGER)

        add_address = ADDRESS(
            COUNTRY=form.COUNTRY.data,
            CONTINENT=form.CONTINENT.data,
            CITY=form.CITY.data,
            ZIP_CODE=form.ZIP_CODE.data,
            STREET=form.STREET.data,
            STREET_NUMBER=form.STREET_NUMBER.data,
            ID_MANAGER=query.ID_MANAGER)
        db.session.add(add_address)
        db.session.commit()

        add_contact = CONTACT(
            PHONE_NUMBER=form.PHONE_NUMBER.data,
            PHONE_NUMBER2=form.PHONE_NUMBER2.data,
            ID_MANAGER=query.ID_MANAGER)
        db.session.add(add_contact)
        db.session.commit()

        return render_template('CreateManagerProfile.html', form=form,
                               message=current_user.USERNAME + ' You have just created Your own profile',UserAccountType=UserAccountType)

    return render_template('CreateManagerProfile.html', form=form,UserAccountType=UserAccountType)


@app.route('/FighterFights', methods=['GET', 'POST'])
@login_required
def FighterFights():
    UserAccountType = CurrentAccountType(current_user.USERNAME)
    query1 = USER.query.filter_by(USERNAME=current_user.USERNAME).first()
    User_id = query1.id
    query2 = FIGHTER.query.filter_by(USER_id=User_id).first()
    id_fighter = query2.ID_FIGHTER
    query3 = FIGHT.query.filter_by(FIGHTER_1=id_fighter).all()
    data = [i.ID_EVENT for i in query3]

    return render_template('CreateManagerProfile.html', data=data,UserAccountType=UserAccountType)

@app.route('/CreateEvents', methods=['GET', 'POST'])
@login_required
def CreateEvents():
    form = Events()
    UserAccountType = CurrentAccountType(current_user.USERNAME)
    name = current_user.USERNAME
    print('Federation name: ' + str(name))
    query = USER.query.filter_by(USERNAME=name).first()
    id_federation = query.FEDERATION.ID_FEDERATION
    print('ID_FEDERATION: ' + str(id_federation))

    # if form.validate_on_submit():
    if request.method == 'POST':

        CREATE_DATE = time.strftime("%d/%m/%Y")
        CREATE_TIME = time.strftime("%X")
        add_event = EVENTS(
            EVENT_NAME=form.EVENT_NAME.data,
            NEED_FIGHTER_STATUS=form.NEED_FIGHTER_STATUS.data,
            COUNTRY=form.COUNTRY.data,
            CONTINENT=form.CONTINENT.data,
            CITY=form.CITY.data,
            ZIP_CODE=form.ZIP_CODE.data,
            STREET=form.STREET.data,
            STREET_NUMBER=form.STREET_NUMBER.data,
            DATE=form.EVENT_DATE.data,
            TIME=form.TIME.data,
            ID_FEDERATION=id_federation,
            CREATION_DATE=CREATE_DATE,
            RECORD_UPDATED=0,
            CREATION_TIME=CREATE_TIME,
            EVENT_STATUS='NEW')
        db.session.add(add_event)
        db.session.commit()
        print('Event: ' + str(form.EVENT_NAME.data) + ' has been created.')
        return render_template('CreateEvents.html', form=form,
                               message=current_user.USERNAME + ' You have just created Your own profile', UserAccountType=UserAccountType)

    return render_template('CreateEvents.html', form=form, UserAccountType=UserAccountType)


@app.route('/CreateFights', methods=['GET', 'POST'])
@login_required
def CreateFights():
    UserAccountType = CurrentAccountType(current_user.USERNAME)
    form = FIGHTS()
    today = time.strftime("%Y-%m-%d")
    print('printujemy today')
    print(today)

    event_list = []
    name = current_user.USERNAME
    q = USER.query.filter_by(USERNAME=name).first()
    ID_FEDERATION = q.FEDERATION.ID_FEDERATION
    q = EVENTS.query.filter_by(ID_FEDERATION=ID_FEDERATION).all()
    for i in q:
        if str(i.DATE) >= today:
            event_list.append(i.EVENT_NAME)
        else:
            print("Stary event: '" + str(i.EVENT_NAME) + "' a jego ID to: " + str(i.ID_EVENT))
            continue
    print('a tu mamy liste eventow :D ')
    print(event_list)

    data = AutocompleteFighters()

    if request.method == 'POST':
        event_name = request.form['eventlist']
        ID_FIGHTER_1 = request.form['Fighter'].rstrip()
        ID_FIGHTER_2 = request.form['Fighter2'].rstrip()
        Time = request.form['time']
        Rounds = request.form['rounds']
        WEIGHT_CATEGORY = request.form['WeightCategory']

        if ID_FIGHTER_1 == 'TBA' and ID_FIGHTER_2 == 'TBA':
            return render_template('CreateFights.html',
                                   message='To crate the fight You need to add at least one fighter.', data=event_list,
                                   data2=data, form=form)
        elif ID_FIGHTER_1 == ID_FIGHTER_2:
            return render_template('CreateFights.html',
                                   message='You cannot add the same fighter to one fight.', data=event_list, data2=data,
                                   form=form)
        elif ID_FIGHTER_1 == 'TBA':
            ID_FIGHTER_1 = 110
        elif ID_FIGHTER_2 == 'TBA':
            ID_FIGHTER_2 = 110

        print("Event name: " + str(event_name))
        print("""ID FIGHTER_1 """ + str(ID_FIGHTER_1))
        print("""ID FIGHTER_2 """ + str(ID_FIGHTER_2))
        print("Time: " + str(Time))
        print("Rounds: " + str(Rounds))
        print('Weight category: ' + str(WEIGHT_CATEGORY))

        q3 = EVENTS.query.filter_by(EVENT_NAME=event_name, ID_FEDERATION=ID_FEDERATION).first()
        print(event_name)
        ID_EVENT = q3.ID_EVENT
        print('ID_EVENT: ' + str(ID_EVENT))

        CREATE_TIME = time.strftime("%X")
        CREATE_DATE = time.strftime("%d/%m/%Y")

        add_fight = FIGHT(
            WEIGHT_CATEGORY=WEIGHT_CATEGORY,
            FEDERATION_ID=ID_FEDERATION,
            CREATION_DATE=CREATE_DATE,
            ID_EVENT=ID_EVENT,
            FIGHT_STATUS='NEW',
            CREATE_TIME=CREATE_TIME)
        db.session.add(add_fight)
        db.session.commit()
        print('Fight has been added')

        F5 = db.engine.execute(
            """SELECT ID_FIGHT FROM FIGHT WHERE WEIGHT_CATEGORY='""" + WEIGHT_CATEGORY + "'" +
            """ AND FEDERATION_ID='""" + str(ID_FEDERATION) + "'" +
            """ AND CREATION_DATE='""" + str(CREATE_DATE) + "'" +
            """ AND CREATE_TIME='""" + str(CREATE_TIME) + "'")
        id_fight = [i.ID_FIGHT for i in F5]
        try:
            id_fight = id_fight[0][0]
            print('ID Fight: ' + str(id_fight[0]))
        except:
            print('ID Fight: ' + str(id_fight[0]))
            id_fight = id_fight[0]

        # Musimy podzielic string z imieniem,nicknamem i nazwiskiem fightera na czesci i poszukac dla niego ID_FIGHTER
        # Problem stanowia zawodnicy z nickami skladajacymi sie z dwoch lub wiecej slow.
        if ID_FIGHTER_1 != 110:
            split_id_fighter_1 = ID_FIGHTER_1.split(' ')
            m1 = FIGHTER.query.filter_by(NAME=split_id_fighter_1[0], NICKNAME=split_id_fighter_1[1],SURNAME=split_id_fighter_1[2]).first()
            ID_FIGHTER_1 = m1.ID_FIGHTER
        if ID_FIGHTER_2 != 110:
            split_id_fighter_2 = ID_FIGHTER_2.split(' ')
            # zeby przetestowac problem z zawodnikami kliknij tu
            # print(split_id_fighter_2)
            m2 = FIGHTER.query.filter_by(NAME=split_id_fighter_2[0], NICKNAME=split_id_fighter_2[1],
                                         SURNAME=split_id_fighter_2[2]).first()
            ID_FIGHTER_2 = m2.ID_FIGHTER

        m = FIGHT.query.filter_by(ID_FIGHT=id_fight).first()
        f1 = FIGHTER.query.filter_by(ID_FIGHTER=ID_FIGHTER_1).first()
        f2 = FIGHTER.query.filter_by(ID_FIGHTER=ID_FIGHTER_2).first()
        m.FIGHTER_FIGHT.append(f1)
        db.session.commit()
        m.FIGHTER_FIGHT.append(f2)
        db.session.commit()

        if ID_FIGHTER_1 !=110:
            q=FIGHTER_DETAILS.query.filter_by(ID_FIGHTER=str(ID_FIGHTER_1)).first()
            q.FIGHT_STATUS='No fight'
            db.session.commit()
        if ID_FIGHTER_2 !=110:
            q = FIGHTER_DETAILS.query.filter_by(ID_FIGHTER=str(ID_FIGHTER_2)).first()
            q.FIGHT_STATUS = 'No fight'
            db.session.commit()

        print(ID_FIGHTER_1)
        print(ID_FIGHTER_2)
        if ID_FIGHTER_1 == 110 or ID_FIGHTER_2 == 110:
            print("""Let's check fights requests""")
            # [Sprawdzmy czy stworzona walka ma wolne miejsce na figtera, a nastepnie odpytujemy kolumne FIGHT_REQUEST]
            F5 = db.engine.execute("""SELECT ID_REQUEST from FIGHT_REQUEST WHERE
            WEIGHT_CATEGORY ='""" + form.WEIGHT_CATEGORY.data + "'" + """ AND 
            CONTINENT LIKE '""" + q3.CONTINENT + "'")
            id_request = [i for i in F5]
            print('id_request')
            id_req_list = [i[0] for i in id_request]
            print(id_req_list)

            try:
                if len(id_req_list) > 1:
                    msg = mail.send_message(
                        'Fight request offer',
                        sender='wlapie40@gmail.com',
                        recipients=['wlapie40@gmail.com'],
                        html=
                        """<p>Hi """ + str(name) + """</p>"""
                                                   """<p>We have some fighters which can be use in <strong>ID Fight: """ + str(
                            id_fight) + """</strong> (event name: <strong>""" + str(event_name) + """</strong> )</p>"""
                                                                                                  """<p>Fighters table:</p>
                                                                                                  <table>
                                                                                                  <tbody>
                                                                                                  <tr>
                                                                                                  <td>Name</td>
                                                                                                  <td>Surname</td>
                                                                                                  <td>Nickname</td>
                                                                                                  <td>Category weight</td>
                                                                                                  <td>Continent</td>
                                                                                                  <td>Country</td>
                                                                                                  <td>City</td>
                                                                                                  <td>Number of wins</td>
                                                                                                  <td>Number od loss</td>
                                                                                                  <td>Fight style</td>
                                                                                                  <td>Health status</td>
                                                                                                  <td>Ready to fight date</td>
                                                                                                  </tr>
                                                                                                  </tbody>
                                                                                                  </table>
                                                                                                  <p>Best regards</p>""")
            except Exception as e:
                print("""I cannot send an email""" + str(e))
        # return render_template('CreateFights.html', message='Fight has been added', form=form)
            redirect(url_for('CreateFights'))
    return render_template('CreateFights.html', data=event_list, data2=data, form=form, UserAccountType=UserAccountType)


@app.route('/SearchEvents', methods=['GET', 'POST'])
@login_required
def searchevents():
    UserAccountType = CurrentAccountType(current_user.USERNAME)
    form = SearchEvent()
    continent = form.CONTINENT.data
    country = form.COUNTRY.data
    weight_category = form.WEIGHT_CATEGORY.data
    date_ev = form.dt.data

    name = current_user.USERNAME
    query = USER.query.filter_by(USERNAME=name).first()
    id_manager = query.MANAGER.ID_MANAGER

    F5 = db.engine.execute("""SELECT ID_FIGHTER FROM FIGHTER_MANAGER WHERE ID_MANAGER='""" + str(id_manager) + "'")
    fighter_list = [i[0] for i in F5]
    print('Manager fighter_list')
    print(fighter_list)

    # zeby moc przerobic na string musimy zmapowac liste z integerami w innym przypadku dostaniemy na twarz error :(
    map_fighter_list = map(str, fighter_list)
    str_fight_list = ','.join(map_fighter_list)
    # print(str_fight_list)


    F5 = db.engine.execute(
        """SELECT fed.FEDERATION_NAME,even.EVENT_NAME,even.CONTINENT,even.COUNTRY,even.CITY,even.DATE,WEIGHT_CATEGORY,ff.ID_FIGHTER,f.ID_FIGHT FROM FEDERATION fed
        INNER JOIN EVENTS even ON even.ID_FEDERATION=fed.ID_FEDERATION
        INNER JOIN FIGHT f ON f.ID_EVENT=even.ID_EVENT
        INNER JOIN FIGHTER_FIGHTS ff ON ff.ID_FIGHT=f.ID_FIGHT
        ORDER BY f.ID_FIGHT DESC""")
    # list=[i for i in F5]
    list = [[i.FEDERATION_NAME, i.EVENT_NAME, i.CONTINENT, i.COUNTRY, i.CITY, i.DATE, i.WEIGHT_CATEGORY, i.ID_FIGHTER,
             i.ID_FIGHT] for i in F5]
    print('Events list')
    print(list)

    event_list = []
    r1 = 0
    r2 = 0

    # Wywalamy fighterow ktorych manager posiada
    for i in list:
        if r1 == 0:
            r1 = i
            print("r1")
            print(r1)
        elif r2 == 0:
            r2 = i
            print("r2")
            print(r2)
            if r1[7] in fighter_list:
                print("r1 in fighter_list")
                r1 = 0
                r2 = 0
            elif r2[7] in fighter_list:
                print("r2 in fighter_list")
                r1 = 0
                r2 = 0
            elif r1[7] == 110:
                print("""Let's test r2""")
                if r2[7] not in fighter_list:
                    print("""r2 spelnil warunek""")
                    event_list.append(r2)
                    r1 = 0
                    r2 = 0
                else:
                    event_list.append(r1)
                    r1 = 0
                    r2 = 0
            elif r1[7] not in fighter_list and r1[7] != 110:
                event_list.append(r1)
                r1 = 0
                r2 = 0
    print("event_list")
    print(event_list)

    # r=0
    # event_list=[]
    # for i in list:
    #     if r == 0:
    #         y = i[7]
    #         r += 1
    #     elif r == 1:
    #         y2 = i[7]
    #         r = 0
    #         if y == 110:
    #             print("y")
    #             print(i)
    #             event_list.append(i)
    #         elif y2 == 110:
    #             print("y2")
    #             print(i)
    #             event_list.append(i)

    # id_event_list = [i[8] for i in event_list]
    # id_event_list=",".join(str(x) for x in id_event_list)
    # print('id_event_list')
    # print(id_event_list)

    # F5 = db.engine.execute(
    #     # """SELECT ID_FIGHTER FROM FIGHTER_FIGHTS WHERE ID_FIGHT IN ("""+id_event_list[0:]+""") AND ID_FIGHTER<>110""")
    # """SELECT ID_FIGHTER FROM FIGHTER_FIGHTS WHERE ID_FIGHT IN (""" + id_event_list[0:] + """)""")
    # opp_list = [''+str(i[0])+'' for i in F5]
    # print("""Oppontent's list""")
    # print(opp_list)
    #
    # r = 0
    # for i in event_list:
    #     i.append(int(opp_list[r]))
    #     r += 1
    #
    # print('final event list')
    # print(event_list)

    if request.method == 'POST':
        continent = form.CONTINENT.data
        print(continent)
        country = form.COUNTRY.data
        print(country)
        weight_category = form.WEIGHT_CATEGORY.data
        print(weight_category)
        date_ev = form.dt.data
        date_ev = str(date_ev)
        print(type(date_ev))
        date_ev = date_ev[8:10] + "/" + date_ev[5:7] + "/" + date_ev[0:4]
        print('dlugosc daty')
        print(len(date_ev))

        print('continent ' + continent)
        print('country ' + country)
        print('weight ' + weight_category)
        print('date ' + date_ev)
        # F5 = db.engine.execute(
        #                     'SELECT fed.FEDERATION_NAME,even.EVENT_NAME,even.CONTINENT,even.COUNTRY,even.CITY,even.DATE,fight.WEIGHT_CATEGORY,'
        #                     'CASE WHEN fight.ID_FIGHTER_1  =' + "'" + 'TBA' + "'" + 'THEN fight.ID_FIGHTER_2 '
        #                     ' WHEN fight.ID_FIGHTER_2  =' + "'" + 'TBA' + "'" + 'THEN fight.ID_FIGHTER_1 END '
        #                     'FROM FEDERATION fed '
        #                     'INNER JOIN EVENTS even ON fed.ID_FEDERATION=even.ID_FEDERATION '
        #                     'INNER JOIN FIGHT fight ON even.ID_EVENT=fight.ID_EVENT'
        #                     ' WHERE (fight.ID_FIGHTER_1 like ' + "'" + 'TBA' + "'" + 'or fight.ID_FIGHTER_2 like ' + "'" + 'TBA' + "'" + ') '
        #                     'AND (fight.ID_FIGHTER_1 <> ' + "'" + ' ' + "'" + ' AND fight.ID_FIGHTER_2 <> ' + "'" + ' ' + "'" + ') '
        #                     'AND (even.CONTINENT like' + "'" + continent + "'" + ' AND COUNTRY like' + "'" + country + "'" +
        #                     ' AND fight.WEIGHT_CATEGORY like' + "'" + weight_category + "'" + ') AND (even.DATE ='+"'"+date_ev+"')"
        #                       'ORDER BY even.DATE ASC,even.CONTINENT')

        # if continent != '%' and country=='%' and weight_category =='%' and  len(date_ev)==6:
        #     F5 = db.engine.execute(
        #         """SELECT fed.FEDERATION_NAME,even.EVENT_NAME,even.CONTINENT,even.COUNTRY,even.CITY,even.DATE,WEIGHT_CATEGORY,ff.ID_FIGHTER,f.ID_FIGHT FROM FEDERATION fed
        #         INNER JOIN EVENTS even ON even.ID_FEDERATION=fed.ID_FEDERATION
        #         INNER JOIN FIGHT f ON f.ID_EVENT=even.ID_EVENT
        #         INNER JOIN FIGHTER_FIGHTS ff ON ff.ID_FIGHT=f.ID_FIGHT
        #         WHERE even.CONTINENT='""" + continent + """' """ +
        #         """ORDER BY f.ID_FIGHT DESC""")
        #     list = [[i.FEDERATION_NAME, i.EVENT_NAME, i.CONTINENT, i.COUNTRY, i.CITY, i.DATE, i.WEIGHT_CATEGORY,
        #              i.ID_FIGHTER,
        #              i.ID_FIGHT] for i in F5]
        #     print('Events list')
        #     print(list)
        # elif continent !='%' and country !='%' and weight_category =='%' and  len(date_ev)==6:
        #     F5 = db.engine.execute(
        #         """SELECT fed.FEDERATION_NAME,even.EVENT_NAME,even.CONTINENT,even.COUNTRY,even.CITY,even.DATE,WEIGHT_CATEGORY,ff.ID_FIGHTER,f.ID_FIGHT FROM FEDERATION fed
        #         INNER JOIN EVENTS even ON even.ID_FEDERATION=fed.ID_FEDERATION
        #         INNER JOIN FIGHT f ON f.ID_EVENT=even.ID_EVENT
        #         INNER JOIN FIGHTER_FIGHTS ff ON ff.ID_FIGHT=f.ID_FIGHT
        #         WHERE even.CONTINENT='""" + continent + """' AND even.COUNTRY='""" +country+
        #         """' ORDER BY f.ID_FIGHT DESC""")
        #     list = [[i.FEDERATION_NAME, i.EVENT_NAME, i.CONTINENT, i.COUNTRY, i.CITY, i.DATE, i.WEIGHT_CATEGORY,
        #              i.ID_FIGHTER,
        #              i.ID_FIGHT] for i in F5]
        #     print('Events list')
        #     print(list)
        #
        # elif continent != '%' and country != '%' and weight_category !='%' and len(date_ev) == 6:
        #     F5 = db.engine.execute(
        #         """SELECT fed.FEDERATION_NAME,even.EVENT_NAME,even.CONTINENT,even.COUNTRY,even.CITY,even.DATE,WEIGHT_CATEGORY,ff.ID_FIGHTER,f.ID_FIGHT FROM FEDERATION fed
        #         INNER JOIN EVENTS even ON even.ID_FEDERATION=fed.ID_FEDERATION
        #         INNER JOIN FIGHT f ON f.ID_EVENT=even.ID_EVENT
        #         INNER JOIN FIGHTER_FIGHTS ff ON ff.ID_FIGHT=f.ID_FIGHT
        #         WHERE even.CONTINENT='""" + continent + """' AND even.COUNTRY='""" + country +
        #         """'  AND WEIGHT_CATEGORY='"""+weight_category+"""' ORDER BY f.ID_FIGHT DESC""")
        #     list = [[i.FEDERATION_NAME, i.EVENT_NAME, i.CONTINENT, i.COUNTRY, i.CITY, i.DATE, i.WEIGHT_CATEGORY,
        #              i.ID_FIGHTER,
        #              i.ID_FIGHT] for i in F5]
        #     print('Events list')
        #     print(list)

        if continent != '%' and country != '%' and weight_category != '%' and len(date_ev) == 6:
            F5 = db.engine.execute(
                """SELECT fed.FEDERATION_NAME,even.EVENT_NAME,even.CONTINENT,even.COUNTRY,even.CITY,even.DATE,WEIGHT_CATEGORY,ff.ID_FIGHTER,f.ID_FIGHT FROM FEDERATION fed
                INNER JOIN EVENTS even ON even.ID_FEDERATION=fed.ID_FEDERATION
                INNER JOIN FIGHT f ON f.ID_EVENT=even.ID_EVENT
                INNER JOIN FIGHTER_FIGHTS ff ON ff.ID_FIGHT=f.ID_FIGHT
                WHERE even.CONTINENT like '""" + continent + """%' AND even.COUNTRY like '""" + country +
                """%'  AND WEIGHT_CATEGORY like '""" + weight_category + """%' ORDER BY f.ID_FIGHT DESC""")
            list = [[i.FEDERATION_NAME, i.EVENT_NAME, i.CONTINENT, i.COUNTRY, i.CITY, i.DATE, i.WEIGHT_CATEGORY,
                     i.ID_FIGHTER,
                     i.ID_FIGHT] for i in F5]
            print('Events list')
            print(list)
        # bierzemy pod uwage takze date wydarzenia
        else:
            F5 = db.engine.execute(
                """SELECT fed.FEDERATION_NAME,even.EVENT_NAME,even.CONTINENT,even.COUNTRY,even.CITY,even.DATE,WEIGHT_CATEGORY,ff.ID_FIGHTER,f.ID_FIGHT FROM FEDERATION fed
                INNER JOIN EVENTS even ON even.ID_FEDERATION=fed.ID_FEDERATION
                INNER JOIN FIGHT f ON f.ID_EVENT=even.ID_EVENT
                INNER JOIN FIGHTER_FIGHTS ff ON ff.ID_FIGHT=f.ID_FIGHT
                WHERE even.CONTINENT like '""" + continent + """%' AND even.COUNTRY like '""" + country +
                """%'  AND WEIGHT_CATEGORY like '""" + weight_category + """%' AND even.DATE >= '""" + date_ev + """' ORDER BY f.ID_FIGHT DESC""")
            list = [[i.FEDERATION_NAME, i.EVENT_NAME, i.CONTINENT, i.COUNTRY, i.CITY, i.DATE, i.WEIGHT_CATEGORY,
                     i.ID_FIGHTER,
                     i.ID_FIGHT] for i in F5]
            print('Events list')
            print(list)

        event_list = []
        r1 = 0
        r2 = 0

        # Wywalamy fighterow ktorych manager posiada
        for i in list:
            if r1 == 0:
                r1 = i
                print("r1")
                print(r1)
            elif r2 == 0:
                r2 = i
                print("r2")
                print(r2)
                if r1[7] in fighter_list:
                    print("r1 in fighter_list")
                    r1 = 0
                    r2 = 0
                elif r2[7] in fighter_list:
                    print("r2 in fighter_list")
                    r1 = 0
                    r2 = 0
                elif r1[7] == 110:
                    print("""Let's test r2""")
                    if r2[7] not in fighter_list:
                        print("""r2 spelnil warunek""")
                        event_list.append(r2)
                        r1 = 0
                        r2 = 0
                    else:
                        event_list.append(r1)
                        r1 = 0
                        r2 = 0
                elif r1[7] not in fighter_list and r1[7] != 110:
                    event_list.append(r1)
                    r1 = 0
                    r2 = 0
        print("event_list")
        print(event_list)

        # list = [
        #     [i.FEDERATION_NAME, i.EVENT_NAME, i.CONTINENT, i.COUNTRY, i.CITY, i.DATE, i.WEIGHT_CATEGORY, i.ID_FIGHTER,
        #      i.ID_FIGHT] for i in F5]
        # print(list)
        # list=[i for i in F5]
        # print(list)
        #
        # r = 0
        # event_list = []
        # for i in list:
        #     if r == 0:
        #         y = i[7]
        #         r += 1
        #     elif r == 1:
        #         y2 = i[7]
        #         r = 0
        #         if y == 110:
        #             event_list.append(i)
        #         elif y2 == 110:
        #             event_list.append(i)
        #         print(event_list)
        # id_event_list = [i[8] for i in event_list]
        # id_event_list = ",".join(str(x) for x in id_event_list)
        # print('event_list')
        # print(event_list)
        #
        # F5 = db.engine.execute(
        #     """SELECT ID_FIGHTER FROM FIGHTER_FIGHTS WHERE ID_FIGHT IN (""" + id_event_list[
        #                                                                       0:] + """) AND ID_FIGHTER<>110""")
        # opp_list = ['' + str(i[0]) + '' for i in F5]
        # print("""Oppontent's list""")
        # print(opp_list)
        #
        # r = 0
        # for i in event_list:
        #     i.append(opp_list[r])
        #     r += 1
        # print('Final event list:')
        # print(event_list)

        return render_template('SearchEvents.html', form=form, data=event_list, UserAccountType=UserAccountType)
    return render_template('SearchEvents.html', form=form, data=event_list,UserAccountType=UserAccountType)


@app.route('/CreateFightManagerRequest', methods=['GET', 'POST'])
@login_required
def CreateFightManagerRequest():
    UserAccountType = CurrentAccountType(current_user.USERNAME)
    form = FightRequest()
    name = current_user.USERNAME

    r = db.engine.execute(
        'SELECT a.ID_FIGHTER, a.NAME, a.SURNAME, a.NICKNAME, b.WEIGHT_CATEGORY, b.SPORT, c.CONTINENT, c.COUNTRY, c.CITY, b.FIGHT_STYLE '
        'from FIGHTER a '
        'INNER JOIN FIGHTER_DETAILS b ON a.ID_FIGHTER=b.ID_FIGHTER '
        'INNER JOIN FIGHT_REQUEST c ON  c.ID_FIGHTER=a.ID_FIGHTER')
    list = [i for i in r]
    print(list)

    q = USER.query.filter_by(USERNAME=name).first()
    User_id = q.id
    q = USER.query.filter_by(id=User_id).first()
    ID_MANAGER = q.MANAGER.ID_MANAGER
    print('ID_MANAGER: ' + str(ID_MANAGER))

    q = db.engine.execute(
        'SELECT a.ID_FIGHTER, a.NAME, a.SURNAME, a.NICKNAME, b.WEIGHT_CATEGORY,b.FIGHT_STYLE,b.HEALTH_STATUS '
        'FROM FIGHTER a INNER JOIN FIGHTER_DETAILS b ON a.ID_FIGHTER=b.ID_FIGHTER INNER JOIN FIGHTER_MANAGER c ON c.ID_FIGHTER=a.ID_FIGHTER WHERE c.ID_MANAGER=' + "'" + str(
            ID_MANAGER) + "'")
    fighterlist = [i for i in q]
    print(fighterlist)

    if form.validate_on_submit():
        ID_FIGHTER = form.ID_FIGHTER.data
        print('ID_FIGHTER: ' + ID_FIGHTER)
        q = FIGHTER_DETAILS.query.filter_by(ID_FIGHTER=ID_FIGHTER).first()
        WEIGHT_CATEGORY = q.WEIGHT_CATEGORY
        print('WEIGHT_CATEGORY: ' + WEIGHT_CATEGORY)
        FIGHT_STYLE = q.FIGHT_STYLE
        SPORT = q.SPORT

        add_request = FIGHT_REQUEST(
            ID_FIGHTER=form.ID_FIGHTER.data,
            ID_MANAGER=ID_MANAGER,
            WEIGHT_CATEGORY=WEIGHT_CATEGORY,
            FIGHT_STYLE=FIGHT_STYLE,
            SPORT=SPORT,
            COUNTRY=form.COUNTRY.data,
            CONTINENT=form.CONTINENT.data,
            CITY=form.CITY.data
        )
        db.session.add(add_request)
        db.session.commit()

        r = db.engine.execute(
            'SELECT c.ID_REQUEST,c.ID_FIGHTER, a.NAME, a.SURNAME, a.NICKNAME, b.WEIGHT_CATEGORY, b.SPORT, c.CONTINENT, c.COUNTRY, c.CITY, b.FIGHT_STYLE '
            'from FIGHTER a '
            'INNER JOIN FIGHTER_DETAILS b ON a.ID_FIGHTER=b.ID_FIGHTER '
            'INNER JOIN FIGHT_REQUEST c ON  c.ID_FIGHTER=a.ID_FIGHTER ORDER BY a.NAME desc')
        list = [i for i in r]
        print(list)

        return render_template('FightRequest.html', form=form, message='Request has been added.', data=list,
                               data1=fighterlist, UserAccountType=UserAccountType)
    return render_template('FightRequest.html', form=form, data=list, data1=fighterlist, UserAccountType=UserAccountType)


@app.route('/deleteRequest', methods=['POST'])
def deleteRequest():
    UserAccountType = CurrentAccountType(current_user.USERNAME)
    print('jestem w deleteRequest')
    # i = FIGHT_REQUEST.query.filter_by(ID_FIGHTER=id_fighter).first()
    continent = request.form['continent']
    print(continent)
    country = request.form['country']
    print(country)
    city = request.form['city']
    print(city)
    id_fighter = request.form['id_fighter']
    print(id_fighter)

    F5 = db.engine.execute("""SELECT ID_REQUEST FROM FIGHT_REQUEST WHERE
    ID_FIGHTER='""" + id_fighter + """' AND 
    CONTINENT='""" + continent + """' AND 
    COUNTRY='""" + country + """' AND 
    CITY='""" + city + """'""")
    list = [i for i in F5]
    q = FIGHT_REQUEST.query.filter_by(ID_REQUEST=list[0][0]).first()
    db.session.delete(q)
    db.session.commit()
    print('success')

    # def updatebomnamerelations():
    #     bom = request.form['bom']
    #     # aspmodel=request.form['aspmodel']
    #     # prodtype=request.form['prodtype']
    #     q = BOM_NAME_RELATION.query.filter_by(BOM_NAME=bom).first()
    #     q.BOM_NAME = request.form['bom']
    #     q.ASPLEX_MODEL = request.form['aspmodel']
    #     q.PRODUCT_TYPE_NAME = request.form['prodtype']
    #     db.session.commit()
    #
    #     return jsonify({'result': 'success'})


    return jsonify({'result': 'success'})


@app.route('/AddFighter2Manager', methods=['GET', 'POST'])
@login_required
def AddFighter2Manager():
    UserAccountType = CurrentAccountType(current_user.USERNAME)
    form = AddFighter()
    name = current_user.USERNAME
    q = USER.query.filter_by(USERNAME=name).first()
    User_id = q.id
    q = USER.query.filter_by(id=User_id).first()
    manager_id = q.MANAGER.ID_MANAGER
    print('ID_MANAGER: ' + str(manager_id))
    id_fighter = form.ID_FIGHTER.data
    f = FIGHTER.query.filter_by(ID_FIGHTER=id_fighter).first()
    m = MANAGER.query.filter_by(ID_MANAGER=manager_id).first()

    if request.method == 'POST' and form.validate():
        try:
            f.FIGHTER_MENAGO.append(m)
            F5 = db.engine.execute("""SELECT ID_FIGHTER FROM FIGHTER_MANAGER WHERE ID_FIGHTER='""" + id_fighter + "'")
            list = [i for i in F5]
            id_men_fighters = [i[0] for i in list]
            if len(id_men_fighters) == 0:
                q = FIGHTER_DETAILS.query.filter_by(ID_FIGHTER=id_fighter).first()
                q.MANAGER_NEED='No'
                db.session.commit()
                gc.collect()
                return render_template('AddFighter2Manager.html', form=form, message='Fighter has been added and status MANAGER_NEED in table FIGHTER_DETAILS has been changed to "No"', UserAccountType=UserAccountType)
            else:
                print(id_men_fighters)
                gc.collect()
                return render_template('AddFighter2Manager.html', form=form, message='Fighter has not been added', UserAccountType=UserAccountType)
        except:
            return render_template('AddFighter2Manager.html', form=form, message='Wrong FIGHTER_ID', UserAccountType=UserAccountType)
    return render_template('AddFighter2Manager.html', form=form, UserAccountType=UserAccountType)


@app.route('/AddFighter2Federation', methods=['GET', 'POST'])
@login_required
def AddFighter2Federation():
    UserAccountType = CurrentAccountType(current_user.USERNAME)
    form = AddFighter()
    name = current_user.USERNAME
    q = USER.query.filter_by(USERNAME=name).first()
    User_id = q.id
    q = USER.query.filter_by(id=User_id).first()
    federation_id = q.FEDERATION.ID_FEDERATION
    federation_name=q.FEDERATION.FEDERATION_NAME
    print(federation_name)
    print('ID_FEDERATION: ' + str(federation_id))
    id_fighter = form.ID_FIGHTER.data
    f = FIGHTER.query.filter_by(ID_FIGHTER=id_fighter).first()
    m = FEDERATION.query.filter_by(ID_FEDERATION=federation_id).first()

    F5 = db.engine.execute("""SELECT DISTINCT f.ID_FIGHTER,f.NAME,f.NICKNAME,f.SURNAME,fd.HEALTH_STATUS,fd.WEIGHT_CATEGORY,fd.READY_TO_FIGHT_DATE FROM FIGHTER f
                                   LEFT JOIN FIGHTER_DETAILS fd ON f.ID_FIGHTER=fd.ID_FIGHTER
                                   LEFT JOIN FIGHTER_FEDERATION fed ON fed.ID_FIGHTER=f.ID_FIGHTER
                                   LEFT JOIN FIGHTER_FIGHTS ff ON ff.ID_FIGHTER=f.ID_FIGHTER
                                   LEFT JOIN FIGHT fi ON fi.ID_FIGHT=ff.ID_FIGHT
                                   LEFT JOIN EVENTS e ON e.ID_EVENT=fi.ID_EVENT
                                   WHERE fed.ID_FEDERATION='""" + str(federation_id) + "' AND f.ID_FIGHTER<>'110'")
    data = [i for i in F5]
    print(data)
    q = MESSAGES.query.filter_by(ID_FEDERATION=1).all()
    job_requests=[[i.TEXT,i.ID_FIGHTER,i.STATUS,i.CONFIRMATION,i.ID_MESSAGE,i.FEDERATION_VISIBLE] for i in q]
    print("""job_request list below:""")
    print(job_requests)
    q = db.engine.execute("""SELECT DISTINCT ID_FIGHTER FROM FIGHTER_FEDERATION""")
    fighter_federation=[i.ID_FIGHTER for i in q]
    print("""Present federation fighters""")
    print(fighter_federation)

    if request.method == 'POST':
        q = MESSAGES.query.filter(MESSAGES.ID_FEDERATION.like(federation_id)).filter(MESSAGES.CONFIRMATION != 4).all()
        federation_requests=[i.ID_FIGHTER for i in q]
        print("Federation request")
        print(federation_requests)

        if int(form.ID_FIGHTER.data) in fighter_federation:
            return render_template('AddFighter2Federation.html', form=form,
                                   message_fail='Fighter which You requested is Your fighter actually.', UserAccountType=UserAccountType,data=data, job_requests=job_requests)
        elif int(form.ID_FIGHTER.data) in federation_requests:
            return render_template('AddFighter2Federation.html', form=form,
                                   message_fail='You have already sent request to the fighter', UserAccountType=UserAccountType, data=data,job_requests=job_requests)
        else:
            send_message = MESSAGES(
                    SUBJECT=str(federation_name) + " federation send You a job offer.",
                    TEXT=form.TEXT.data,
                    ID_FEDERATION=federation_id,
                    ID_FIGHTER=form.ID_FIGHTER.data,
                    STATUS='PENDING',
                    FEDERATION_VISIBLE=1,
                    FIGHTER_VISIBLE=1,
                    CONFIRMATION=0)
            db.session.add(send_message)
            db.session.commit()

            q = MESSAGES.query.filter_by(ID_FEDERATION=1).all()
            job_requests = [[i.TEXT, i.ID_FIGHTER, i.STATUS, i.CONFIRMATION, i.ID_MESSAGE, i.FEDERATION_VISIBLE] for i in q]
            return render_template('AddFighter2Federation.html', form=form,
                                       message_success='Requst has been sent to fighter, please wait for their acceptation', UserAccountType=UserAccountType, data=data,
                                       job_requests=job_requests)
    return render_template('AddFighter2Federation.html', form=form, UserAccountType=UserAccountType, data=data,job_requests=job_requests)

@app.route('/Messages', methods=['GET', 'POST'])
@login_required
def Messages():
    UserAccountType = CurrentAccountType(current_user.USERNAME)
    q=USER.query.filter_by(USERNAME=current_user.USERNAME).first()
    account_type=q.ACCOUNT_TYPE
    if account_type=='Fighter':
        print(account_type)
        id_fighter=q.FIGHTER.ID_FIGHTER
        q=MESSAGES.query.filter_by(ID_FIGHTER=id_fighter)
        data = [[i.SUBJECT,i.TEXT,i.ID_FEDERATION,i.ID_MESSAGE,i.CONFIRMATION,i.FIGHTER_VISIBLE] for i in q]
        print(data)
        return render_template('messages.html', data=data)
    elif account_type=='Manager':
        id_manager = q.FEDERATION.ID_FEDERATION
        print(id_manager)
        q = MESSAGES.query.filter_by(ID_MANAGER=id_manager)
        data = [[i.SUBJECT, i.TEXT, i.ID_FEDERATION, i.ID_MESSAGE, i.CONFIRMATION,i.FIGHTER_VISIBLE] for i in q]
        return render_template('messages.html', data=data, UserAccountType=UserAccountType)

@app.route('/messages_federation_json_accept', methods=['POST'])
@login_required
def messages_federation_json_accept():
    UserAccountType = CurrentAccountType(current_user.USERNAME)
    q = USER.query.filter_by(USERNAME=current_user.USERNAME).first()
    account_type = q.ACCOUNT_TYPE

    if account_type == 'Fighter':
        print('jsonify POST')
        id_message = request.form['id_message']
        print(id_message)

        q = MESSAGES.query.filter_by(ID_MESSAGE=id_message).first()
        q.CONFIRMATION = 1
        q.STATUS = """CONFIRMED"""
        db.session.commit()

        id_federation = q.ID_FEDERATION
        id_fighter = q.ID_FIGHTER

        f = FIGHTER.query.filter_by(ID_FIGHTER=id_fighter).first()
        m = FEDERATION.query.filter_by(ID_FEDERATION=id_federation).first()

        f.FIGHTER_FEDERO.append(m)
        db.session.commit()
        print('Fighter has been added to Federation.')

    elif account_type == 'Federation':
        print('jsonify POST')
        id_message = request.form['id_message']
        print(id_message)

        q = MESSAGES.query.filter_by(ID_MESSAGE=id_message).first()
        q = MENAGER_VISIBLE = 0
        db.session.commit()
    return jsonify({'result': 'success'})

@app.route('/messages_federation_json_refuse', methods=['POST'])
@login_required
def messages_federation_json_refuse():
    UserAccountType = CurrentAccountType(current_user.USERNAME)
    id_message = request.form['id_message']
    print(id_message)
    q = MESSAGES.query.filter_by(ID_MESSAGE=id_message).first()
    q.CONFIRMATION = 0
    q.STATUS = 'REJECTED'
    q.FIGHTER_VISIBLE = 0
    db.session.commit()
    print('STATUS:"REJECTED" CONFIRMATION:"0" AND FIGHTER_VISIBLE:"0"')

    return jsonify({'result': 'success'})

@app.route('/messages_federation_json_delete', methods=['POST'])
@login_required
def messages_federation_json_delete():
    print("test")
    id_message = request.form['id_message']
    print(id_message)
    q = MESSAGES.query.filter_by(ID_MESSAGE=id_message).first()
    db.session.delete(q)
    db.session.commit()
    print('Message not been deleted.')
    return jsonify({'result': 'success'})

@app.route('/Notes')
def Notes():
    return render_template('Notes.html')

@app.route('/download')
def download():
    file_data = IMAGES.query.filter_by(USERNAME='fighter_1').first()

    return send_file(BytesIO(file_data.DATA), attachment_filename='test.jpg', as_attachment=True)

@app.route('/FighterProfile/<id_fighter>')
def FighterProfile(id_fighter):
    UserAccountType = CurrentAccountType(current_user.USERNAME)
    F5 = db.engine.execute(
        'SELECT fight.ID_FIGHTER,fight.NAME,fight.NICKNAME,fight.SURNAME,det.FIGHT_STYLE,det.HEIGHT,det.WEIGHT,det.NUMBER_OF_WINS,det.NUMBER_OF_LOSS,det.URL '
        'FROM FIGHTER fight '
        'INNER JOIN FIGHTER_DETAILS det ON fight.ID_FIGHTER=det.ID_FIGHTER'
        ' WHERE fight.ID_FIGHTER=' + "'" + id_fighter + "'")
    list = [i for i in F5]
    q = FIGHTER.query.filter_by(ID_FIGHTER=id_fighter).first()
    fighter_name = q.USER.USERNAME
    file_data = IMAGES.query.filter_by(USERNAME=fighter_name).first()
    if file_data is None:
        print('file is none')
        return render_template('FighterProfile.html', data=list, UserAccountType=UserAccountType)
    else:
        print('file_data is not none')
        image = base64.b64encode(file_data.DATA).decode('ascii')
        return render_template('FighterProfile.html', data=list, image=image, UserAccountType=UserAccountType)

@app.route('/EventInformation/<id_event>')
def EventInformation(id_event):

    UserAccountType=CurrentAccountType(current_user.USERNAME)
    F5 = db.engine.execute("""SELECT f.NAME,f.NICKNAME,f.SURNAME,fd.WEIGHT_CATEGORY,f.ID_FIGHTER,ff.ID_FIGHT,fd.NUMBER_OF_WINS,fd.NUMBER_OF_LOSS,fd.NUMBER_OF_DRAW,fd.NUMBER_OF_NC FROM FIGHTER f
    INNER JOIN EVENTS eve ON eve.ID_EVENT=fi.ID_EVENT
    INNER JOIN FIGHTER_FIGHTS ff ON ff.ID_FIGHTER=f.ID_FIGHTER
    INNER JOIN FIGHT fi ON fi.ID_FIGHT=ff.ID_FIGHT
    INNER JOIN FIGHTER_DETAILS fd ON fd.ID_FIGHTER=f.ID_FIGHTER
    WHERE eve.ID_EVENT='""" + id_event + """'""")
    data = [i for i in F5]
    print(data)

    q=EVENTS.query.filter_by(ID_EVENT=id_event).first()
    event_data=[q.EVENT_NAME,q.CITY,q.COUNTRY,q.DATE,q.TIME]

    return render_template('EventInformation.html', data=data,event_data=event_data, UserAccountType=UserAccountType)

@app.route('/JSON/Edit/Event/Information', methods=['POST'])
def JSONEditEventInformation():
    print("Yo you it works")
    print(requests.get(url="""/JSON/Edit/Event/Information"""))
    return jsonify({'result': 'success'})


@app.route('/FederationProfile/<federation_name>')
def FedertionProfile(federation_name):
    UserAccountType = CurrentAccountType(current_user.USERNAME)
    print('Federation name is: ' + str(federation_name))
    q = FEDERATION.query.filter_by(FEDERATION_NAME=federation_name).first()
    id_federation = q.ID_FEDERATION
    print(id_federation)

    F5 = db.engine.execute("""SELECT f.ID_FEDERATION,f.NAME,f.SURNAME,f.FEDERATION_NAME,f.FEDERATION_CREATED_DATE,a.CONTINENT,a.COUNTRY,a.CITY,a.ZIP_CODE,a.STREET,a.STREET_NUMBER,c.PHONE_NUMBER,c.PHONE_NUMBER2,c.E_MAIL FROM FEDERATION f
    INNER JOIN ADDRESS a ON f.ID_FEDERATION=a.ID_FEDERATION
    INNER JOIN CONTACT c ON f.ID_FEDERATION=c.ID_FEDERATION
    WHERE f.ID_FEDERATION='""" + str(id_federation) + "'")
    list = [i for i in F5]
    for i in list:
        print(i)
    file_data = IMAGES.query.filter_by(USERNAME=federation_name).first()
    if file_data is None:
        print('file is none')
        return render_template('FederationProfile.html', data=list, UserAccountType=UserAccountType)
    else:
        print('file_data is not none')
        image = base64.b64encode(file_data.DATA).decode('ascii')
        return render_template('FederationProfile.html', data=list, image=image, UserAccountType=UserAccountType)

@app.route('/ShowFederationEven', methods=['GET', 'POST'])
@login_required
def ShowFederationEven():
    UserAccountType = CurrentAccountType(current_user.USERNAME)
    form = test120()
    # print("nowe czasu liczenie")
    name = current_user.USERNAME
    q = USER.query.filter_by(USERNAME=name).first()
    id_federation = q.FEDERATION.ID_FEDERATION

    print(id_federation)
    q = EVENTS.query.filter(EVENTS.ID_FEDERATION.like(id_federation)).filter(EVENTS.EVENT_STATUS.notlike('Fisnihed')).all()
    list=[[i.EVENT_NAME,i.CITY,i.CONTINENT,i.COUNTRY,i.ZIP_CODE,i.NUMBER_OF_FIGHTS,i.STREET,i.STREET_NUMBER,i.DATE,i.TIME,i.NEED_FIGHTER_STATUS,i.EVENT_STATUS,i.ID_EVENT] for i in q]

    if form.validate_on_submit():
        continent = form.CONTINENT.data,
        country = form.COUNTRY.data,
        city = form.CITY.data,
        event_status = form.EVENT_STATUS.data,

        print(continent[0])
        print(country[0])
        print(city[0])
        print(event_status[0])
        F5 = db.engine.execute(
            """SELECT EVENT_NAME,CITY,CONTINENT,COUNTRY,ZIP_CODE,NUMBER_OF_FIGHTS,STREET,STREET_NUMBER,DATE,TIME,NEED_FIGHTER_STATUS,EVENT_STATUS,ID_EVENT FROM EVENTS WHERE ID_FEDERATION= """ + "'" + str(
                id_federation) + "'"
                                 """AND CONTINENT like""" + "'" + str(continent[0]) + "'"
                                                                                      """AND COUNTRY  like""" + "'" + str(
                country[0]) + "'"
                              """AND CITY like """ + "'" + str(city[0]) + "%'"
                                                                          """AND EVENT_STATUS like """ + "'" + str(
                event_status[0]) + "'")

        list = [i for i in F5]
        print(list)
        print("test")
        return render_template('ShowFederationEvents.html', data=list, form=form, UserAccountType=UserAccountType)
    return render_template('ShowFederationEvents.html', form=form, data=list, UserAccountType=UserAccountType)

@app.route('/UpdateAddress', methods=['GET', 'POST'])
@login_required
def UpdateAddress():
    UserAccountType = CurrentAccountType(current_user.USERNAME)
    user = USER.query.filter_by(USERNAME=current_user.USERNAME).first()
    check_account_type = user.ACCOUNT_TYPE
    print(str(check_account_type) + ' account want change address')
    if check_account_type == 'Fighter':
        query = USER.query.filter_by(USERNAME=current_user.USERNAME).first()
        id_fighter = query.FIGHTER.ID_FIGHTER
        q = FIGHTER.query.filter_by(ID_FIGHTER=id_fighter).first()
    elif check_account_type == 'Manager':
        query = USER.query.filter_by(USERNAME=current_user.USERNAME).first()
        id_manager = query.MANAGER.ID_MANAGER
        q = MANAGER.query.filter_by(ID_MANAGER=id_manager).first()
    elif check_account_type == 'Federation':
        query = USER.query.filter_by(USERNAME=current_user.USERNAME).first()
        id_federation = query.FEDERATION.ID_FEDERATION
        q = FEDERATION.query.filter_by(ID_FEDERATION=id_federation).first()

    return render_template('UpdateAddress.html', q=q, check_account_type=check_account_type, UserAccountType=UserAccountType)

@app.route('/updateAddress', methods=['POST'])
def updateAddress():
    user = USER.query.filter_by(USERNAME=current_user.USERNAME).first()
    check_account_type = user.ACCOUNT_TYPE
    print(str(check_account_type))
    if check_account_type == 'Fighter':
        query = USER.query.filter_by(USERNAME=current_user.USERNAME).first()
        id_fighter = query.FIGHTER.ID_FIGHTER
        i = ADDRESS.query.filter_by(ID_FIGHTER=id_fighter).first()
        i.CONTINENT = request.form['continent']
        i.COUNTRY = request.form['country']
        i.CITY = request.form['city']
        i.ZIP_CODE = request.form['zip_code']
        i.STREET = request.form['street']
        i.STREET_NUMBER = request.form['street_number']
        db.session.commit()

    elif check_account_type == 'Manager':
        query = USER.query.filter_by(USERNAME=current_user.USERNAME).first()
        id_manager = query.MANAGER.ID_MANAGER
        i = ADDRESS.query.filter_by(ID_MANAGER=id_manager).first()
        i.CONTINENT = request.form['continent']
        i.COUNTRY = request.form['country']
        i.CITY = request.form['city']
        i.ZIP_CODE = request.form['zip_code']
        i.STREET = request.form['street']
        i.STREET_NUMBER = request.form['street_number']
        db.session.commit()

    elif check_account_type == 'Federation':
        query = USER.query.filter_by(USERNAME=current_user.USERNAME).first()
        id_federation = query.FEDERATION.ID_FEDERATION
        i = ADDRESS.query.filter_by(ID_FEDERATION=id_federation).first()
        i.CONTINENT = request.form['continent']
        i.COUNTRY = request.form['country']
        i.CITY = request.form['city']
        i.ZIP_CODE = request.form['zip_code']
        i.STREET = request.form['street']
        i.STREET_NUMBER = request.form['street_number']
        db.session.commit()

    return jsonify({'result': 'success'})

@app.route('/UpdateContact', methods=['GET', 'POST'])
@login_required
def UpdateContact():
    UserAccountType = CurrentAccountType(current_user.USERNAME)
    user = USER.query.filter_by(USERNAME=current_user.USERNAME).first()
    check_account_type = user.ACCOUNT_TYPE
    print(str(check_account_type) + ' account want change address')
    if check_account_type == 'Fighter':
        query = USER.query.filter_by(USERNAME=current_user.USERNAME).first()
        id_fighter = query.FIGHTER.ID_FIGHTER
        q = FIGHTER.query.filter_by(ID_FIGHTER=id_fighter).first()
    elif check_account_type == 'Manager':
        query = USER.query.filter_by(USERNAME=current_user.USERNAME).first()
        id_manager = query.MANAGER.ID_MANAGER
        q = MANAGER.query.filter_by(ID_MANAGER=id_manager).first()
    elif check_account_type == 'Federation':
        query = USER.query.filter_by(USERNAME=current_user.USERNAME).first()
        id_federation = query.FEDERATION.ID_FEDERATION
        q = FEDERATION.query.filter_by(ID_FEDERATION=id_federation).first()
    return render_template('UpdateContact.html', q=q, check_account_type=check_account_type, UserAccountType=UserAccountType)

@app.route('/updateContact', methods=['POST'])
def updateContact():
    user = USER.query.filter_by(USERNAME=current_user.USERNAME).first()
    check_account_type = user.ACCOUNT_TYPE
    print(str(check_account_type))

    if check_account_type == 'Fighter':
        query = USER.query.filter_by(USERNAME=current_user.USERNAME).first()
        id_fighter = query.FIGHTER.ID_FIGHTER
        i = CONTACT.query.filter_by(ID_FIGHTER=id_fighter).first()
        i.PHONE_NUMBER = request.form['phone_number']
        i.PHONE_NUMBER2 = request.form['phone_number_2']
        i.E_MAIL = request.form['e_mail']
        db.session.commit()

    if check_account_type == 'Manager':
        query = USER.query.filter_by(USERNAME=current_user.USERNAME).first()
        id_manager = query.MANAGER.ID_MANAGER
        i = CONTACT.query.filter_by(ID_MANAGER=id_manager).first()
        i.PHONE_NUMBER = request.form['phone_number']
        i.PHONE_NUMBER2 = request.form['phone_number_2']
        i.E_MAIL = request.form['e_mail']
        db.session.commit()

    if check_account_type == 'Federation':
        query = USER.query.filter_by(USERNAME=current_user.USERNAME).first()
        id_federaton = query.FEDERATION.ID_FEDERATION
        i = CONTACT.query.filter_by(ID_FEDERATION=id_federaton).first()
        i.PHONE_NUMBER = request.form['phone_number']
        i.PHONE_NUMBER2 = request.form['phone_number_2']
        i.E_MAIL = request.form['e_mail']
        db.session.commit()

    return jsonify({'result': 'success'})

@app.route('/UpdateFighterFighterDetails', methods=['GET', 'POST'])
@login_required
def UpdateFighterFighterDetails():
    UserAccountType = CurrentAccountType(current_user.USERNAME)
    name = current_user.USERNAME
    print(name)
    query = USER.query.filter_by(USERNAME=name).first()
    id_fighter = query.FIGHTER.ID_FIGHTER
    print(id_fighter)
    q = FIGHTER.query.filter_by(ID_FIGHTER=id_fighter).first()
    return render_template('FighterFighterDetails.html', q=q, FIGHTERS_LIST=FIGHTERS_LIST,
                           FEDERATIONS_LIST=FEDERATIONS_LIST, MANAGERS_LIST=MANAGERS_LIST)

@app.route('/updateFighterFighterDetails', methods=['POST'])
def updateFighterDetails():
    name = current_user.USERNAME
    query = USER.query.filter_by(USERNAME=name).first()
    id_fighter = query.FIGHTER.ID_FIGHTER

    i = FIGHTER_DETAILS.query.filter_by(ID_FIGHTER=id_fighter).first()
    i.WEIGHT_CATEGORY = request.form['weight_category']
    i.SPORT = request.form['sport']
    i.WEIGHT = request.form['weight']
    i.HEIGHT = request.form['height']
    i.FIGHT_STYLE = request.form['fight_style']
    i.NUMBER_OF_WINS = request.form['number_of_wins']
    i.NUMBER_OF_LOSS = request.form['number_of_loss']
    db.session.commit()
    return jsonify({'result': 'success'})

@app.route('/UpdateFighterFightDetails', methods=['GET', 'POST'])
@login_required
def UpdateFighterFightDetails():

    name = current_user.USERNAME
    print(name)
    query = USER.query.filter_by(USERNAME=name).first()
    id_fighter = query.FIGHTER.ID_FIGHTER
    print(id_fighter)
    q = FIGHTER.query.filter_by(ID_FIGHTER=id_fighter).first()
    return render_template('FighterFightDetails.html', q=q, FIGHTERS_LIST=FIGHTERS_LIST,
                           FEDERATIONS_LIST=FEDERATIONS_LIST, MANAGERS_LIST=MANAGERS_LIST)

@app.route('/updateFighterFightDetails', methods=['POST'])
def updateFighterFightDetails():
    name = current_user.USERNAME
    query = USER.query.filter_by(USERNAME=name).first()
    id_fighter = query.FIGHTER.ID_FIGHTER

    # Actuall health status
    health_query = FIGHTER_DETAILS.query.filter_by(ID_FIGHTER=id_fighter).first()
    actual_health = health_query.HEALTH_STATUS
    print(' ' + str(actual_health))

    i = FIGHTER_DETAILS.query.filter_by(ID_FIGHTER=id_fighter).first()
    i.HEALTH_STATUS = request.form['health_status']
    if i.HEALTH_STATUS != actual_health:
        print(actual_health)
        print(i.HEALTH_STATUS)
        print("""Health condition has been changed""")
        F5 = db.engine.execute("""SELECT ID_MANAGER FROM FIGHTER_MANAGER WHERE ID_FIGHTER='""" + str(id_fighter) + "'")
        manager = [i for i in F5]
        e_mail = CONTACT.query.filter_by(ID_MANAGER=manager[0][0]).first()
        manager_name = MANAGER.query.filter_by(ID_MANAGER=manager[0][0]).first()
        manager_name.NAME
        fighter_name = FIGHTER.query.filter_by(ID_FIGHTER=id_fighter).first()
        fighter_name.NAME
        fighter_name.SURNAME
        msg = mail.send_message(
            'Health issue',
            sender='wlapie40@gmail.com',
            recipients=['wlapie40@gmail.com'],
            body='Hi ' + str(manager_name.NAME) + ' Your fighter: ' + str(fighter_name.NAME) + ' ' + str(
                fighter_name.SURNAME) + ' has just changed health status ' + str(i.HEALTH_STATUS))
        print(e_mail.E_MAIL)

    else:
        print("""Health condition doesn't change""")
    i.HEALTH_DESCRIPTION = request.form['health_description']
    i.FREE_AGENT = request.form['free_agent']
    i.MANAGER_NEED = request.form['manager_need']
    i.FIGHT_STATUS = request.form['fight_status']
    i.READY_TO_FIGHT_DATE = request.form['ready_to_fight_date']

    db.session.commit()
    return jsonify({'result': 'success'})

@app.route('/UpdateManagerManagerDetails', methods=['GET', 'POST'])
@login_required
def UpdateManagerManagerDetails():
    name = current_user.USERNAME
    print(name)
    query = USER.query.filter_by(USERNAME=name).first()
    id_manager = query.MANAGER.ID_MANAGER
    print(id_manager)
    q = MANAGER.query.filter_by(ID_MANAGER=id_manager).all()
    return render_template('ManagerManagerDetails.html', q=q, FIGHTERS_LIST=FIGHTERS_LIST,
                           FEDERATIONS_LIST=FEDERATIONS_LIST, MANAGERS_LIST=MANAGERS_LIST)

@app.route('/updateManagerManagerDetails', methods=['POST'])
def updateManagerManagerDetails():
    name = current_user.USERNAME
    query = USER.query.filter_by(USERNAME=name).first()
    id_manager = query.MANAGER.ID_MANAGER

    i = MANAGER.query.filter_by(ID_MANAGER=id_manager).first()
    i.NAME = request.form['name']
    i.SURNAME = request.form['surname']
    i.SPORT = request.form['sport']
    i.JOB_FIGHTERS = request.form['job_fighters']
    i.JOB_FIGHTS = request.form['job_fights']

    db.session.commit()
    return jsonify({'result': 'success'})

@app.route('/ShowYourTeam', methods=['GET', 'POST'])
@login_required
def ShowYourTeam():
    form = CheckTeam()
    fight_status = form.FIGHT_STATUS.data,
    health_status = form.HEALTH_STATUS.data,

    name = current_user.USERNAME
    query = USER.query.filter_by(USERNAME=name).first()
    id_manager = query.MANAGER.ID_MANAGER

    F5 = db.engine.execute("""SELECT f.ID_FIGHTER,f.NAME,f.NICKNAME,f.SURNAME,fd.HEALTH_STATUS,fd.READY_TO_FIGHT_DATE,e.EVENT_NAME,fi.WEIGHT_CATEGORY,e.DATE,e.ID_EVENT,ff.ID_FIGHT FROM FIGHTER f
                    LEFT JOIN FIGHTER_DETAILS fd ON f.ID_FIGHTER=fd.ID_FIGHTER
                    LEFT JOIN FIGHTER_MANAGER fm ON fm.ID_FIGHTER=f.ID_FIGHTER
                    LEFT JOIN FIGHTER_FIGHTS ff ON ff.ID_FIGHTER=f.ID_FIGHTER
                    LEFT JOIN FIGHT fi ON fi.ID_FIGHT=ff.ID_FIGHT
                    LEFT JOIN EVENTS e ON e.ID_EVENT=fi.ID_EVENT
                    WHERE fm.ID_MANAGER='""" + str(id_manager) + "'")
    list = [i for i in F5]
    print(list)

    if form.validate_on_submit():
        name = current_user.USERNAME
        query = USER.query.filter_by(USERNAME=name).first()
        id_manager = query.MANAGER.ID_MANAGER
        print('ID_MANAGER: ' + str(id_manager))

        # Wyciagmy liste fighterow
        # F5 = db.engine.execute("""SELECT ID_FIGHTER FROM FIGHTER_MANAGER
        #      WHERE ID_MANAGER=""" + str(id_manager))
        # list = [i for i in F5]
        # id_fighter_list = [str(i[0]) for i in list]
        # print('ID_FIGHTER nunumbers belong to ID_MANAGER ' + str(id_manager))
        #
        #
        # fighters_id = ''.join(["'" + i + "'" + "," for i in id_fighter_list])
        # print(fighters_id)

        # Wyciągamy listę walk fighterów
        # F5 = db.engine.execute("""SELECT e.EVENT_NAME,f.WEIGHT_CATEGORY,e.DATE,ff.ID_FIGHTER FROM EVENTS e
        # LEFT JOIN FIGHT f ON f.ID_EVENT=e.ID_EVENT
        # LEFT JOIN FIGHTER_FIGHTS ff ON ff.ID_FIGHT=f.ID_FIGHT
        # WHERE ff.ID_FIGHTER IN("""+fighters_id[:-1]+")")
        # Fights = [i for i in F5]
        # print(Fights)



        # event_list=[]
        # [event_list.append(i) for i in Fights if if_statement]
        # print('event_list')
        # print(event_list)
        #
        # F5 = db.engine.execute("""SELECT f.ID_FIGHTER,f.NAME,f.NICKNAME,f.SURNAME,fd.HEALTH_STATUS,fd.READY_TO_FIGHT_DATE,e.EVENT_NAME,fi.WEIGHT_CATEGORY,e.DATE FROM FIGHTER f
        #            LEFT JOIN FIGHTER_DETAILS fd ON f.ID_FIGHTER=fd.ID_FIGHTER
        #            LEFT JOIN FIGHTER_MANAGER fm ON fm.ID_FIGHTER=f.ID_FIGHTER
        #            LEFT JOIN FIGHTER_FIGHTS ff ON ff.ID_FIGHTER=f.ID_FIGHTER
        #            LEFT JOIN FIGHT fi ON fi.ID_FIGHT=ff.ID_FIGHT
        #            LEFT JOIN EVENTS e ON e.ID_EVENT=fi.ID_EVENT
        #            WHERE f.ID_FIGHTER IN (""" + fighters_id[:-1]+")"+""" AND fd.HEALTH_STATUS="""+"'"+str(health_status[0])+"'"+"""AND fd.FIGHT_STATUS="""+"'"+str(fight_status[0])+"'")
        # list = [i for i in F5]
        # print('list')
        # print(list)
        F5 = db.engine.execute("""SELECT f.ID_FIGHTER,f.NAME,f.NICKNAME,f.SURNAME,fd.HEALTH_STATUS,fd.FIGHT_STATUS,fd.READY_TO_FIGHT_DATE,fi.WEIGHT_CATEGORY,e.DATE,e.ID_EVENT,ff.ID_FIGHTFROM FIGHTER f
                      LEFT JOIN FIGHTER_DETAILS fd ON f.ID_FIGHTER=fd.ID_FIGHTER
                      LEFT JOIN FIGHTER_MANAGER fm ON fm.ID_FIGHTER=f.ID_FIGHTER
                      LEFT JOIN FIGHTER_FIGHTS ff ON ff.ID_FIGHTER=f.ID_FIGHTER
                      LEFT JOIN FIGHT fi ON fi.ID_FIGHT=ff.ID_FIGHT
                      LEFT JOIN EVENTS e ON e.ID_EVENT=fi.ID_EVENT
                      WHERE fm.ID_MANAGER='""" + str(id_manager) + "'" + """AND fd.HEALTH_STATUS like""" + "'%" + str(
            health_status[0]) + "%'" + """AND fd.FIGHT_STATUS like""" + "'%" + str(fight_status[0]) + "%'")
        list = [i for i in F5]
        print('list')
        print(list)

        return render_template('ShowYourTeam.html', form=form, data=list, FIGHTERS_LIST=FIGHTERS_LIST,
                               FEDERATIONS_LIST=FEDERATIONS_LIST, MANAGERS_LIST=MANAGERS_LIST)
    return render_template('ShowYourTeam.html', form=form, data=list, FIGHTERS_LIST=FIGHTERS_LIST,
                           FEDERATIONS_LIST=FEDERATIONS_LIST, MANAGERS_LIST=MANAGERS_LIST)

@app.route('/ShowYourTeam/Event/Information/<id_event>/<id_fighter>/<id_fight>')
def ShowYourTeamEventInformation(id_event, id_fighter, id_fight):
    UserAccountType = CurrentAccountType(current_user.USERNAME)
    F5_opp = db.engine.execute("""SELECT f.NAME,f.NICKNAME,f.SURNAME,f.ID_FIGHTER FROM FIGHTER f
    INNER JOIN FIGHTER_FIGHTS ff ON ff.ID_FIGHTER=f.ID_FIGHTER 
    INNER JOIN FIGHT fi ON fi.ID_FIGHT=ff.ID_FIGHT
    INNER JOIN EVENTS e ON e.ID_EVENT=fi.ID_EVENT
    WHERE e.ID_EVENT='""" + id_event + "' " + """and ff.ID_FIGHTER<>'""" + id_fighter + "'" + """AND ff.ID_FIGHT='""" + id_fight + "'")
    print('Opponent information')
    opp = [i for i in F5_opp]

    print('ID_EVENT: ' + str(id_event))
    print('ID_FIGHTER: ' + str(id_fighter))

    F5 = db.engine.execute("""SELECT e.EVENT_NAME,e.CITY,e.CONTINENT,e.COUNTRY,e.ZIP_CODE,e.STREET,e.STREET_NUMBER,e.DATE,e.TIME,e.NEED_FIGHTER_STATUS,e.EVENT_STATUS FROM EVENTS e
     INNER JOIN FIGHT f ON f.ID_EVENT=e.ID_EVENT 
     INNER JOIN FIGHTER_FIGHTS ff ON ff.ID_FIGHT=f.ID_FIGHT
     WHERE e.ID_EVENT='""" + id_event + "' " + """and ff.ID_FIGHTER='""" + id_fighter + "'")
    list = [i for i in F5]
    print('Event information')
    print(list)
    return render_template('ShowYourTeamEventInformation.html', data=list, data2=opp, UserAccountType=UserAccountType)


@app.route('/FindEvent', methods=['GET', 'POST'])
@login_required
def FindEvent():
    UserAccountType = CurrentAccountType(current_user.USERNAME)
    form = SearchFighter()
    continent = form.CONTINENT.data,
    country = form.COUNTRY.data,
    city = form.CITY.data,
    weight_category = form.WEIGHT_CATEGORY.data,
    number_of_fights = form.NUMBER_OF_FIGHTS.data,

    fight_style = form.FIGHT_STYLE.data,

    health_status = form.HEALTH_STATUS.data,
    fight_status = form.FIGHT_STATUS.data
    today = time.strftime("%d/%m/%Y")

    if form.validate_on_submit():
        if len(country[0]) == 0:
            country = ('%')
        if len(city[0]) == 0:
            city = ('%')
        if len(number_of_fights[0]) == 0:
            number_of_fights = ('0')
        if len(fight_status[0]) == 0:
            fight_status = ('%')
        if len(health_status[0]) == 0:
            health_status = ('%')
        F5 = db.engine.execute("""
        SELECT f.ID_FIGHTER,f.NAME,f.SURNAME,f.NICKNAME,
        CASE WHEN fd.WEIGHT_CATEGORY='' THEN '%' ELSE fd.WEIGHT_CATEGORY END
            ,fd.WEIGHT,fd.HEIGHT,fd.HEALTH_STATUS,fd.READY_TO_FIGHT_DATE,fd.FIGHT_STATUS,
        CASE WHEN fd.FIGHT_STYLE='' THEN '%' ELSE fd.FIGHT_STYLE END
            ,fd.NUMBER_OF_WINS,fd.NUMBER_OF_LOSS,a.CONTINENT,a.COUNTRY,a.CITY
        FROM FIGHTER f
        INNER JOIN FIGHTER_DETAILS fd ON f.ID_FIGHTER=fd.ID_FIGHTER
        INNER JOIN ADDRESS a ON a.ID_FIGHTER=f.ID_FIGHTER
            WHERE fd.WEIGHT_CATEGORY like """ + "'" + weight_category[0] + "'" + """
            AND fd.FIGHT_STYLE like """ + "'" + str(fight_style[0]) + "'" + """
            AND a.CONTINENT like """ + "'" + str(continent[0]) + "'" + """
            AND a.COUNTRY like """ + "'" + str(country[0]) + "'" + """
            AND a.CITY like """ + "'" + str(city[0]) + "'" + """
            AND fd.NUMBER_OF_WINS >= """ + number_of_fights[0] + """
            AND fd.FIGHT_STATUS like""" + "'" + str(fight_status) + "'" + """
            AND fd.HEALTH_STATUS like""" + "'" + str(
            health_status[0]) + "' ORDER BY fd.WEIGHT_CATEGORY,fd.READY_TO_FIGHT_DATE"
                               )
        list = [i for i in F5]
        print(list)
        return render_template('FindEvent.html', form=form, data=list, UserAccountType=UserAccountType)
    return render_template('FindEvent.html', form=form, UserAccountType=UserAccountType)


# Not finished
@app.route('/Phonebook', methods=['GET', 'POST'])
@login_required
def Phonebook():
    UserAccountType = CurrentAccountType(current_user.USERNAME)
    user = USER.query.filter_by(USERNAME=current_user.USERNAME).first()
    check_account_type = user.ACCOUNT_TYPE
    print(str(check_account_type))

    if check_account_type == 'Fighter':
        query = USER.query.filter_by(USERNAME=current_user.USERNAME).first()
        id_fighter = query.FIGHTER.ID_FIGHTER

        query = USER.query.filter_by(USERNAME=current_user.USERNAME).first()
        id_fighter = query.FIGHTER.ID_FIGHTER

        F5 = db.engine.execute("""SELECT c.PHONE_NUMBER,c.PHONE_NUMBER2,c.E_MAIL FROM CONTACT c
        INNER JOIN FIGHTER_MANAGER fm ON fm.ID_FIGHTER=c.ID_FIGHTER""")

    if check_account_type == 'Manager':
        query = USER.query.filter_by(USERNAME=current_user.USERNAME).first()
        id_manager = query.MANAGER.ID_MANAGER

        F5 = db.engine.execute("""""")

    if check_account_type == 'Federation':
        query = USER.query.filter_by(USERNAME=current_user.USERNAME).first()
        id_federaton = query.FEDERATION.ID_FEDERATION

        F5 = db.engine.execute("""""")

    return render_template('CreateFighterProfile.html', UserAccountType=UserAccountType)


@app.route('/FindFederations', methods=['GET', 'POST'])
@login_required
def FindFederations():
    UserAccountType = CurrentAccountType(current_user.USERNAME)
    form = FindFederation()
    continent = form.CONTINENT.data,
    country = form.COUNTRY.data,
    city = form.CITY.data

    if form.validate_on_submit():
        print('Continent: ' + str(continent[0]))
        print('Country: ' + str(country[0]))
        if len(city) == 0:
            city = '%'
        print('City: ' + str(city))

        if continent[0] == '%' and city == '%' and country[0] == '%':
            print('search everything')
            F5 = db.engine.execute("""SELECT f.FEDERATION_NAME,f.FEDERATION_CREATED_DATE,a.COUNTRY,a.CITY FROM FEDERATION f
                    INNER JOIN ADDRESS a ON f.ID_FEDERATION=a.ID_FEDERATION""")
            data = [i for i in F5]
            return render_template('FindFederation.html', form=form, data=data)
        elif continent[0] != '%' and city == '%' and country[0] == '%':
            print('test1')
            F5 = db.engine.execute("""SELECT f.FEDERATION_NAME,f.FEDERATION_CREATED_DATE,a.COUNTRY,a.CITY FROM FEDERATION f
                            INNER JOIN ADDRESS a ON f.ID_FEDERATION=a.ID_FEDERATION
                            WHERE a.CONTINENT='""" + continent[0] + "'")
            data = [i for i in F5]
            return render_template('FindFederation.html', form=form, data=data)
            # F5 = db.engine.execute("""SELECT f.FEDERATION_NAME,f.FEDERATION_CREATED_DATE,a.COUNTRY,a.CITY FROM FEDERATION f
            #                     INNER JOIN ADDRESS a ON f.ID_FEDERATION=a.ID_FEDERATION
            #                     WHERE a.CONTINENT='""" + continent[0] + "'" + """ AND a.COUNTRY like '""" + country[0] + "'" + """ AND a.CITY like'""" + city + "'")
            # data = [i for i in F5]
        elif continent[0] == '%' and city != '%' and country[0] == '%':
            print('test2')
            F5 = db.engine.execute("""SELECT f.FEDERATION_NAME,f.FEDERATION_CREATED_DATE,a.COUNTRY,a.CITY FROM FEDERATION f
                                INNER JOIN ADDRESS a ON f.ID_FEDERATION=a.ID_FEDERATION
                                WHERE a.CITY like'""" + str(city) + "%'")
            data = [i for i in F5]
            return render_template('FindFederation.html', form=form, data=data)
        elif continent[0] == '%' and city == '%' and country[0] != '%':
            print('test3')
            F5 = db.engine.execute("""SELECT f.FEDERATION_NAME,f.FEDERATION_CREATED_DATE,a.COUNTRY,a.CITY FROM FEDERATION f
                            INNER JOIN ADDRESS a ON f.ID_FEDERATION=a.ID_FEDERATION
                            WHERE  a.COUNTRY like '""" + country[0] + "'")
            data = [i for i in F5]
            return render_template('FindFederation.html', form=form, data=data, UserAccountType=UserAccountType)
    return render_template('FindFederation.html', form=form, UserAccountType=UserAccountType)


@app.route('/FederationFighters', methods=['GET', 'POST'])
@login_required
def FederationFighters():
    UserAccountType = CurrentAccountType(current_user.USERNAME)
    form = CheckTeam()
    fight_status = form.FIGHT_STATUS.data,
    health_status = form.HEALTH_STATUS.data,

    if form.validate_on_submit():
        name = current_user.USERNAME
        query = USER.query.filter_by(USERNAME=name).first()
        id_federation = query.FEDERATION.ID_FEDERATION
        print('ID_MANAGER: ' + str(id_federation))

        # Wyciagmy liste fighterow
        F5 = db.engine.execute("""SELECT ID_FIGHTER FROM FIGHTER_FEDERATION
             WHERE ID_FEDERATION=""" + str(id_federation))
        list = [i for i in F5]
        id_fighter_list = [str(i[0]) for i in list]
        print('ID_FIGHTER nunumbers belong to ID_FEDERATION ' + str(id_federation))

        fighters_id = ''.join(["'" + i + "'" + "," for i in id_fighter_list])
        print(fighters_id)

        # Wyciągamy listę walk fighterów
        F5 = db.engine.execute("""SELECT e.EVENT_NAME,f.WEIGHT_CATEGORY,e.DATE,ff.ID_FIGHTER FROM EVENTS e 
        LEFT JOIN FIGHT f ON f.ID_EVENT=e.ID_EVENT
        LEFT JOIN FIGHTER_FIGHTS ff ON ff.ID_FIGHT=f.ID_FIGHT
        WHERE ff.ID_FIGHTER IN(""" + fighters_id[:-1] + ")")
        Fights = [i for i in F5]
        print(Fights)

        print(fighters_id[:-1])
        print(health_status[0])
        print(fight_status[0])

        F5 = db.engine.execute("""SELECT DISTINCT f.ID_FIGHTER,f.NAME,f.NICKNAME,f.SURNAME,fd.HEALTH_STATUS,fd.READY_TO_FIGHT_DATE,e.EVENT_NAME,fd.WEIGHT_CATEGORY,e.DATE FROM FIGHTER f
                   LEFT JOIN FIGHTER_DETAILS fd ON f.ID_FIGHTER=fd.ID_FIGHTER
                   LEFT JOIN FIGHTER_MANAGER fm ON fm.ID_FIGHTER=f.ID_FIGHTER
                   LEFT JOIN FIGHTER_FIGHTS ff ON ff.ID_FIGHTER=f.ID_FIGHTER
                   LEFT JOIN FIGHT fi ON fi.ID_FIGHT=ff.ID_FIGHT
                   LEFT JOIN EVENTS e ON e.ID_EVENT=fi.ID_EVENT
                   WHERE f.ID_FIGHTER IN (""" + fighters_id[:-1] + ")" + """ AND fd.HEALTH_STATUS=""" + "'" + str(
            health_status[0]) + "'" + """AND fd.FIGHT_STATUS=""" + "'" + str(fight_status[0]) + "'")
        list = [i for i in F5]
        print('list')
        print(list)

        return render_template('FederationFighters.html', form=form, data=list, UserAccountType=UserAccountType)
    return render_template('FederationFighters.html', form=form, UserAccountType=UserAccountType)

@app.route('/FireFighters', methods=['GET', 'POST'])
@login_required
def FireFighters():
    UserAccountType = CurrentAccountType(current_user.USERNAME)
    form = CheckTeam()
    # fight_status = form.FIGHT_STATUS.data,
    # health_status = form.HEALTH_STATUS.data,

    name = current_user.USERNAME
    query = USER.query.filter_by(USERNAME=name).first()
    account_type = query.ACCOUNT_TYPE
    if account_type == 'Manager':
        # id_manager = query.MANAGER.ID_MANAGER
        # F5 = db.engine.execute("""SELECT DISTINCT f.ID_FIGHTER,f.NAME,f.NICKNAME,f.SURNAME,fd.HEALTH_STATUS,fd.READY_TO_FIGHT_DATE,e.EVENT_NAME,fi.WEIGHT_CATEGORY,e.DATE,e.ID_EVENT,ff.ID_FIGHT FROM FIGHTER f
        #                 LEFT JOIN FIGHTER_DETAILS fd ON f.ID_FIGHTER=fd.ID_FIGHTER
        #                 LEFT JOIN FIGHTER_MANAGER fm ON fm.ID_FIGHTER=f.ID_FIGHTER
        #                 LEFT JOIN FIGHTER_FIGHTS ff ON ff.ID_FIGHTER=f.ID_FIGHTER
        #                 LEFT JOIN FIGHT fi ON fi.ID_FIGHT=ff.ID_FIGHT
        #                 LEFT JOIN EVENTS e ON e.ID_EVENT=fi.ID_EVENT
        #                 WHERE fm.ID_MANAGER='""" + str(id_manager) + "' AND f.ID_FIGHTER<>'110'")
        # data = [i for i in F5]
        # print(data)
        id_manager = query.MANAGER.ID_MANAGER
        F5 = db.engine.execute("""SELECT DISTINCT f.ID_FIGHTER,f.NAME,f.NICKNAME,f.SURNAME,fd.HEALTH_STATUS,fd.WEIGHT_CATEGORY FROM FIGHTER f
                        LEFT JOIN FIGHTER_DETAILS fd ON f.ID_FIGHTER=fd.ID_FIGHTER
                        LEFT JOIN FIGHTER_MANAGER fm ON fm.ID_FIGHTER=f.ID_FIGHTER
                        WHERE fm.ID_MANAGER='""" + str(id_manager) + "' AND f.ID_FIGHTER<>'110'")
        data = [i for i in F5]
        print(data)

    elif account_type == 'Federation':
        id_federation = query.FEDERATION.ID_FEDERATION
        F5 = db.engine.execute("""SELECT DISTINCT f.ID_FIGHTER,f.NAME,f.NICKNAME,f.SURNAME,fd.HEALTH_STATUS,fd.WEIGHT_CATEGORY FROM FIGHTER f
                        LEFT JOIN FIGHTER_DETAILS fd ON f.ID_FIGHTER=fd.ID_FIGHTER
                        LEFT JOIN FIGHTER_FEDERATION fed ON fed.ID_FIGHTER=f.ID_FIGHTER
                        WHERE fed.ID_FEDERATION='""" + str(id_federation) + "' AND f.ID_FIGHTER<>'110'")
        data = [[i.ID_FIGHTER,i.NAME,i.NICKNAME,i.SURNAME,i.HEALTH_STATUS,i.WEIGHT_CATEGORY] for i in F5]
        print(data)


    return render_template('FireFighters.html', form=form, data=data, UserAccountType=UserAccountType)


@app.route('/fireFighter', methods=['POST'])
def fireFighter():
    print('jsonify POST')
    name = current_user.USERNAME
    query = USER.query.filter_by(USERNAME=name).first()
    account_type = query.ACCOUNT_TYPE
    id_fighter = request.form['id_fighter']
    print("""ID_FIGHTER: """ + str(id_fighter))
    if account_type == 'Manager':
        F5 = db.engine.execute("""DELETE FROM FIGHTER_MANAGER WHERE ID_FIGHTER='""" + id_fighter + "'")
        q = FIGHTER_DETAILS.query.filter_by(ID_FIGHTER=id_fighter).first()
        q.MANAGER_NEED = """Yes"""
        db.session.commit()
        gc.collect()
    elif account_type == 'Federation':
        F5 = db.engine.execute("""DELETE FROM FIGHTER_FEDERATION WHERE ID_FIGHTER='""" + id_fighter + "'")
        q = FIGHTER_DETAILS.query.filter_by(ID_FIGHTER=id_fighter).first()
        q.FREE_AGENT = """Yes"""
        db.session.commit()
        gc.collect()
    print('Fighter has been deleted and status has been changed (MANAGER_NEED or FREE_AGENT)')



    return jsonify({'result': 'success'})


@app.route('/SearchEventsFederation', methods=['GET', 'POST'])
@login_required
def SearchEventsFederation():
    UserAccountType = CurrentAccountType(current_user.USERNAME)
    form = SearchEvent()
    continent = form.CONTINENT.data
    country = form.COUNTRY.data
    weight_category = form.WEIGHT_CATEGORY.data
    today = time.strftime("%d/%m/%Y")
    test = datetime.datetime.strptime(today, '%d/%m/%Y')
    toDay = test.strftime('%Y-%m-%d')


    F5 = db.engine.execute(
        """SELECT DISTINCT fed.FEDERATION_NAME,even.EVENT_NAME,even.CONTINENT,even.COUNTRY,even.CITY,even.DATE,even.ID_EVENT FROM FEDERATION fed
        INNER JOIN EVENTS even ON even.ID_FEDERATION=fed.ID_FEDERATION
        ORDER BY even.DATE DESC""")
    all_event = [[i.FEDERATION_NAME, i.EVENT_NAME, i.CONTINENT, i.COUNTRY, i.CITY, i.DATE, i.ID_EVENT] for i in F5]
    print('Events list')
    actuall_event=[i for i in all_event if parse(i[5])>=parse(toDay)]
    print(actuall_event)

    if request.method == 'POST':
        continent = form.CONTINENT.data
        print(continent)
        country = form.COUNTRY.data
        print(country)
        weight_category = form.WEIGHT_CATEGORY.data
        print(weight_category)
        date_ev = form.dt.data
        date_ev = str(date_ev)
        print(type(date_ev))
        date_ev = date_ev[8:10] + "/" + date_ev[5:7] + "/" + date_ev[0:4]
        print('dlugosc daty')
        print(len(date_ev))

        print('continent ' + continent)
        print('country ' + country)
        print('weight ' + weight_category)
        print('date ' + date_ev)

        if continent != '%' and country != '%' and weight_category != '%' and len(date_ev) == 6:
            F5 = db.engine.execute(
                """SELECT distinct fed.FEDERATION_NAME,even.EVENT_NAME,even.CONTINENT,even.COUNTRY,even.CITY,even.DATE,even.ID_EVENT FROM FEDERATION fed
                INNER JOIN EVENTS even ON even.ID_FEDERATION=fed.ID_FEDERATION
                WHERE even.CONTINENT like '""" + continent + """%' AND even.COUNTRY like '""" + country +
                """%'  AND WEIGHT_CATEGORY like '""" + weight_category + """%' ORDER BY f.ID_FIGHT DESC""")
            list = [[i.FEDERATION_NAME, i.EVENT_NAME, i.CONTINENT, i.COUNTRY, i.CITY, i.DATE,i.ID_EVENT] for i in F5]
            print('Events list')
            print(list)
        # bierzemy pod uwage takze date wydarzenia
        else:
            F5 = db.engine.execute(
                """SELECT distinct fed.FEDERATION_NAME,even.EVENT_NAME,even.CONTINENT,even.COUNTRY,even.CITY,even.DATE,even.ID_EVENT FROM FEDERATION fed
                INNER JOIN EVENTS even ON even.ID_FEDERATION=fed.ID_FEDERATION
                INNER JOIN FIGHT f ON f.ID_EVENT=even.ID_EVENT
                INNER JOIN FIGHTER_FIGHTS ff ON ff.ID_FIGHT=f.ID_FIGHT
                WHERE even.CONTINENT like '""" + continent + """%' AND even.COUNTRY like '""" + country +
                """%'  AND WEIGHT_CATEGORY like '""" + weight_category + """%' AND even.DATE >= '""" + date_ev + """' ORDER BY f.ID_FIGHT DESC""")
            list = [[i.FEDERATION_NAME, i.EVENT_NAME, i.CONTINENT, i.COUNTRY, i.CITY, i.DATE,i.ID_EVENT] for i in F5]
            print('Events list')
            print(list)

        event_list = []
        r1 = 0
        r2 = 0

        return render_template('SearchEventsFederation.html', form=form, data=list, UserAccountType=UserAccountType)
    return render_template('SearchEventsFederation.html', form=form, data=actuall_event, UserAccountType=UserAccountType)

if __name__ == '__main__':
    app.run(debug=True, port=81)
