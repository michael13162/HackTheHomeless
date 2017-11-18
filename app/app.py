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
    print(request.get_json())
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
    print(request.get_json())
    user_id = get_user_id(request)
    js = get_user_data(user_id)
    print(json.dumps(js))
    return Response(json.dumps(js), mimetype='application/json')

@app.route('/api/account/user/<int:user_id>', methods=['GET'])
def user_by_id(user_id):
    print(request.get_json())
    js = get_user_data(user_id)
    return Response(json.dumps(js), mimetype='application/json')

@app.route('/api/account/user/transactions', methods=['POST'])
def transactions():
    print(request.get_json())
    user_id = get_user_id(request)
    js = get_user_transactions(user_id)
    return Response(json.dumps(js), mimetype='application/json')

@app.route('/api/account/user/donations', methods=['POST'])
def donations():
    print(request.get_json())
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
        spenderId = get_spender_id(publicHash)
        if (spenderId == None):
            return message_response(400, 'ERROR', 'application/json')

    query = '''
            select * from purchases where spenderId=\'%s\'
                order by temporal desc;
            ''' % (spenderId)
    rows = query_db(query)

    js = { 'purchases' : [], 'spenderId' : spenderId }
    purchases = js['purchases']
    for row in rows:
        purchases.append({
            'spenderId' : spenderId,
            'amount' : row['amount'],
            'description' : row['description'],
            'date' : row['temporal']
        })

    return Response(json.dumps(js), mimetype='application/json')

@app.route('/api/account/user/donate', methods=['POST'])
def donate():
    '''
    gets spenderId, email, password
    '''
    user_id = get_user_id(request)
    donate_info = request.get_json()
    print('donate_info: ' + str(donate_info))
    spender_id = donate_info['spenderId']
    amount = donate_info['amount']

    if amount > get_user_data(user_id)['balance']:
        return message_response(400, 'The user does not have enough balance for this donation amount', 'application/json')

    print('spender_id: ' + spender_id)
    print('user_data: ' + str(get_user_data(user_id)))
    print('spender_data: ' + str(get_user_data(spender_id)))
    blockchain.processTransaction(get_user_data(user_id)['qr'], get_user_data(spender_id)['qr'], amount)

    query = 'insert into donations(donorId, spenderId, amount, temporal) values(\'%s\', \'%s\', \'%s\', datetime())' % (
        user_id,
        spender_id,
        amount
    )
    insert_id = insert_db(query)
    return message_response(200, str(insert_id) + 'The donation was successful!', 'application/json')

@app.route('/api/account/user/buy', methods=['POST'])
def buy():
    '''
    gets email, password, amount
    '''
    print(request.get_json())
    user_id = get_user_id(request)
    user_data = get_user_data(user_id)
    publicHash = user_data['qr']
    amount = request.get_json()['amount']

    balance = blockchain.getBalance(publicHash)
    new_balance = balance + amount
    blockchain.setBalance(publicHash, new_balance)

    js = { 'balance' : new_balance }
    return Response(json.dumps(js), mimetype='application/json')

@app.route('/api/account/user/purchase', methods=['POST'])
def purchase():
    '''
    gets amount, description, email, password, publicHash
    POV of sellers purchasing HTH
    '''
    user_id = get_user_id(request)
    purchase_info = request.get_json()
    print(purchase_info)

    amount = purchase_info['amount']
    description = purchase_info['description']
    spenderId = get_spender_id(purchase_info['publicHash'])
    if (spenderId == None):
        return message_response(400, 'ERROR', 'application/json')

    if amount > get_user_data(spenderId)['balance']:
        return message_response(400, 'The spender does not have enough balance for this purchase amount', 'application/json')

    blockchain.processTransaction(get_user_data(spenderId)['qr'], get_user_data(user_id)['qr'], amount)

    query = 'insert into purchases(spenderId, amount, description, temporal) values(\'%s\', \'%s\', \'%s\', datetime())' % (
        spender_id,
        amount,
        description
    )
    insert_id = insert_db(query)
    return message_response(200, str(insert_id) + 'The transaction was successful!', 'application/json')

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
    return Response(json.dumps("{'message':'" + message + "'}"), status=status_code, mimetype=mime_type)

def check_user_rows(rows):
    if (len(rows) == 0):
        return message_response(400, 'There are no users with these credentials', 'application/json')
    if (len(rows) > 1):
        return message_response(400, 'There is more than one user with these credentials', 'application/json')
    return None

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
    if check_user_rows(rows) != None:
        return None

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
    if check_user_rows(rows) != None:
        return None

    user = rows[0]

    print(user)

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
        if (name == None):
            return message_response(400, 'ERROR', 'application/json')
        donations.append({
            'spenderId' : spenderId,
            'name' : name,
            'amount' : row['amount'],
            'date' : row['temporal'],
        })

    return js

def get_spender_id(publicHash):
    query = 'select * from users where publicHash=\'%s\'' % (publicHash)
    rows = query_db(query)
    if check_user_rows(rows) != None:
        return None
    return rows[0]['id']

if __name__ == '__main__':
    app.run()
