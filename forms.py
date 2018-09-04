from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField,TextField,DateField,TextAreaField,DateTimeField,SubmitField,HiddenField,widgets,SelectMultipleField
from wtforms.validators import InputRequired,Email,Length,NumberRange
from wtforms.ext.sqlalchemy.fields import QuerySelectField
# from app import TupleEvents
# DatePickerWidget
from DB import LOCALIZATION
TupleEventStatus = [('Finished','Finished'),('Pending','Pending'),('Incoming','Incoming')]
TupleSport = [('MMA','MMA'),('K1','K1'),('Boxing','Boxing'),('Kick-Boxing','Kick-Boxing')]
TupleContinentSearch = [('%','All'),('Asia','Asia'),('Africa','Africa'),('Australia','Australia'),('Europe','Europe'),('North America','North America'),('South America','South America')]
TupleContinent = [('Asia','Asia'),('Africa','Africa'),('Australia','Australia'),('Europe','Europe'),('North America','North America'),('South America','South America')]
TuplePreferFightStyle =[('Striker','Striker'),('Grappler','Grappler'),('Wrestler','Wrestler')]
TuplePreferFightStyleSearch =[('%','All'),('Striker','Striker'),('Grappler','Grappler'),('Wrestler','Wrestler')]
TupleACCOUNT_TYPE = [('Standard user','Standard user'),('Fighter','Fighter'),('Manager','Manager'),('Federation','Federation')]
TupleWeightCatMenSearch = [('%','All'),('Strawweight','Strawweight'),('Bantamweight','Bantamweight'),('Featherweight','Featherweight'),('Welterweight','Welterweight'),('Middleweight','Middleweight'),('Light heavyweight','Light heavyweight'),('Heavyweight','Heavyweight')]
TupleWeightCatMen = [('Strawweight','Strawweight'),('Bantamweight','Bantamweight'),('Featherweight','Featherweight'),('Welterweight','Welterweight'),('Middleweight','Middleweight'),('Light heavyweight','Light heavyweight'),('Heavyweight','Heavyweight')]
TupleWeightCatWom = [('Strawweight','Strawweight'),('Bantamweight','Bantamweight'),('Featherweight','FEATHERWEIGHT')]
TupleHealthCondition = [('Healthy','Healthy'),('Light injury','Light injury'),('Serious injury','Serious injury')]
TupleHealthConditionSearch = [('','Any health condition'),('Healthy','Healthy'),('Light injury','Light injury'),('Serious injury','Serious injury')]
TupleFightStatus = [('Looking for fight','Looking for fight'),('Maybe in the future','Maybe in the future'),('No fight','No fight')]
TupleFightStatusSearch = [('','All fight status'),('Looking for fight','Looking for fight'),('Maybe in the future','Maybe in the future'),('No fight','No fight')]
TupleCountrySearch =[('','All'),('Afghanistan','Afghanistan'),
('Aland Islands','Aland Islands'),
('Albania','Albania'),
('Algeria','Algeria'),
('American Samoa','American Samoa'),
('Andorra','Andorra'),
('Angola','Angola'),
('Anguilla','Anguilla'),
('Antarctica','Antarctica'),
('Antigua and Barbuda','Antigua and Barbuda'),
('Argentina','Argentina'),
('Armenia','Armenia'),
('Aruba' , 'Aruba') ,
('Australia','Australia'),
('Austria','Austria'),
('Azerbaijan','Azerbaijan'),
('Bahamas','Bahamas'),
('Bahrain','Bahrain'),
('Bangladesh','Bangladesh'),
('Barbados','Barbados'),
('Belarus','Belarus'),
('Belgium','Belgium'),
('Belize','Belize'),
('Benin','Benin'),
('Bermuda','Bermuda'),
('Bhutan','Bhutan'),
('Bolivia','Bolivia'),
('Bosnia and Herzegovina','Bosnia and Herzegovina'),
('Botswana','Botswana'),
('Bouvet Island','Bouvet Island'),
('Brazil','Brazil'),
('British Virgin Islands','British Virgin Islands'),
('British Indian Ocean Territory','British Indian Ocean Territory'),
('Brunei Darussalam','Brunei Darussalam'),
('Bulgaria','Bulgaria'),
('Burkina Faso','Burkina Faso'),
('Burundi','Burundi'),
('Cambodia','Cambodia'),
('Cameroon','Cameroon'),
('Canada','Canada'),
('Cape Verde','Cape Verde'),
('Cayman Islands','Cayman Islands'),
('Central African Republic','Central African Republic'),
('Chad','Chad'),
('Chile','Chile'),
('China','China'),
('Hong Kong, SAR China','Hong Kong, SAR China'),
('Macao, SAR China','Macao, SAR China'),
('Christmas Island','Christmas Island'),
('Cocos (Keeling) Islands','Cocos (Keeling) Islands'),
('Colombia','Colombia'),
('Comoros','Comoros'),
('Congo (Brazzaville)','Congo (Brazzaville)'),
('Congo, (Kinshasa)','Congo, (Kinshasa)'),
('Cook Islands','Cook Islands'),
('Costa Rica','Costa Rica'),
("Côte d'Ivoire","Côte d'Ivoire"),
('Croatia','Croatia'),
('Cuba','Cuba'),
('Cyprus','Cyprus'),
('Czech Republic','Czech Republic'),
('Denmark','Denmark'),
('Djibouti','Djibouti'),
('Dominica','Dominica'),
('Dominican Republic','Dominican Republic'),
('Ecuador','Ecuador'),
('Egypt','Egypt'),
('El Salvador','El Salvador'),
('Equatorial Guinea','Equatorial Guinea'),
('Eritrea','Eritrea'),
('Estonia','Estonia'),
('Ethiopia','Ethiopia'),
('Falkland Islands (Malvinas)','Falkland Islands (Malvinas)'),
('Faroe Islands','Faroe Islands'),
('Fiji','Fiji'),
('Finland','Finland'),
('France','France'),
('French Guiana','French Guiana'),
('French Polynesia','French Polynesia'),
('French Southern Territories','French Southern Territories'),
('Gabon','Gabon'),
('Gambia','Gambia'),
('Georgia','Georgia'),
('Germany','Germany'),
('Ghana','Ghana'),
('Gibraltar','Gibraltar'),
('Greece','Greece'),
('Greenland','Greenland'),
('Grenada','Grenada'),
('Guadeloupe','Guadeloupe'),
('Guam','Guam'),
('Guatemala','Guatemala'),
('Guernsey','Guernsey'),
('Guinea','Guinea'),
('Guinea-Bissau','Guinea-Bissau'),
('Guyana','Guyana'),
('Haiti','Haiti'),
('Heard and Mcdonald Islands','Heard and Mcdonald Islands'),
('Holy See (Vatican City State)','Holy See (Vatican City State)'),
('Honduras','Honduras'),
('Hungary','Hungary'),
('Iceland','Iceland'),
('India','India'),
('Indonesia','Indonesia'),
('Iran, Islamic Republic of','Iran, Islamic Republic of'),
('Iraq','Iraq'),
('Ireland','Ireland'),
('Isle of Man','Isle of Man'),
('Israel','Israel'),
('Italy','Italy'),
('Jamaica','Jamaica'),
('Japan','Japan'),
('Jersey','Jersey'),
('Jordan','Jordan'),
('Kazakhstan','Kazakhstan'),
('Kenya','Kenya'),
('Kiribati','Kiribati'),
('Korea (North)','Korea (North)'),
('Korea (South)','Korea (South)'),
('Kuwait','Kuwait'),
('Kyrgyzstan','Kyrgyzstan'),
('Lao PDR','Lao PDR'),
('Latvia','Latvia'),
('Lebanon','Lebanon'),
('Lesotho','Lesotho'),
('Liberia','Liberia'),
('Libya','Libya'),
('Liechtenstein','Liechtenstein'),
('Lithuania','Lithuania'),
('Luxembourg','Luxembourg'),
('Macedonia, Republic of','Macedonia, Republic of'),
('Madagascar','Madagascar'),
('Malawi','Malawi'),
('Malaysia','Malaysia'),
('Maldives','Maldives'),
('Mali','Mali'),
('Malta','Malta'),
('Marshall Islands','Marshall Islands'),
('Martinique','Martinique'),
('Mauritania','Mauritania'),
('Mauritius','Mauritius'),
('Mayotte','Mayotte'),
('Mexico','Mexico'),
('Micronesia, Federated States of','Micronesia, Federated States of'),
('Moldova','Moldova'),
('Monaco','Monaco'),
('Mongolia','Mongolia'),
('Montenegro','Montenegro'),
('Montserrat','Montserrat'),
('Morocco','Morocco'),
('Mozambique','Mozambique'),
('Myanmar','Myanmar'),
('Namibia','Namibia'),
('Nauru','Nauru'),
('Nepal','Nepal'),
('Netherlands','Netherlands'),
('Netherlands Antilles','Netherlands Antilles'),
('New Caledonia','New Caledonia'),
('New Zealand','New Zealand'),
('Nicaragua','Nicaragua'),
('Niger','Niger'),
('Nigeria','Nigeria'),
('Niue','Niue'),
('Norfolk Island','Norfolk Island'),
('Northern Mariana Islands','Northern Mariana Islands'),
('Norway','Norway'),
('Oman','Oman'),
('Pakistan','Pakistan'),
('Palau','Palau'),
('Palestinian Territory','Palestinian Territory'),
('Panama','Panama'),
('Papua New Guinea','Papua New Guinea'),
('Paraguay','Paraguay'),
('Peru','Peru'),
('Philippines','Philippines'),
('Pitcairn','Pitcairn'),
('Poland','Poland'),
('Portugal','Portugal'),
('Puerto Rico','Puerto Rico'),
('Qatar','Qatar'),
('Réunion','Réunion'),
('Romania','Romania'),
('Russian Federation','Russian Federation'),
('Rwanda','Rwanda'),
('Saint-Barthélemy','Saint-Barthélemy'),
('Saint Helena','Saint Helena'),
('Saint Kitts and Nevis','Saint Kitts and Nevis'),
('Saint Lucia','Saint Lucia'),
('Saint-Martin (French part)','Saint-Martin (French part)'),
('Saint Pierre and Miquelon','Saint Pierre and Miquelon'),
('Saint Vincent and Grenadines','Saint Vincent and Grenadines'),
('Samoa','Samoa'),
('San Marino','San Marino'),
('Sao Tome and Principe','Sao Tome and Principe'),
('Saudi Arabia','Saudi Arabia'),
('Senegal','Senegal'),
('Serbia','Serbia'),
('Seychelles','Seychelles'),
('Sierra Leone','Sierra Leone'),
('Singapore','Singapore'),
('Slovakia','Slovakia'),
('Slovenia','Slovenia'),
('Solomon Islands','Solomon Islands'),
('Somalia','Somalia'),
('South Africa','South Africa'),
('South Georgia and the South Sandwich Islands','South Georgia and the South Sandwich Islands'),
('South Sudan','South Sudan'),
('Spain','Spain'),
('Sri Lanka','Sri Lanka'),
('Sudan','Sudan'),
('Suriname','Suriname'),
('Svalbard and Jan Mayen Islands','Svalbard and Jan Mayen Islands'),
('Swaziland','Swaziland'),
('Sweden','Sweden'),
('Switzerland','Switzerland'),
('Syrian Arab Republic (Syria)','Syrian Arab Republic (Syria)'),
('Taiwan, Republic of China','Taiwan, Republic of China'),
('Tajikistan','Tajikistan'),
('Tanzania, United Republic of','Tanzania, United Republic of'),
('Thailand','Thailand'),
('Timor-Leste','Timor-Leste'),
('Togo','Togo'),
('Tokelau','Tokelau'),
('Tonga' , 'Tonga'),
('Trinidad and Tobago','Trinidad and Tobago'),
('Tunisia','Tunisia'),
('Turkey','Turkey'),
('Turkmenistan','Turkmenistan'),
('Turks and Caicos Islands','Turks and Caicos Islands'),
('Tuvalu','Tuvalu'),
('Uganda','Uganda'),
('Ukraine','Ukraine'),
('United Arab Emirates','United Arab Emirates'),
('United Kingdom','United Kingdom'),
('United States of America','United States of America'),
('US Minor Outlying Islands','US Minor Outlying Islands'),
('Uruguay','Uruguay'),
('Uzbekistan','Uzbekistan'),
('Vanuatu','Vanuatu'),
('Venezuela (Bolivarian Republic)','Venezuela (Bolivarian Republic)'),
('Viet Nam','Viet Nam'),
('Virgin Islands, US','Virgin Islands, US'),
('Wallis and Futuna Islands','Wallis and Futuna Islands'),
('Western Sahara','Western Sahara'),
('Yemen','Yemen'),
('Zambia','Zambia'),
('Zimbabwe','Zimbabwe')]

