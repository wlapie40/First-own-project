import time
import schedule
from app import db

# def job():
F5 = db.engine.execute("""SELECT e.EVENT_NAME,e.CITY,e.CONTINENT,e.COUNTRY,e.ZIP_CODE,e.STREET,e.STREET_NUMBER,e.DATE,e.TIME,f.WEIGHT_CATEGORY,ff.ID_FIGHT FROM FIGHTER_FIGHTS ff
INNER JOIN FIGHT f  ON ff.ID_FIGHT=f.ID_FIGHT
INNER JOIN EVENTS e ON e.ID_EVENT=f.ID_EVENT
WHERE ff.ID_FIGHTER=110""")

fight_list = [i for i in F5]
print(fight_list)


# schedule.every(1).minutes.do(job)
# schedule.every(1).minutes.do(job)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)