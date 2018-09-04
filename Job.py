# import schedule
import time
from DB import db
from datetime import datetime as dt
from DB import EVENTS
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
# def job():


CREATE_DATE = time.strftime("%d/%m/%y")

print('Job has been started...')
print(CREATE_DATE)



# Szukamy ofert walk dla managerow
# Lista FIGHT_REQUEST
print("""Lista FIGHT_REQUEST (ID_FIHGTER,ID_MANAGER,WEIGHT_CATEGORY,CONTINENT,COUNTRY,CITY)""")
F5 = db.engine.execute("""SELECT ID_FIGHTER,ID_MANAGER,WEIGHT_CATEGORY,CASE WHEN CONTINENT is Null THEN '' ELSE CONTINENT END,CASE WHEN COUNTRY is Null THEN '' ELSE COUNTRY END,CASE WHEN CITY is Null THEN '' ELSE CITY END FROM FIGHT_REQUEST""")
req_list = [i for i in F5]
print(req_list)
for i in req_list:
    print(i)
    F6 = db.engine.execute("""SELECT e.EVENT_NAME,e.CITY,e.CONTINENT,e.COUNTRY,f.ID_FIGHT FROM FIGHT f 
    INNER JOIN EVENTS e ON f.FEDERATION_ID=e.ID_FEDERATION
    WHERE WEIGHT_CATEGORY='"""+i[2]+"'"+""" AND e.CONTINENT = '"""+str(i[3])+"'"+""" AND COUNTRY = '"""+str(i[4])+"'"+""" AND e.CITY = '"""+str(i[5])+"'")
    print('WEIGHT_CATEGORY:')
    print(i[2])
    print('CONTINENT:')
    print(i[3])
    print('COUNTRY:')
    print(i[4])
    print('CITY:')
    print(i[5])
    fight_list = [i for i in F6]
    print(fight_list)

for i in fight_list:
    print(i)
# Lista walk które potrzebują zawodników

# sendEmail=[]
# r=0
# # print(str(req_list[r][2]))
# # print(str(req_list[r][3]))
# # print(str(req_list[r][4]))
# F5 = db.engine.execute("""SELECT distinct(f.ID_FIGHT) FROM FIGHT f INNER JOIN EVENTS e ON f.FEDERATION_ID=e.ID_FEDERATION
# WHERE (f.WEIGHT_CATEGORY= """+"'"+ req_list[r][2]+"'"+""" AND e.CONTINENT= """+"'"+req_list[r][3]+"'"+""" AND e.COUNTRY LIKE"""+"'"+req_list[r][4]+"'"+"""AND e.CITY LIKE"""+"'"+req_list[r][5]+"'"+")"+"""AND (f.ID_FIGHTER_1='TBA' or f.ID_FIGHTER_2='TBA')""")
# ev_list = [i for i in F5]
# print("""Lista ID_EVENT'ow spełniających kryteria z listy 'req_list'""")
# print(ev_list)
# sendEmail.append(ev_list,req_list[r])
# r+=1







# # Zmieniamy statusy Eventom (NEW,PENDING,FINISHED)
# query_event=db.engine.execute('SELECT ID_EVENT,EVENT_NAME,DATE,COUNTRY,CONTINENT FROM EVENTS')
# list = [i for i in query_event]
# print(list)
# r=1
# for i in list:
#     if dt.strptime(i[2], '%m/%d/%y')>dt.strptime(CREATE_DATE,'%d/%m/%y'):
#         print('ID_EVENT: ' +"'"+ str(r) +"'"+ " has status 'NEW' still.")
#     elif dt.strptime(i[2], '%m/%d/%y')==dt.strptime(CREATE_DATE,'%d/%m/%y'):
#         query = EVENTS.query.get(str(r))
#         query.EVENT_STATUS='PENDING'
#         db.session.commit()
#         print('ID_EVENT: ' +"'"+ str(r) +"'"+ " status has been changed on 'PENDING'.")
#     elif dt.strptime(i[2], '%m/%d/%y')<dt.strptime(CREATE_DATE,'%d/%m/%y'):
#         query = EVENTS.query.get(str(r))
#         query.EVENT_STATUS = 'FINISHED'
#         db.session.commit()
#         print('ID_EVENT: ' +"'"+ str(r) +"'"+ " status has been changed on 'FINISHED'.")
#     r=r+1
#
# # Wysylamy maile do managerow:
#     query_manager = db.engine.execute('SELECT ID_FIGHT FROM FIGHT WHERE ID_FIGHT_1='+"'"+"99"+"'" + "OR"+ "ID_FIGHT_2=" +"'"+"99"+"'")
#     if query_manager.rowcount:
#         query_manager_list = [i for i in query_manager ]
#     else:
#         print('the is now records')
    # print(query_manager_list)

# schedule.every(1).minutes.do(job)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)

# projectlitchi@gmail.com
# 2Francja