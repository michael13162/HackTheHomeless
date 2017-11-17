import json
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

@app.route('/api/account/register', methods=['POST'])
def register():
    account_info = request.form
    print(account_info)

@app.route('/api/account/user', methods=['GET'])
def user():
    email = request.args.get('email')
    password = request.args.get('password')
    print(email)
    print(password)

    js = []
    js.append("Yo Will")
    return Response(json.dumps(js), mimetype='application/json')

if __name__ == '__main__':
    app.run()
