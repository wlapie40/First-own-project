from DB import USER
from app import current_user

def Id_Fighter(name):
    name = current_user.USERNAME
    query = USER.query.filter_by(USERNAME=name).first()
    id_fighter = query.FIGHTER.ID_FIGHTER
    print('[def: Id_Fighter] ID_FIHGTER: '+str(id_fighter))
    return id_fighter