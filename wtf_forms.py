from flask_wtf import FlaskForm
from app import InputRequired,validators,Length,StringField,Email,PasswordField,SelectField,BooleanField

InvalidUsernameList=["username","user","admin"]
InvalidPasswordList=["password","1234","123","admin","admin123","123456","123456789"]


class SportForm(FlaskForm):
    sport_name = StringField('sport_name')


class LoginForm(FlaskForm):
    USERNAME = StringField('username',validators=[InputRequired(),Length(min=4,max=15)])
    PASSWORD = PasswordField('password',validators=[InputRequired(),Length(min=3,max=80)])
    REMEMBER = BooleanField('remember me')

# AccountForm jest dla managera,fightera i SEO
class AccountForm(FlaskForm):
    NAME = StringField(u'Name',validators=[InputRequired(), Length(min=3, max=30)])
    SURNAME = StringField(u'Surname',validators=[InputRequired(),Length(min = 1, max=45)])
    CITY = StringField(u'City',validators=[InputRequired(),Length(min = 1, max=45)])
    ZIP_CODE = StringField(u'Zip-code',validators=[InputRequired(),Length(min = 1, max=7)])
    STREET = StringField(u'Street',validators=[InputRequired(),Length(min = 1, max=45)])
    STREET_NUMBER = StringField(u'Street number',validators=[InputRequired(),Length(min = 1, max=5)])
    PHONE_NUMBER = StringField(u'Phone number 1',validators=[InputRequired(),Length(min = 6, max=20)])
    PHONE_NUMBER2 = StringField(u'Phone number 2 (optional)',validators=[Length(min = 6, max=20)])
    E_MAIL = StringField(u'Email Address',validators=[InputRequired(),Length(min = 5, max = 40),Email(message=u'Invalid email address.')])

#

#
