from flask import Flask, render_template, request,url_for,redirect, session, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
import gc

from wtforms import StringField, PasswordField, BooleanField, SelectField,TextField,validators
from flask_wtf import FlaskForm

app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] =  r'sqlite:///C:/Users/Me/Desktop/Litchi/db/Litchi.db'
db = SQLAlchemy(app)

class SportForm(FlaskForm):
    sport_name = StringField('sport_name')

class USER(db.Model):
    __tablename__ = 'user'
    ID_USER = db.Column(db.Integer, primary_key=True)
    ID_ACCOUNT_TYPE = db.Column(db.Integer)
    LOGIN = db.Column(db.String(25), unique=True)
    PASSWORD = db.Column(db.String(100))
    E_MAIL = db.Column(db.String(45), unique=True)
    CREATE_DATE=db.Column(db.String(10))
    CREATE_TIME=db.Column(db.String(8))


class SPORT(db.Model):
    __tablename__ = 'sport'
    ID_SPORT = db.Column(db.Integer, primary_key=True)
    SPORT_NAME = db.Column(db.String(30), unique=True)


class COUNTRY(db.Model):
    __tablename__ = 'country'
    ID_COUNTRY = db.Column(db.Integer, primary_key=True)
    COUNTRY_NAME = db.Column(db.String(44), unique=True)


class PM_MESSAGE(db.Model):
    __tablename__ = 'pm_message'
    ID_USER = db.Column(db.Integer)
    ID_TOPIC_TYPE = db.Column(db.Integer, primary_key=True)
    DATA_MESSAGE = db.Column(db.String(26))
    TOPIC = db.Column(db.String(40))
    MESSAGE = db.Column(db.String(400))


class TOPIC_TYPE(db.Model):
    __tablename__ = 'topic_type'
    ID_TOPIC_TYPE = db.Column(db.Integer, primary_key=True)
    TOPIC_TYPE = db.Column(db.String(50), unique=True)


class CLUB(db.Model):
    __tablename__ = 'manager'
    ID_CLUB = db.Column(db.Integer, primary_key=True)
    ID_FIGHTER = db.Column(db.Integer)
    ID_ACCOUNT_TYPE = db.Column(db.Integer)
    ID_COUNTRY = db.Column(db.Integer)
    ID_USER = db.Column(db.Integer)
    CLUB_NAME = db.Column(db.String(45))
    NAME = db.Column(db.String(45))
    SURNAME = db.Column(db.String(45))
    CITY = db.Column(db.String(45))
    ZIP_CODE = db.Column(db.String(7))
    STREET = db.Column(db.String(45))
    STREET_NUMBER = db.Column(db.String(10))
    PHONE_NUMBER = db.Column(db.String(20))
    PHONE_NUMBER2 = db.Column(db.String(20))
    E_MAIL = db.Column(db.String(45))
    ID_PAYMENT = db.Column(db.Integer)
    CREATION_DATE = db.Column(db.DateTime)
    OUT_OF_DATE = db.Column(db.DateTime)
    ID_DOCUMENT = db.Column(db.Integer)


class FIHGTER_MANAGER(db.Model):
    __tablename__ = 'fighter_manager'
    ID_FIGHTER_MANAGER = db.Column(db.Integer, primary_key=True)
    ID_FIGHTER = db.Column(db.Integer)
    ID_ACCOUNT_TYPE = db.Column(db.Integer)
    ID_USER = db.Column(db.Integer)
    ID_EVENT = db.Column(db.Integer)
    NAME = db.Column(db.String(45))
    SURNAME = db.Column(db.String(45))
    PHONE_NUMBER = db.Column(db.String(20))
    PHONE_NUMBER2 = db.Column(db.String(20))
    E_MAIL = db.Column(db.String(45))
    ID_PAYMENT = db.Column(db.Integer)
    CREATION_DATE = db.Column(db.DateTime)
    OUT_OF_DATE = db.Column(db.DateTime)
    ID_DOCUMENT = db.Column(db.Integer)


class FIGHTER_DETAILS(db.Model):
    __tablename__ = 'fighter_details'
    ID_FIGHTER = db.Column(db.Integer, primary_key=True)
    ID_SPORT = db.Column(db.Integer)
    ID_EVENT = db.Column(db.Integer)
    WEIGHT_CATEGORY = db.Column(db.String(6))
    HEIGHT = db.Column(db.String(5))
    FIGHT_STATUS = db.Column(db.Boolean)
    HEALTH_STATUS = db.Column(db.Boolean)
    HEALTH_DESCRIPTION = db.Column(db.String(400))
    ID_COUNTRY_ACTUAL = db.Column(db.Integer)


class FIGHT_HISTORY(db.Model):
    __tablename__ = 'fight_history'
    ID_FIGHT_HISTORY = db.Column(db.Integer, primary_key=True)
    ID_FIGHTER_1 = db.Column(db.Integer)
    ID_FIGHTER_2 = db.Column(db.Integer)
    DATE = db.Column(db.DateTime)
    FIGHT_TIME = db.Column(db.Time)
    SCORE_1 = db.Column(db.Boolean)
    SCORE_2 = db.Column(db.Boolean)
    ID_FIGHT_END_BY = db.Column(db.Integer)
    ROUND = db.Column(db.Numeric(2))


