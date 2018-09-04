

class USER(db.Model):
    __tablename__ = 'user'
    ID_USER = db.Column(db.Integer, primary_key=True)
    ID_ACCOUNT_TYPE = db.Column(db.Integer)
    LOGIN = db.Column(db.String(45), unique=True)
    PASSWORD = db.Column(db.String(100))
    E_MAIL = db.Column(db.String(45), unique=True)


class SPORT(db.Model):
    __tablename__ = 'sport'
    ID_SPORT = db.Column(db.Integer, primary_key=True)
    SPORT_NAME = db.Column(db.String(50), unique=True)


class COUNTRY(db.Model):
    __tablename__ = 'country'
    ID_COUNTRY = db.Column(db.Integer, primary_key=True)
    COUNTRY_NAME = db.Column(db.String(50), unique=True)


class PM_MESSAGE(db.Model):
    __tablename__ = 'pm_message'
    ID_USER = db.Column(db.Integer)
    ID_TOPIC_TYPE = db.Column(db.Integer, primary_key=True)
    DATA_MESSAGE = db.Column(db.DateTime)
    TOPIC = db.Column(db.String(45))
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
    PHONE_NUMBER = db.Column(db.String(11))
    PHONE_NUMBER2 = db.Column(db.String(11))
    E_MAIL = db.Column(db.String(45))
    ID_PAYMENT = db.Column(db.Integer)
    CREATION_DATE = db.Column(db.DateTime)
    OUT_OF_DATE = db.Column(db.DateTime)
    ID_DOCUMENT = db.Column(db.Integer)


class MANAGER(db.Model):
    __tablename__ = 'manager'
    ID_MANAGER = db.Column(db.Integer, primary_key=True)
    ID_FIGHTER = db.Column(db.Integer)
    ID_ACCOUNT_TYPE = db.Column(db.Integer)
    ID_USER = db.Column(db.Integer)
    ID_EVENT = db.Column(db.Integer)
    NAME = db.Column(db.String(45))
    SURNAME = db.Column(db.String(45))
    PHONE_NUMBER = db.Column(db.String(11))
    PHONE_NUMBER2 = db.Column(db.String(11))
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
    ID_MANAGER = db.Column(db.Integer)
    ID_ACCOUNT_TYPE = db.Column(db.Integer)
    ID_USER = db.Column(db.Integer)
    ID_EVENT = db.Column(db.Integer)
    ID_CLUB = db.Column(db.Integer)
    ID_FEDERATION = db.Column(db.Integer)
    NAME = db.Column(db.String(45))
    SURNAME = db.Column(db.String(45))
    PHONE_NUMBER = db.Column(db.String(11))
    PHONE_NUMBER2 = db.Column(db.String(11))
    E_MAIL = db.Column(db.String(45))
    ID_PAYMENT = db.Column(db.Integer)
    CREATION_DATE = db.Column(db.DateTime)
    OUT_OF_DATE = db.Column(db.DateTime)
    ID_DOCUMENT = db.Column(db.Integer)


class FEDERATION(db.Model):
    __tablename__ = 'federation'
    ID_FEDERATION = db.Column(db.Integer, primary_key=True)
    ID_MANAGER = db.Column(db.Integer)
    ID_ACCOUNT_TYPE = db.Column(db.Integer)
    ID_USER = db.Column(db.Integer)
    ID_EVENT = db.Column(db.Integer)
    NAME = db.Column(db.String(45))
    SURNAME = db.Column(db.String(45))
    PHONE_NUMBER = db.Column(db.String(11))
    PHONE_NUMBER2 = db.Column(db.String(11))
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
    DATE = db.Column(db.Date)
    TIME = db.Column(db.Time)
    NEED_FIGHTER_STATUS = db.Column(db.Boolean)


class USERS_FILES(db.Model):
    __tablename__ = 'users_files'
    ID_DOCUMENT = db.Column(db.Integer, primary_key=True)
    ID_USER = db.Column(db.Integer)
    DOCUMENT = db.Column(db.Blob)
    IMAGE = db.Column(db.Blob)


class ADDRESS(db.Model):
    ID_USER = db.Column(db.Integer)
    ID_COUNTRY = db.Column(db.Integer)
    CITY = db.Column(db.String(45))
    ZIP_CODE = db.Column(db.String(7))
    STREET = db.Column(db.String(45))
    STREET_NUMBER = db.Column(db.String(10))
