from flask import Flask, render_template, request, json, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from requests.bucket_req import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BucketList.db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route("/")
def main():
    return render_template('index.html')


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/signUp', methods=['POST'])
def signUp():
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    if _name and _email and _password:
        query = check_user(_name)
        if query is None:
            try:
                _hashed_password = generate_password_hash(_password)
                create_user(_name, _email, _hashed_password)
                return json.dumps({'message': 'Пользователь создан!'}, ensure_ascii=False)
            except Exception as ex:
                return json.dumps({'error': str(ex)}, ensure_ascii=False)
        else:
            return json.dumps({'message': 'Пользователь с таким именем уже существует!'}, ensure_ascii=False)
    else:
        return json.dumps({'html': '<span>Должны быть заполнены все поля</span>'}, ensure_ascii=False)


@app.route('/showSignin')
def showSignin():
    return render_template('signin.html')


@app.route('/validateLogin', methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']

        query = get_user(_username)
        if not query is None:
            if check_password_hash(query.user_password, _password):
                session['user'] = query.user_name
                return redirect('/userHome')
            else:
                return render_template('error.html', error='Wrong Email address or Password.')
        else:
            return render_template('error.html', error='Wrong Email address or Password.')

    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html', error='Unauthorized Access')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route('/showAddWish')
def showAddWish():
    return render_template('addWish.html')


@app.route('/addWish', methods=['POST'])
def addWish():
    try:
        if session.get('user'):
            _title = request.form['inputTitle']
            _description = request.form['inputDescription']
            _user = session.get('user')

            if create_wish(_title, _description, _user):
                return redirect('/userHome')
            else:
                return render_template('error.html', error='An error occurred!')

        else:
            return render_template('error.html', error='Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/getWish')
def getWish():
    try:
        if session.get('user'):
            _user = session.get('user')

            wishes = get_wish_by_user(_user)
            wishes_dict = []
            # for wish in wishes:
            for i in range(len(wishes)):
                wish = wishes[i]
                wish_dict = {
                    'Id': wish.wish_id,
                    'Title': wish.wish_title,
                    'Description': wish.wish_description,
                    'Date': wish.wish_date}
                wishes_dict.append(wish_dict)

            return json.dumps(wishes_dict)
        else:
            return render_template('error.html', error='Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error=str(e))


if __name__ == "__main__":
    app.secret_key = b'_789y2L"HGF8z&%^Tf]/'
    app.run()
