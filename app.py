from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

app = Flask(__name__)

#const variables
username_post = []

ENV = 'dev'
if ENV == 'dev':
    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:P@ssword1@localhost/blog'
else:
    app.debug = False
    app.config["SQLALCHEMY_DATABASE_URI"] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

session = sessionmaker()
engine = create_engine('postgresql://postgres:P@ssword1@localhost/blog')
session.configure(bind=engine)
session = session()

#create model
class Blog(db.Model):
    __tablename__ = 'blog'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = password

#create model for post
class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20))
    title = db.Column(db.String(10))
    content = db.Column(db.Text())

    def __init__(self,username,title,content):
        self.username = username
        self.title = title
        self.content = content

@app.route('/')
def index():
    post_index = Post.query.all()
    return render_template('index.html', post_index = post_index)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/user')
def user():
    try:
        if username_post[0] == '':
            post_index = Post.query.all()
            return render_template('index.html',msg='Please login', post_index = post_index)
        else:
            current_user = Post.query.filter(Post.username == username_post[0]).all()
            return render_template('user_page.html',username = username_post[0],all_post = current_user)
    except IndexError:
        post_index = Post.query.all()
        return render_template('index.html',msg='Please login', post_index = post_index)


@app.route('/register_submit', methods=['POST'])
def register_submit():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if username == '' or email == '' or password == '':
            return render_template('register.html', msg='please enter all the fields')
        else:
            if(db.session.query(Blog).filter(Blog.username == username).count() == 0):
                data = Blog(username,email,password)
                db.session.add(data)
                db.session.commit()            
            return render_template('login.html')

@app.route('/login_submit',methods=['POST'])
def login_submit():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        all_post = Post.query.filter(Post.username == username).all()
        if(db.session.query(Blog).filter(Blog.username == username,Blog.password == password).count() == 1):
            username_post.insert(0,username)
            return render_template('user_page.html', username = username, text= 'user page', all_post = all_post)
        else:
            return render_template('login.html',msg='Please login with correct credentials')

@app.route('/user_page/<username>',methods=['POST'])
def user_page(username):
    if request.method == 'POST':
        title = request.form['post_title']
        content = request.form['post_content']
        data = Post(username,title,content)
        db.session.add(data)
        db.session.commit()
        all_post = Post.query.filter(Post.username == username).all()
        return render_template('user_page.html', all_post = all_post)


@app.route('/edit_page/<id>', methods=['GET'])
def edit_page(id):
    try:
        if len(username_post[0]) >= 1:
            page = Post.query.get(id)
            return render_template('edit_page.html',id = page.id, username = page.username, title = page.title, content = page.content)
    except IndexError:
        post_index = Post.query.all()
        return render_template('index.html',msg='Please login', post_index = post_index)
    

@app.route('/edit_page_commit/<id>', methods=['POST'])
def edit_page_commit(id):
    try:
        if len(username_post[0]) >= 1:
                edit_title = request.form['edit_post_title']
                edit_content = request.form['edit_post_content']
                edit = Post.query.get(id)
                edit.title = edit_title
                edit.content = edit_content
                db.session.commit()
                return user()
    except IndexError:
        post_index = Post.query.all()
        return render_template('index.html',msg='Please login', post_index = post_index)


@app.route('/delete_page/<id>', methods=['GET'])
def delete_page(id):
    try:
        if len(username_post[0]) >= 1:
                Post.query.filter(Post.id == id).delete()
                db.session.commit()
                return user()
    except IndexError:
        post_index = Post.query.all()
        return render_template('index.html',msg='Please login', post_index = post_index)

@app.route('/user_logout')
def user_logout():
    try:
        if len(username_post[0]) >= 1:
            session.close()
            username_post.pop()
            return index()
    except:
        return index()

if __name__ == '__main__':
    app.run()