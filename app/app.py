import os
from flask import Flask, render_template

template_dir = os.path.abspath('web')
app = Flask(__name__, template_folder = template_dir)

@app.route('/')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run()