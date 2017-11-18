import json
import web3
import sqlite3
import os
import hashlib
from flask import Flask, g, render_template, request, Response
from web3 import Web3, HTTPProvider

template_dir = os.path.abspath('web')
DATABASE = '../database/hackthehomeless.db'
app = Flask(__name__, template_folder = template_dir)

w3 = Web3(HTTPProvider('http://localhost:8545'))

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
    publicHash = w3.sha3(text=name)

    query = 'insert into users(name, email, password, publicHash) values(\'%s\', \'%s\', \'%s\', \'%s\')' % (
        name,
        email,
        password,
        publicHash
    )
    user_id = insert_db(query)

    js = get_user_data(user_id)
    return Response(json.dumps(js), mimetype='application/json')

@app.route('/api/account/user', methods=['POST'])
def user():
    user_id = get_user_id(request)
    js = get_user_data(user_id)
    return Response(json.dumps(js), mimetype='application/json')

@app.route('/api/account/user/transactions', methods=['POST'])
def transactions():
    user_id = get_user_id(request)
    js = get_user_transactions(user_id)
    return Response(json.dumps(js), mimetype='application/json')

@app.route('/api/account/user/donations', methods=['POST'])
def donations():
    user_id = get_user_id(request)
    js = get_user_donations(user_id)
    return Response(json.dumps(js), mimetype='application/json')

@app.route('/api/account/user/purchases', methods=['GET'])
def purchases():
    '''
    can get publicHash OR id as url params
    return date, description, amount, id
    '''
    # TODO Michael

@app.route('/api/account/user/donate', methods=['POST'])
def donate():
    '''
    gets spenderId, email, password
    '''
    user_id = get_user_id(request)
    donate_info = request.get_json()
    spender_id = donate_info['spenderId']
    amount = donate_info['amount']

    query = 'insert into donations(donorId, spenderId, amount, temporal) values(\'%s\', \'%s\', \'%s\', datetime())' % (
        user_id,
        spender_id,
        amount
    )
    insert_id = insert_db(query)
    print(insert_id)
    return message_response(200, 'The donation was successful!', 'application/json')

@app.route('/api/account/user/buy', methods=['POST'])
def buy():
    '''
    gets email, password, amount
    '''
    user_id = get_user_id(request)
    user_data = get_user_data(user_id)
    publicHash = user_data['qr']
    amount = request.get_json()['amount']
    # TODO Igor does this using the blockchain using the publicHash and amount
    return message_response(200, 'The purchase of HTH was successful!', 'application/json')

@app.route('/api/account/user/purchase', methods=['POST'])
def purchase():
    '''
    gets amount, description, email, password, publicHash
    POV of sellers
    if homeless person buying food, then amount is positive
    if donator buying crypto, then amount if positive
    '''
    user_id = get_user_id(request)
    # TODO Michael

@app.route('/api/account/user/balance', methods=['GET'])
def balance():
    '''
    gets publicHash as url param
    '''
    publicHash = request.args.get('publicHash', '')
    if (publicHash == ''):
        return message_response(400, 'The publicHash was not provided', 'application/json')

    balance = get_user_balance(publicHash)
    js = { 'balance' : balance }
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

def query_db(query):
    cur = get_db().cursor()
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    return rows

def insert_db(query):
    cur = get_db().cursor()
    cur.execute(query)
    get_db().commit()
    insert_id = cur.lastrowid
    cur.close()
    return insert_id

def message_response(status_code, message, mime_type):
    return Response("{'message':'" + message + "'}", status=status_code, mimetype=mime_type)

def check_user_rows(rows):
    if (len(rows) == 0):
        return message_response(400, 'There are no users with these credentials', 'application/json')
    if (len(rows) > 1):
        return message_response(400, 'There is more than one user with these credentials', 'application/json')

'''
The request needs to contain and email and password encoded using json.
'''
def get_user_id(request):
    user_info = request.get_json()
    print(user_info)

    email = user_info['email']
    password = user_info['password']

    query = 'select * from users where email=\'%s\' and password=\'%s\'' % (
        email,
        password
    )
    rows = query_db(query)
    check_user_rows(rows)

    user_id = rows[0]['id']
    return user_id

def get_user_data(user_id):
    '''
    returns a json dictionary encoding the:
        name
        qr
        balance
    '''
    query = 'select * from users where id=\'%s\'' % (
        user_id
    )
    rows = query_db(query)
    check_user_rows(rows)

    user = rows[0]

    js = {
        'name' : user['name'],
        'qr' : user['publicHash'],
        'balance' : get_user_balance(user['publicHash'])
     }
    return js

def get_user_balance(public_hash):
    # TODO Igor gets this from blockchain using the publicHash
    return 9000

def get_user_transactions(user_id):
	#TODO: filter by user_id
    '''
    returns a json dictionary encoding the:
        type (Donation|Purchase)
        amount
        description
        date
    '''
    query_db('begin transaction;')
    query_db('''
        create table if not exists transactions (
            type varchar(255),
            amount float,
            description varchar(255),
            temporal timestamp
        );
    	''')
    query_db('''
    	insert into transactions
            select 'Donation',amount,'Donation',temporal from donations;
    	''')
    query_db('''
    	insert into transactions
            select 'Purchase',amount,description,temporal from purchases;
        ''')
    rows = query_db('''
    	select * from transactions
            order by temporal desc;
        ''')
    query_db('drop table if exists transactions;')
    query_db('commit;')

    js = { 'transactions': [] }
    transactions = js['transactions']
    for row in rows:
        transactions.append({
            'type' : row['type'],
            'amount' : row['amount'],
            'description' : row['description'],
            'date' : row['temporal']
        })

    return js

def get_user_donations(user_id):
    '''
    return a json dictionary encoding the:
        date
        amount
        spender_id (homeless_id)
    '''
    query = 'select * from donations where donorId=\'%s\'' % (
        user_id
    )
    rows = query_db(query)

    js = { 'donations': [] }
    donations = js['donations']
    for row in rows:
        donations.append({
            'spenderId' : row['spenderId'],
            'amount' : row['amount'],
            'date' : row['temporal'],
        })

    return js

if __name__ == '__main__':
    app.run()