TupleCountry =[('',''),('Afghanistan','Afghanistan'),
('Aland Islands','Aland Islands'),
('Albania','Albania'),
('Algeria','Algeria'),
('American Samoa','American Samoa'),
('Andorra','Andorra'),
('Angola','Angola'),
('Anguilla','Anguilla'),
('Antarctica','Antarctica'),
('Antigua and Barbuda','Antigua and Barbuda'),
('Argentina','Argentina'),
('Armenia','Armenia'),
('Aruba' , 'Aruba') ,
('Australia','Australia'),
('Austria','Austria'),
('Azerbaijan','Azerbaijan'),
('Bahamas','Bahamas'),
('Bahrain','Bahrain'),
('Bangladesh','Bangladesh'),
('Barbados','Barbados'),
('Belarus','Belarus'),
('Belgium','Belgium'),
('Belize','Belize'),
('Benin','Benin'),
('Bermuda','Bermuda'),
('Bhutan','Bhutan'),
('Bolivia','Bolivia'),
('Bosnia and Herzegovina','Bosnia and Herzegovina'),
('Botswana','Botswana'),
('Bouvet Island','Bouvet Island'),
('Brazil','Brazil'),
('British Virgin Islands','British Virgin Islands'),
('British Indian Ocean Territory','British Indian Ocean Territory'),
('Brunei Darussalam','Brunei Darussalam'),
('Bulgaria','Bulgaria'),
('Burkina Faso','Burkina Faso'),
('Burundi','Burundi'),
('Cambodia','Cambodia'),
('Cameroon','Cameroon'),
('Canada','Canada'),
('Cape Verde','Cape Verde'),
('Cayman Islands','Cayman Islands'),
('Central African Republic','Central African Republic'),
('Chad','Chad'),
('Chile','Chile'),
('China','China'),
('Hong Kong, SAR China','Hong Kong, SAR China'),
('Macao, SAR China','Macao, SAR China'),
('Christmas Island','Christmas Island'),
('Cocos (Keeling) Islands','Cocos (Keeling) Islands'),
('Colombia','Colombia'),
('Comoros','Comoros'),
('Congo (Brazzaville)','Congo (Brazzaville)'),
('Congo, (Kinshasa)','Congo, (Kinshasa)'),
('Cook Islands','Cook Islands'),
('Costa Rica','Costa Rica'),
("Côte d'Ivoire","Côte d'Ivoire"),
('Croatia','Croatia'),
('Cuba','Cuba'),
('Cyprus','Cyprus'),
('Czech Republic','Czech Republic'),
('Denmark','Denmark'),
('Djibouti','Djibouti'),
('Dominica','Dominica'),
('Dominican Republic','Dominican Republic'),
('Ecuador','Ecuador'),
('Egypt','Egypt'),
('El Salvador','El Salvador'),
('Equatorial Guinea','Equatorial Guinea'),
('Eritrea','Eritrea'),
('Estonia','Estonia'),
('Ethiopia','Ethiopia'),
('Falkland Islands (Malvinas)','Falkland Islands (Malvinas)'),
('Faroe Islands','Faroe Islands'),
('Fiji','Fiji'),
('Finland','Finland'),
('France','France'),
('French Guiana','French Guiana'),
('French Polynesia','French Polynesia'),
('French Southern Territories','French Southern Territories'),
('Gabon','Gabon'),
('Gambia','Gambia'),
('Georgia','Georgia'),
('Germany','Germany'),
('Ghana','Ghana'),
('Gibraltar','Gibraltar'),
('Greece','Greece'),
('Greenland','Greenland'),
('Grenada','Grenada'),
('Guadeloupe','Guadeloupe'),
('Guam','Guam'),
('Guatemala','Guatemala'),
('Guernsey','Guernsey'),
('Guinea','Guinea'),
('Guinea-Bissau','Guinea-Bissau'),
('Guyana','Guyana'),
('Haiti','Haiti'),
('Heard and Mcdonald Islands','Heard and Mcdonald Islands'),
('Holy See (Vatican City State)','Holy See (Vatican City State)'),
('Honduras','Honduras'),
('Hungary','Hungary'),
('Iceland','Iceland'),
('India','India'),
('Indonesia','Indonesia'),
('Iran, Islamic Republic of','Iran, Islamic Republic of'),
('Iraq','Iraq'),
('Ireland','Ireland'),
('Isle of Man','Isle of Man'),
('Israel','Israel'),
('Italy','Italy'),
('Jamaica','Jamaica'),
('Japan','Japan'),
('Jersey','Jersey'),
('Jordan','Jordan'),
('Kazakhstan','Kazakhstan'),
('Kenya','Kenya'),
('Kiribati','Kiribati'),
('Korea (North)','Korea (North)'),
('Korea (South)','Korea (South)'),
('Kuwait','Kuwait'),
('Kyrgyzstan','Kyrgyzstan'),
('Lao PDR','Lao PDR'),
('Latvia','Latvia'),
('Lebanon','Lebanon'),
('Lesotho','Lesotho'),
('Liberia','Liberia'),
('Libya','Libya'),
('Liechtenstein','Liechtenstein'),
('Lithuania','Lithuania'),
('Luxembourg','Luxembourg'),
('Macedonia, Republic of','Macedonia, Republic of'),
('Madagascar','Madagascar'),
('Malawi','Malawi'),
('Malaysia','Malaysia'),
('Maldives','Maldives'),
('Mali','Mali'),
('Malta','Malta'),
('Marshall Islands','Marshall Islands'),
('Martinique','Martinique'),
('Mauritania','Mauritania'),
('Mauritius','Mauritius'),
('Mayotte','Mayotte'),
('Mexico','Mexico'),
('Micronesia, Federated States of','Micronesia, Federated States of'),
('Moldova','Moldova'),
('Monaco','Monaco'),
('Mongolia','Mongolia'),
('Montenegro','Montenegro'),
('Montserrat','Montserrat'),
('Morocco','Morocco'),
('Mozambique','Mozambique'),
('Myanmar','Myanmar'),
('Namibia','Namibia'),
('Nauru','Nauru'),
('Nepal','Nepal'),
('Netherlands','Netherlands'),
('Netherlands Antilles','Netherlands Antilles'),
('New Caledonia','New Caledonia'),
('New Zealand','New Zealand'),
('Nicaragua','Nicaragua'),
('Niger','Niger'),
('Nigeria','Nigeria'),
('Niue','Niue'),
('Norfolk Island','Norfolk Island'),
('Northern Mariana Islands','Northern Mariana Islands'),
('Norway','Norway'),
('Oman','Oman'),
('Pakistan','Pakistan'),
('Palau','Palau'),
('Palestinian Territory','Palestinian Territory'),
('Panama','Panama'),
('Papua New Guinea','Papua New Guinea'),
('Paraguay','Paraguay'),
('Peru','Peru'),
('Philippines','Philippines'),
('Pitcairn','Pitcairn'),
('Poland','Poland'),
('Portugal','Portugal'),
('Puerto Rico','Puerto Rico'),
('Qatar','Qatar'),
('Réunion','Réunion'),
('Romania','Romania'),
('Russian Federation','Russian Federation'),
('Rwanda','Rwanda'),
('Saint-Barthélemy','Saint-Barthélemy'),
('Saint Helena','Saint Helena'),
('Saint Kitts and Nevis','Saint Kitts and Nevis'),
('Saint Lucia','Saint Lucia'),
('Saint-Martin (French part)','Saint-Martin (French part)'),
('Saint Pierre and Miquelon','Saint Pierre and Miquelon'),
('Saint Vincent and Grenadines','Saint Vincent and Grenadines'),
('Samoa','Samoa'),
('San Marino','San Marino'),
('Sao Tome and Principe','Sao Tome and Principe'),
('Saudi Arabia','Saudi Arabia'),
('Senegal','Senegal'),
('Serbia','Serbia'),
('Seychelles','Seychelles'),
('Sierra Leone','Sierra Leone'),
('Singapore','Singapore'),
('Slovakia','Slovakia'),
('Slovenia','Slovenia'),
('Solomon Islands','Solomon Islands'),
('Somalia','Somalia'),
('South Africa','South Africa'),
('South Georgia and the South Sandwich Islands','South Georgia and the South Sandwich Islands'),
('South Sudan','South Sudan'),
('Spain','Spain'),
('Sri Lanka','Sri Lanka'),
('Sudan','Sudan'),
('Suriname','Suriname'),
('Svalbard and Jan Mayen Islands','Svalbard and Jan Mayen Islands'),
('Swaziland','Swaziland'),
('Sweden','Sweden'),
('Switzerland','Switzerland'),
('Syrian Arab Republic (Syria)','Syrian Arab Republic (Syria)'),
('Taiwan, Republic of China','Taiwan, Republic of China'),
('Tajikistan','Tajikistan'),
('Tanzania, United Republic of','Tanzania, United Republic of'),
('Thailand','Thailand'),
('Timor-Leste','Timor-Leste'),
('Togo','Togo'),
('Tokelau','Tokelau'),
('Tonga' , 'Tonga'),
('Trinidad and Tobago','Trinidad and Tobago'),
('Tunisia','Tunisia'),
('Turkey','Turkey'),
('Turkmenistan','Turkmenistan'),
('Turks and Caicos Islands','Turks and Caicos Islands'),
('Tuvalu','Tuvalu'),
('Uganda','Uganda'),
('Ukraine','Ukraine'),
('United Arab Emirates','United Arab Emirates'),
('United Kingdom','United Kingdom'),
('United States of America','United States of America'),
('US Minor Outlying Islands','US Minor Outlying Islands'),
('Uruguay','Uruguay'),
('Uzbekistan','Uzbekistan'),
('Vanuatu','Vanuatu'),
('Venezuela (Bolivarian Republic)','Venezuela (Bolivarian Republic)'),
('Viet Nam','Viet Nam'),
('Virgin Islands, US','Virgin Islands, US'),
('Wallis and Futuna Islands','Wallis and Futuna Islands'),
('Western Sahara','Western Sahara'),
('Yemen','Yemen'),
('Zambia','Zambia'),
('Zimbabwe','Zimbabwe')]


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
    NAME = StringField(u'Name',validators=[InputRequired(), Length(min=3, max=25)])
    NICKNAME = StringField(u'Nickname', validators=[Length(max=50)])
    SURNAME = StringField(u'Surname',validators=[InputRequired(),Length(min=1, max=45)])
    CONTINENT = SelectField(u'Choose continent',choices=TupleContinent)
    COUNTRY = SelectField(u'Country', choices=TupleCountry)
    CITY = StringField(u'City',validators=[InputRequired(),Length(min = 1, max=45)])
    ZIP_CODE = StringField(u'Zip-code',validators=[InputRequired(),Length(min = 1, max=7)])
    STREET = StringField(u'Street',validators=[InputRequired(),Length(min = 1, max=45)])
    STREET_NUMBER = StringField(u'Street number',validators=[InputRequired(),Length(min = 1, max=10)])
    PHONE_NUMBER = StringField(u'Phone number 1',validators=[InputRequired(),Length(min = 6, max=20)])
    PHONE_NUMBER2 = StringField(u'Phone number 2 *')
    WEIGHT_CATEGORY = SelectField(u'Choose Your weight category *', choices=TupleWeightCatMen)
    WEIGHT = StringField(u'What is Your weight [lb] ? *')
    HEIGHT = StringField(u'Your height: *')
    SPORT = SelectField(u'Sport', choices=TupleSport)
    FIGHT_STYLE =SelectField(u'What kind of fight do You prefer?',choices=TuplePreferFightStyle)
    FIGHT_STATUS = SelectField(u'Are You looking for fight? *', choices=TupleFightStatus)
    NUMBER_OF_WINS = StringField(u'How many fights have You win ?')
    NUMBER_OF_LOSS = StringField(u'How many fights have You loss ?')
    FREE_AGENT = SelectField(u'Do You have any exclusive contract ?',choices=[('Yes','Yes'),('No','No')])
    URL = StringField(u'Paste http link from Sherdog.com')

