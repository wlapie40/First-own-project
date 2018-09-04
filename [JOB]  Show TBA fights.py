import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from email.mime.base import MIMEBase
import time
import schedule
from app import db

def job():
    F5 = db.engine.execute("""SELECT e.EVENT_NAME,e.CITY,e.CONTINENT,e.COUNTRY,e.ZIP_CODE,e.STREET,e.STREET_NUMBER,e.DATE,e.TIME,f.WEIGHT_CATEGORY,ff.ID_FIGHT FROM FIGHTER_FIGHTS ff
    INNER JOIN FIGHT f  ON ff.ID_FIGHT=f.ID_FIGHT
    INNER JOIN EVENTS e ON e.ID_EVENT=f.ID_EVENT
    WHERE ff.ID_FIGHTER=110""")

    fight_list = [i for i in F5]
    print(fight_list)


schedule.every(1).minutes.do(job)
schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

    # 'SELECT fed.FEDERATION_NAME,even.EVENT_NAME,even.CONTINENT,even.COUNTRY,even.CITY,even.DATE,fight.WEIGHT_CATEGORY,'
    # 'CASE WHEN fight.ID_FIGHTER_1  =' + "'" + 'TBA' + "'" + 'THEN fight.ID_FIGHTER_2 '
    # ' WHEN fight.ID_FIGHTER_2  =' + "'" + 'TBA' + "'" + 'THEN fight.ID_FIGHTER_1 END '
    # 'FROM FEDERATION fed '
    # 'INNER JOIN EVENTS even ON fed.ID_FEDERATION=even.ID_FEDERATION '
    # 'INNER JOIN FIGHT fight ON even.ID_EVENT=fight.ID_EVENT ORDER BY even.DATE ASC,even.CONTINENT')