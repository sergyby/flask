from datetime import datetime
import models.bucket_models as bm
from app import db


tusr = bm.TblUser
tws = bm.TblWish


def check_user(usr_name):
    _name = db.session.query(tusr).filter(tusr.user_name == usr_name).all()
    if len(_name) == 0:
        return None
    else:
        return _name[0].user_name


def get_user(email):
    _name = db.session.query(tusr).filter(tusr.user_username == email).all()
    if len(_name) == 0:
        return None
    else:
        return _name[0]


def create_user(name, email, pwd):
    try:
        new_user = tusr(user_name=name,
                        user_username=email,
                        user_password=pwd)
        db.session.add(new_user)
        db.session.commit()
    except Exception as ex:
        return str(ex)


def create_wish(title, description, user):
    try:
        new_wish = tws(wish_title=title,
                       wish_description=description,
                       wish_user_id=user,
                       wish_date=datetime.now())
        db.session.add(new_wish)
        db.session.commit()
        return True
    except Exception as ex:
        return False


def get_wish_by_user(user):
    # select * from tbl_wish where wish_user_id = p_user_id;
    uids = db.session.query(tws).filter(tws.wish_user_id == user).all()
    if len(uids) == 0:
        return None
    else:
        return uids