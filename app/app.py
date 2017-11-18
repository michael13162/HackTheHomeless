import json
import web3
import sqlite3
import os
import hashlib
import blockchain
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

@app.route('/api/account/user/<int:user_id>', methods=['GET'])
def user_by_id():
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
    can get publicHash OR spenderId as url params
    return date, description, amount, spenderId
    '''
    publicHash = request.args.get('publicHash', '')
    spenderId = request.args.get('spenderId', '')
    if (publicHash == '' and spenderId == ''):
        return message_response(400, 'The query string does not have a publicHash or a spenderId', 'application/json')

    if (spenderId == ''):
        query = 'select * from users where publicHash=\'%s\'' % (publicHash)
        rows = query_db(query)
        check_user_rows(rows)
        spenderId = rows[0]['id']

    query = '''
            select * from purchases where spenderId=\'%s\'
                order by temporal desc;
            ''' % (spenderId)
    rows = query_db(query)

    js = { 'purchases' : [] }
    purchases = js['purchases']
    for row in rows:
        purchases.append({
            'spenderId' : spenderId,
            'amount' : row['amount'],
            'description' row['description'],
            'date' : row['temporal']
        })

    return js

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

    balance = blockchain.getBalance(publicHash)
    blockchain.setBalance(publicHash, balance + amount)
    
    return message_response(200, 'The purchase of HTH was successful!', 'application/json')

@app.route('/api/account/user/purchase', methods=['POST'])
def purchase():
    '''
    gets amount, description, email, password, publicHash
    POV of sellers purchasing HTH
    '''
    user_id = get_user_id(request)
    purchase_info = request.get_json()

    amount = purchase_info['amount']
    description = purchase_info['description']
    publicHash = purchase_info['publicHash']

    # TODO Michael

@app.route('/api/account/user/balance', methods=['GET'])
def balance():
    '''
    gets publicHash as url param
    '''
    publicHash = request.args.get('publicHash', '')
    if (publicHash == ''):
        return message_response(400, 'The publicHash was not provided', 'application/json')

    balance = blockchain.getBalance(publicHash)
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
        'balance' : blockchain.getBalance(user['publicHash'])
     }
    return js

def get_user_transactions(user_id):
    '''
    returns a json dictionary encoding the:
        type (Donation|Purchase)
        amount
        description
        date
    '''
    cur = get_db().cursor()
    cur.execute('begin transaction;')
    cur.execute('''
        create table if not exists transactions (
            type varchar(255),
            amount float,
            description varchar(255),
            temporal timestamp
        );
    	''')
    cur.execute('''
    	insert into transactions
            select 'Donation',amount,'Donation',temporal from donations
                where spenderId=\'%s\';
    	''' % (user_id))
    cur.execute('''
    	insert into transactions
            select 'Purchase',amount,description,temporal from purchases
                where spenderId=\'%s\';
        ''' % (user_id))
    cur.execute('''
    	select * from transactions
            order by temporal desc;
        ''')
    rows = cur.fetchall()
    cur.execute('drop table if exists transactions;')
    get_db().commit()

    cur.close()

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
        name (homeless_name)
        spender_id (homeless_id)
    '''
    query = '''
        select * from donations where donorId=\'%s\'
            order by temporal desc;
    ''' % (user_id)
    rows = query_db(query)

    js = { 'donations': [] }
    donations = js['donations']
    for row in rows:
        spenderId = row['spenderId']
        name = get_user_data(spenderId)['name']
        donations.append({
            'spenderId' : spenderId,
            'name' : name,
            'amount' : row['amount'],
            'date' : row['temporal'],
        })

    return js

if __name__ == '__main__':
    app.run()
