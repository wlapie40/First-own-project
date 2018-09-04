# class UserForm(FlaskForm):
#     username = StringField(u'Username',[validators.Required(),validators.Length(min = 4, max = 30),validators.NoneOf(InvalidUsernameList,message=u"Invalid value")])
#     email = StringField(u'Email Address',[validators.Required(),validators.Length(min = 6, max = 40), validators.Email(message=u'Invalid email address.')])
#     password = PasswordField(u'Password',[validators.Required(),validators.NoneOf(InvalidPasswordList,message=u"Invalid value"),validators.Length(min = 6, max = 50)])
#     confirm = PasswordField(u'Repeat Password')
#     accounttype = SelectField(u'Account type',[validators.Required()],choices=['Standard user','Fighter','Manager','CEO'],coerce=int)
#     accept_tos = BooleanField(u'I accept the <ahref="/tos/">Terms of Service</a> and the <a href="/privacy/"> Privacy Notice</a> (Last updated Sunday, 9 April 2017)',[validators.Required])
#
# class SportForm(FlaskForm):
#     sport_name = StringField('sport_name')
#
#
# class LoginForm(FlaskForm):
#     username = StringField('username')
#     password = PasswordField('password')
#
#
# # AccountForm jest dla managera,fightera i SEO
# class AccountForm(FlaskForm):
#     # ID_ACCOUNT_TYPE = StringField()
#     # ID_COUNTRY = StringField()
#     # ID_USER = StringField()
#     NAME = StringField(u'Name',validators=[InputRequired(), Length(min=4, max=15)])
#     SURNAME = StringField(u'Surname',validators=[InputRequired(),Length(min = 1, max=45)])
#     COUNTRY = StringField(u'Country', validators=[InputRequired(), Length(min=1, max=45)])
#     CITY = StringField(u'City',validators=[InputRequired(),Length(min = 1, max=45)])
#     ZIP_CODE = StringField(u'Zip-code',validators=[InputRequired(),Length(min = 1, max=7)])
#     STREET = StringField(u'Street',validators=[InputRequired(),Length(min = 1, max=45)])
#     STREET_NUMBER = StringField(u'Street number',validators=[InputRequired(),Length(min = 1, max=10)])
#     PHONE_NUMBER = StringField(u'Phone number 1',validators=[InputRequired(),Length(min = 6, max=20)])
#     PHONE_NUMBER2 = StringField(u'Phone number 2',validators=[Length(min = 6, max=20)])
#     E_MAIL = StringField(u'Email Address',validators=[InputRequired(),Length(min = 6, max = 40),Email(message=u'Invalid email address.')])
#
# class USER(db.Model):
#     ID_USER = db.Column(db.Integer, primary_key=True)
#     LOGIN = db.Column(db.String(25), unique=True)
#     PASSWORD = db.Column(db.String(100))
#     E_MAIL = db.Column(db.String(45), unique=True)
#     CREATE_DATE=db.Column(db.String(10))
#     CREATE_TIME=db.Column(db.String(8))
#
#
# class SPORT(db.Model):
#     __tablename__ = 'sport'
#     ID_SPORT = db.Column(db.Integer(), primary_key=True)
#     SPORT_NAME = db.Column(db.String(30), unique=True)
#
# class COUNTRY(db.Model):
#     __tablename__ = 'country'
#     ID_SPORT = db.Column(db.Integer(), primary_key=True)
#     COUNTRY_NAME = db.Column(db.String(44), unique=True)
#     COUNTRY_ISO = db.Column(db.String(3), unique=True)
#
#
# class PM_MESSAGE(db.Model):
#     __tablename__ = 'pm_message'
#     ID_USER = db.Column(db.Integer)
#     ID_TOPIC_TYPE = db.Column(db.Integer, primary_key=True)
#     DATA_MESSAGE = db.Column(db.String(26))
#     TOPIC = db.Column(db.String(40))
#     MESSAGE = db.Column(db.String(400))
#
#
# class TOPIC_TYPE(db.Model):
#     __tablename__ = 'topic_type'
#     ID_TOPIC_TYPE = db.Column(db.Integer, primary_key=True)
#     TOPIC_TYPE = db.Column(db.String(50), unique=True)
#
# class ACCOUNT_TYPE(db.Model):
#     __tablename__ = 'account_type'
#     ID_ACCOUNT_TYPE = db.Column(db.Integer, primary_key=True)
#     ACCOUNT_TYPE = db.Column(db.String(50), unique=True)
#
#
# class CLUB(db.Model):
#     __tablename__ = 'manager'
#     ID_CLUB = db.Column(db.Integer, primary_key=True)
#     # ID_FIGHTER = db.Column(db.Integer)
#     # ID_ACCOUNT_TYPE = db.Column(db.Integer)
#     # ID_COUNTRY = db.Column(db.Integer)
#     # ID_USER = db.Column(db.Integer)
#     CLUB_NAME = db.Column(db.String(45))
#     NAME = db.Column(db.String(45))
#     SURNAME = db.Column(db.String(45))
#     CITY = db.Column(db.String(45))
#     ZIP_CODE = db.Column(db.String(7))
#     STREET = db.Column(db.String(45))
#     STREET_NUMBER = db.Column(db.String(10))
#     PHONE_NUMBER = db.Column(db.String(20))
#     PHONE_NUMBER2 = db.Column(db.String(20))
#     E_MAIL = db.Column(db.String(45))
#     ID_PAYMENT = db.Column(db.Integer)
#     CREATION_DATE = db.Column(db.DateTime)
#     OUT_OF_DATE = db.Column(db.DateTime)
#     ID_DOCUMENT = db.Column(db.Integer)
#
#
# class FIHGTER_MANAGER(db.Model):
#     __tablename__ = 'fighter_manager'
#     ID_FIGHTER_MANAGER = db.Column(db.Integer, primary_key=True)
#     ID_FIGHTER = db.Column(db.Integer)
#     ID_ACCOUNT_TYPE = db.Column(db.Integer)
#     ID_USER = db.Column(db.Integer)
#     ID_EVENT = db.Column(db.Integer)
#     NAME = db.Column(db.String(45))
#     SURNAME = db.Column(db.String(45))
#     PHONE_NUMBER = db.Column(db.String(20))
#     PHONE_NUMBER2 = db.Column(db.String(20))
#     E_MAIL = db.Column(db.String(45))
#     COUNTRY = db.Column(db.String(45))
#     ID_PAYMENT = db.Column(db.Integer)
#     CREATION_DATE = db.Column(db.DateTime)
#     OUT_OF_DATE = db.Column(db.DateTime)
#     ID_DOCUMENT = db.Column(db.Integer)
#
#
# class FIGHTER_DETAILS(db.Model):
#     __tablename__ = 'fighter_details'
#     ID_FIGHTER = db.Column(db.Integer, primary_key=True)
#     ID_SPORT = db.Column(db.Integer)
#     ID_EVENT = db.Column(db.Integer)
#     WEIGHT_CATEGORY = db.Column(db.String(6))
#     HEIGHT = db.Column(db.String(5))
#     FIGHT_STATUS = db.Column(db.Boolean)
#     HEALTH_STATUS = db.Column(db.Boolean)
#     HEALTH_DESCRIPTION = db.Column(db.String(400))
#     ID_COUNTRY_ACTUAL = db.Column(db.Integer)
#
#
# class FIGHT_HISTORY(db.Model):
#     __tablename__ = 'fight_history'
#     ID_FIGHT_HISTORY = db.Column(db.Integer, primary_key=True)
#     ID_FIGHTER_1 = db.Column(db.Integer)
#     ID_FIGHTER_2 = db.Column(db.Integer)
#     DATE = db.Column(db.DateTime)
#     FIGHT_TIME = db.Column(db.Time)
#     SCORE_1 = db.Column(db.Boolean)
#     SCORE_2 = db.Column(db.Boolean)
#     ID_FIGHT_END_BY = db.Column(db.Integer)
#     ROUND = db.Column(db.Numeric(2))
#
#
# class FIGHT_FINISH(db.Model):
#     __tablename__ = 'fight_finish'
#     ID_FIGHT_END_BY = db.Column(db.Integer, primary_key=True)
#     FIGHT_END_BY = db.Column(db.String(45), unique=True)
#
#
# class FIGHTER(db.Model):
#     ID_FIGHTER = db.Column(db.Integer, primary_key=True)
#     NAME = db.Column(db.String(45))
#     SURNAME = db.Column(db.String(45))
#     CREATION_DATE = db.Column(db.DateTime)
#     OUT_OF_DATE = db.Column(db.DateTime)
#     ID_DOCUMENT = db.Column(db.Integer)
#
#     ADDRESS = db.relationship('ADDRESS',backref='FIGHTER',lazy='dynamic')
#
# class ADDRESS(db.Model):
#     ID_ADDRESS = db.Column(db.Integer, primary_key=True)
#     COUNTRY = db.Column(db.String(45))
#     CITY = db.Column(db.String(45))
#     ZIP_CODE = db.Column(db.String(7))
#     STREET = db.Column(db.String(45))
#     STREET_NUMBER = db.Column(db.String(10))
#     ID_FIGHTER = db.Column(db.Integer,db.ForeignKey('ID_FIGHTER'))
#
# class CONTACT(db.Model):
#     ID_CONTACT = db.Column(db.Integer, primary_key=True)
#     PHONE_NUMBER = db.Column(db.String(20))
#     PHONE_NUMBER2 = db.Column(db.String(20))
#     E_MAIL = db.Column(db.String(45))
#
#
#
# class FEDERATION(db.Model):
#     __tablename__ = 'federation'
#     ID_FEDERATION = db.Column(db.Integer, primary_key=True)
#     ID_FIGHTER_MANAGER = db.Column(db.Integer)
#     ID_ACCOUNT_TYPE = db.Column(db.Integer)
#     ID_USER = db.Column(db.Integer)
#     ID_EVENT = db.Column(db.Integer)
#     NAME = db.Column(db.String(45))
#     SURNAME = db.Column(db.String(45))
#     PHONE_NUMBER = db.Column(db.String(20))
#     PHONE_NUMBER2 = db.Column(db.String(20))
#     E_MAIL = db.Column(db.String(45))
#     COUNTRY = db.Column(db.String(45))
#     ID_PAYMENT = db.Column(db.Integer)
#     CREATION_DATE = db.Column(db.DateTime)
#     OUT_OF_DATE = db.Column(db.DateTime)
#     ID_DOCUMENT = db.Column(db.Integer)
#
#
# class PAYMENT_HISTORY(db.Model):
#     __tablename__ = 'payment_history'
#     ID_PAYMENT = db.Column(db.Integer, primary_key=True)
#     ID_USER = db.Column(db.Integer)
#     TRANSACTION_DATE = db.Column(db.DateTime)
#     AMOUNT = db.Column(db.String(10))
#
#
# class EVENT(db.Model):
#     __tablename__ = 'event'
#     ID_EVENT = db.Column(db.Integer, primary_key=True)
#     ID_FIGHTER = db.Column(db.Integer)
#     ID_FEDERATION = db.Column(db.Integer)
#     ID_COUNTRY = db.Column(db.Integer)
#     CITY = db.Column(db.String(45))
#     ZIP_CODE = db.Column(db.String(7))
#     STREET = db.Column(db.String(45))
#     STREET_NUMBER = db.Column(db.String(10))
#     DATE = db.Column(db.String(10))
#     TIME = db.Column(db.String(8))
#     NEED_FIGHTER_STATUS = db.Column(db.Boolean)
#
#
# class USERS_PRIVATE_FILES(db.Model):
#     __tablename__ = 'users_private_files'
#     ID_DOCUMENT = db.Column(db.Integer, primary_key=True)
#     ID_USER = db.Column(db.Integer)
#     DOCUMENT = db.Column(db.String(100))
#     IMAGE = db.Column(db.String(100))
