from flask import Flask,render_template

app = Flask(__name__)

ENV = 'dev'
if ENV == 'prod':
    app.debug = False
else:
    app.debug = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run()