class FIGHT_FINISH(db.Model):
    __tablename__ = 'fight_finish'
    ID_FIGHT_END_BY = db.Column(db.Integer, primary_key=True)
    FIGHT_END_BY = db.Column(db.String(45), unique=True)


class FIGHTER(db.Model):
    __tablename__ = 'fighter'
    ID_FIGHTER = db.Column(db.Integer, primary_key=True)
    ID_FIGHTER_MANAGER = db.Column(db.Integer)
    ID_ACCOUNT_TYPE = db.Column(db.Integer)
    ID_USER = db.Column(db.Integer)
    ID_EVENT = db.Column(db.Integer)
    ID_CLUB = db.Column(db.Integer)
    ID_FEDERATION = db.Column(db.Integer)
    NAME = db.Column(db.String(45))
    SURNAME = db.Column(db.String(45))
    PHONE_NUMBER = db.Column(db.String(20))
    PHONE_NUMBER2 = db.Column(db.String(20))
    E_MAIL = db.Column(db.String(45))
    ID_PAYMENT = db.Column(db.Integer)
    CREATION_DATE = db.Column(db.DateTime)
    OUT_OF_DATE = db.Column(db.DateTime)
    ID_DOCUMENT = db.Column(db.Integer)


class FEDERATION(db.Model):
    __tablename__ = 'federation'
    ID_FEDERATION = db.Column(db.Integer, primary_key=True)
    ID_FIGHTER_MANAGER = db.Column(db.Integer)
    ID_ACCOUNT_TYPE = db.Column(db.Integer)
    ID_USER = db.Column(db.Integer)
    ID_EVENT = db.Column(db.Integer)
    NAME = db.Column(db.String(45))
    SURNAME = db.Column(db.String(45))
    PHONE_NUMBER = db.Column(db.String(20))
    PHONE_NUMBER2 = db.Column(db.String(20))
    E_MAIL = db.Column(db.String(45))
    ID_PAYMENT = db.Column(db.Integer)
    CREATION_DATE = db.Column(db.DateTime)
    OUT_OF_DATE = db.Column(db.DateTime)
    ID_DOCUMENT = db.Column(db.Integer)


class PAYMENT_HISTORY(db.Model):
    __tablename__ = 'payment_history'
    ID_PAYMENT = db.Column(db.Integer, primary_key=True)
    ID_USER = db.Column(db.Integer)
    TRANSACTION_DATE = db.Column(db.DateTime)
    AMOUNT = db.Column(db.String(10))


class EVENT(db.Model):
    __tablename__ = 'event'
    ID_EVENT = db.Column(db.Integer, primary_key=True)
    ID_FIGHTER = db.Column(db.Integer)
    ID_FEDERATION = db.Column(db.Integer)
    ID_COUNTRY = db.Column(db.Integer)
    CITY = db.Column(db.String(45))
    ZIP_CODE = db.Column(db.String(7))
    STREET = db.Column(db.String(45))
    STREET_NUMBER = db.Column(db.String(10))
    DATE = db.Column(db.String(10))
    TIME = db.Column(db.String(8))
    NEED_FIGHTER_STATUS = db.Column(db.Boolean)


class USERS_PRIVATE_FILES(db.Model):
    __tablename__ = 'users_private_files'
    ID_DOCUMENT = db.Column(db.Integer, primary_key=True)
    ID_USER = db.Column(db.Integer)
    DOCUMENT = db.Column(db.String(100))
    IMAGE = db.Column(db.String(100))


class ADDRESS(db.Model):
    __tablename__ = 'address'
    ID_USER = db.Column(db.Integer, primary_key=True)
    ID_COUNTRY = db.Column(db.Integer)
    CITY = db.Column(db.String(45))
    ZIP_CODE = db.Column(db.String(7))
    STREET = db.Column(db.String(45))
    STREET_NUMBER = db.Column(db.String(10))


@app.route('/')
def index():
    return render_template('dashboard.html')


@app.route('/add/sport', methods=['GET', 'POST'])
def Sport():
    form = SportForm()

    if form.validate_on_submit():
        return "it works"
    return render_template('SportForm.html',form=form)



# @app.route('/login', methods=["POST","GET"])
# def login():
#     error=""
#     try:
#         if request.method == 'POST':
#
#             attempted_username = request.form['username']
#             attempted_password = request.form['password']
#
#             if attempted_username == "admin" and attempted_password == "password":
#                 return redirect(url_for('dashboard'))
#
#             else:
#                 error = "Invalid credentials. Try Again."
#         return render_template('login.html',error=error)
#     except Exception as e:
#         return render_template("login.html", error=error)
#
# @app.route('/register')
# def register_page():
#     try:
#         form = RegisterForm(request.form)
#         if request.method == "POST" and form.validate():
#             username = form.username.data
#             email = form.email.data
#             password = sha256_crypt.encrypt((str(form.password.data)))
#             accounttype = form.accounttype.data
#             new_user = User(username=form.username.data, email=form.email.data, password=sha256_crypt.encrypt((str(form.password.data))))
#             db.session.add(new_user)
#             db.session.commit()
#             flash("Thank You for registration")
#             gc.collect
#             session['logged_in']=True
#             session['username'] = username
#
#             return redirect(url_for(' '))
#         return render_template("register.html",form=form)
#     except Exception as e:
#         return(str(e))

@app.route('/dashboard/')
def dashboard():
    return render_template('dashboard.html')

# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template("404.html")

if __name__ == '__main__':
    app.run(debug=True)