class FederationAccountForm(FlaskForm):
    NAME = StringField(u'Name',validators=[InputRequired(), Length(min=3, max=15)])
    SURNAME = StringField(u'Surname',validators=[InputRequired(),Length(min = 1, max=45)])
    CONTINENT = SelectField(u'Choose continent',choices=TupleContinent)
    COUNTRY = SelectField(u'Country', choices=TupleCountry)
    CITY = StringField(u'City',validators=[InputRequired(),Length(min = 1, max=45)])
    ZIP_CODE = StringField(u'Zip-code',validators=[InputRequired(),Length(min = 1, max=7)])
    STREET = StringField(u'Street',validators=[InputRequired(),Length(min = 1, max=45)])
    STREET_NUMBER = StringField(u'Street number',validators=[InputRequired(),Length(min = 1, max=10)])
    PHONE_NUMBER = StringField(u'Phone number 1',validators=[InputRequired(),Length(min = 6, max=20)])
    PHONE_NUMBER2 = StringField(u'Phone number 2 *')
    FEDERATION_NAME = StringField(u'What is Your federation name ?', validators=[InputRequired(),Length(min = 2, max=50)])
    # FEDERATION_RANGE = SelectMultipleField(u'Where do You organise fights ?',choices=TupleContinent,default = ['1', '3'])
    FEDERATION_CREATED_DATE = StringField(u'Start yeaer')
    SPORT_NAME =SelectField(u'Choose sport',choices=TupleSport)


