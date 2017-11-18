import json
import sqlite3
import os
from flask import Flask, g, render_template, request, Response

template_dir = os.path.abspath('web')
DATABASE = '../database/hackthehomeless.db'
app = Flask(__name__, template_folder = template_dir)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/account/register', methods=['POST'])
def register():
    register_info = request.get_json()
    print(register_info)

    name = register_info['name']
    email = register_info['email']
    password = register_info['password']
    publicHash = 'TODO'
    qr = 'TODO'

    cur = get_db().cursor()
    query = 'insert into users(name, email, password, publicHash, qr) values(\'%s\', \'%s\', \'%s\', \'%s\', \'%s\')' % (
        name,
        email,
        password,
        publicHash,
        qr
    )
    cur.execute(query)
    get_db().commit()
    user_id = cur.lastrowid
    cur.close()

    js = get_user_data(user_id)
    # TODO return 200 if can't be registered
    return Response(json.dumps(js), mimetype='application/json')

@app.route('/api/account/user', methods=['POST'])
def user():
    user_info = request.get_json()
    print(user_info)

    email = user_info['email']
    password = user_info['password']

    cur = get_db().cursor()
    query = 'select * from users where email=\'%s\' and password=\'%s\'' % (
        email,
        password
    )
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()

    if (len(rows) == 0):
        return message_response(400, 'There are no users with these credentials', 'application/json')
    if (len(rows) > 1):
        return message_response(400, 'There is more than one user with these credentials', 'application/json')

    js = get_user_data(rows[0]['id'])
    return Response(json.dumps(js), mimetype='application/json')

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def message_response(status_code, message, mime_type):
    return Response("{'message':'" + message + "'}", status=status_code, mimetype=mime_type)

def get_user_data(user_id):
    '''
    returns a json dictionary encoding the:
        name
        qr
        balance
    '''
    cur = get_db().cursor()
    query = 'select * from users where id=\'%s\'' % (
        user_id
    )
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()

    if (len(rows) != 1):
        return None

    user = rows[0]

    js = {'name' : user['name'],
          'qr' : user['qr'],
          'balance' : get_user_balance(user_id)
         }
    return js

def get_user_balance(user_id):
    return 9000

if __name__ == '__main__':
    app.run()
