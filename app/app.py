import json
import sqlite3
from flask import Flask
from flask import request
from flask import g

app = Flask(__name__)

DATABASE = '../database/hackthehomeless.db'

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

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
    query = 'insert into users(id, name, email, password, publicHash, qr) values(\'%s\', \'%s\', \'%s\', \'%s\', \'%s\')' % (
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
    r = cur.fetchall()
    user_id = cur.lastrowid
    cur.close()

    js = get_user_data(user_id)
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

def get_user_data(user_id):
    '''
    returns a json dictionary encoding the:
        name
        qr
        balance
    '''
    js = []
    js.append('Yo Will')
    return js

if __name__ == '__main__':
    app.run()