class ManagerAccountForm(FlaskForm):
    NAME = StringField(u'Name',validators=[InputRequired(), Length(min=3, max=15)])
    SURNAME = StringField(u'Surname',validators=[InputRequired(),Length(min = 1, max=45)])
    CONTINENT = SelectField(u'Choose continent',choices=TupleContinent)
    COUNTRY = SelectField(u'Country', choices=TupleCountry)
    CITY = StringField(u'City',validators=[InputRequired(),Length(min = 1, max=45)])
    ZIP_CODE = StringField(u'Zip-code',validators=[InputRequired(),Length(min = 1, max=7)])
    STREET = StringField(u'Street',validators=[InputRequired(),Length(min = 1, max=45)])
    STREET_NUMBER = StringField(u'Street number',validators=[InputRequired(),Length(min = 1, max=10)])
    PHONE_NUMBER = StringField(u'Phone number 1',validators=[InputRequired(),Length(min = 6, max=20)])
    PHONE_NUMBER2 = StringField(u'Phone number 2 *')
    SPORT_NAME =SelectField(u'Choose sport for which You deal with',choices=TupleSport)

ContinentList =[]
CountryList =[]
CityList =[]
class Area(FlaskForm):
    CONTINENT = SelectField(u'Continent', choices=ContinentList)
    COUNTRY = SelectField(u'Country',choices=CountryList)
    CITY = SelectField(u'City',choices=CityList)


