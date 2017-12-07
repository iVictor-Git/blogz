from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'abc'

db = SQLAlchemy(app)

def getBlogs():
    return Blog.query.all()

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(40))
    text = db.Column(db.String(255))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, text, owner):
        self.title = title
        self.text = text
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True)
    password = db.Column(db.String(60))
    blogs = db.relationship('Blog', backref="owner")

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    owner = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        if not title: # if title is empty
            flash("Title was left empty", "error")
        if not text: # if text is left empty
            flash("Text was left empty")
        if not title or not text:
            return render_template('newpost.html', title_value=title)
        new_blog = Blog(title, text)
        db.session.add(new_blog)
        db.session.commit()
        return redirect('/blog?id=' + str(new_blog.id))
    return render_template('newpost.html', title="Build-a-Blog :: New Post")

@app.route('/blog')
def default():
    blog_id = request.args.get('id')
    if blog_id != None:
        blog = Blog.query.get(blog_id)
        return render_template('ind-blog-page.html', blog = blog)
    return render_template('blog.html', title="Build-a-Blog :: New Post", blogs=getBlogs())

@app.route('/signup', methods=['POST', 'GET'])
def signup():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        # if any fields are empty
        if not (username or password or verify): 
            if not username:
                flash('Username was left blank', "error")
            if not password:
                flash('Password was left blank', "error")
            if not verify:
                flash('Password verification left blank', "error")
            return redirect('/signup')
        
        #  checks for length of username and password being greater than length 3
        if not (len(username) > 2 or len(password) > 2):
            if not len(username) > 2:
                flash("Username does not meet length requirement of 3")
            if not len(password) > 2:
                flash("Password is not meet required length of 3")

        # if password doesn't equal the verify password field
        if not (password == verify):
            flash("Passwords do not match", "error")

        # check for an existing user
        # if existing user exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists")
            return redirect('/signup')


        user = User(username, password)
        db.session.add(user)
        db.session.commit()
        session['username'] = user.username
        return redirect('/newpost')

    return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == "POST":
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        
        # if user exists
        if user:
            password = request.form['password']
            
            #check if password doesn't match
            if password != user.password: 
                flash('Incorrect username or password')
                return redirect('/login')
            
            #otherwise redirect to /newpost
            session['username'] = user.username
            return redirect('/newpost') 

        # if user doesn't exist
        else: 
            flash("Username doesn't exist")
            return redirect('/login')

    return render_template('login.html')

# @app.route('/')
# def index():
#     return render_template('index.html')


@app.route('/logout')
def logout():
    del session['username']
    redirect('/blog')
    
if __name__ == '__main__':
    app.run()
