from flask import Flask, render_template, request, json, session, redirect
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
conn = sqlite3.connect("BucketList.db", check_same_thread=False)
cursor = conn.cursor()


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
        query = cursor.execute("select 1 from tbl_user where user_name= ? ", (_name,)).fetchone()
        if query is None:
            try:
                _hashed_password = generate_password_hash(_password)
                cursor.execute('insert into tbl_user (user_name, user_username, user_password) values (?, ?, ?)',
                               (_name, _email, _hashed_password,))
                conn.commit()
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

        query = cursor.execute("select * from tbl_user where user_username= ? ", (_username,)).fetchone()
        if not query is None:
            if check_password_hash(str(query[3]), _password):
                session['user'] = query[1]
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


def create_db():
    query = cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='tbl_user'").fetchone()
    if (not query is None) and (query[0] == 0):
        cursor.execute('CREATE TABLE if not exists tbl_user('
                       'user_id integer PRIMARY KEY AUTOINCREMENT,'
                       'user_name VARCHAR(45) default null,'
                       'user_username VARCHAR(45) default null,'
                       'user_password VARCHAR(45) default null)')
    return True


if __name__ == "__main__":
    if create_db():
        app.secret_key = b'_5#y2L"HGF8z&%^Tf]/'
        app.run()