class SearchFormFindFighters(FlaskForm):
    WEIGHT_CATEGORY = SelectField(u'Choose weight category *', choices=TupleWeightCatMen)
    COUNTRY = SelectField(u'Country',choices=TupleCountry)
    COUNTRY = SelectField(u'Country',choices=TupleCountry)

class Events(FlaskForm):
    EVENT_NAME = StringField(u'Event name',validators=[InputRequired(),Length(min=3,max=50)],id='EVENTS_NAME')
    CONTINENT = SelectField(u'Continent', choices=TupleContinent)
    CITY = StringField(u'City',validators=[InputRequired(),Length(min=1,max=50)])
    COUNTRY = SelectField(u'Country', choices=TupleCountry)
    ZIP_CODE = StringField(u'Zip-code', validators=[InputRequired(), Length(min=1, max=7)])
    STREET = StringField(u'Street', validators=[InputRequired(), Length(min=1, max=45)])
    STREET_NUMBER = StringField(u'Street number', validators=[InputRequired(), Length(min=1, max=10)])
    dt = DateField('Pick a Date', format="%d/%m/%y")
    TIME = StringField(u'Event start time (use format: H:M) ',validators=[InputRequired()])
    NEED_FIGHTER_STATUS = BooleanField(U'Are You looking for fighters for the event ?',validators=[InputRequired()])

