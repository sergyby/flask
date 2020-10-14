from app import db


class TblUser(db.Model):
    __tablename__ = 'tbl_user'
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_name = db.Column(db.String(45), nullable=True)
    user_username = db.Column(db.String(45), nullable=True)
    user_password = db.Column(db.String(45), nullable=True)


class TblWish(db.Model):
    __tablename__ = 'tbl_wish'
    wish_id = db.Column(db.Integer, primary_key=True, nullable=False)
    wish_title = db.Column(db.String(45), nullable=True)
    wish_description = db.Column(db.String(5000), nullable=True)
    wish_user_id = db.Column(db.Integer, nullable=True)
    wish_date = db.Column(db.DateTime, nullable=True)


db.create_all()
db.session.commit()