FIGHTERS =[]
json_lists = []

class FIGHTS(FlaskForm):
    EVENT_NAME = StringField(u'Choose event name')
    ID_FIGHTER_1 = StringField(u'ID number for first fighter')
    ID_FIGHTER_2 = StringField(u'ID number for second fighter')
    WEIGHT_CATEGORY = SelectField(u'Weight category', choices=TupleWeightCatMen)
    TIME = StringField(u'Round time')
    AMOUNT_OF_ROUNDS = StringField(u'Amount of rounds')

class SearchEvent(FlaskForm):
    CONTINENT = SelectField(u'Continent', choices=TupleContinentSearch)
    COUNTRY = SelectField(u'Country', choices=TupleCountrySearch)
    WEIGHT_CATEGORY = SelectField(u'Weight category',choices=TupleWeightCatMenSearch)
    dt = DateField('Pick a Date', format="%m/%d/%y")

class ShowEvent(FlaskForm):
    CONTINENT = SelectField(u'Continent', choices=TupleContinentSearch)
    COUNTRY = SelectField(u'Country', choices=TupleCountry)
    CITY = StringField(u'City')
    EVENT_STATUS = SelectField(u'Event status', choices=TupleEventStatus)

class SearchFighter(FlaskForm):
    CONTINENT = SelectField(u'Continent', choices=TupleContinentSearch)
    COUNTRY = SelectField(u'Country', choices=TupleCountrySearch)
    CITY = StringField(u'City')
    WEIGHT_CATEGORY = SelectField(u'Choose Your weight category *', choices=TupleWeightCatMenSearch)
    NUMBER_OF_FIGHTS = StringField(u'Point minimal number of fights which fighter should have (combine wins and losses)')
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

class CheckTeam(FlaskForm):
    FIGHT_STATUS = SelectField(u'Fight status 2323', choices=TupleFightStatusSearch)
    HEALTH_STATUS = SelectField(u'Health status 2323', choices=TupleHealthConditionSearch)

class FindFederation(FlaskForm):
    CONTINENT = SelectField(u'Continent', choices=TupleContinentSearch)
    COUNTRY = SelectField(u'Country', choices=TupleCountrySearch)
    CITY = StringField(u'City')

# def CountryList():
#     q=LOCALIZATION.query.all()
#     continents = [i.CONTINENT for i in q]
#     continents_no_dup=set(continents)
#     final_list=list(continents_no_dup)
#     print(final_list)
#     return final_list
#
