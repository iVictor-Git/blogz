from flask import Flask, request, redirect, render_template, flash
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

    def __init__(self, title, text):
        self.title = title
        self.text = text

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60))
    password = db.Column(db.String(60))
    blogs = db.relationship('Blog', backref="owner")

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

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

# @app.route('/register', methods=['POST', 'GET'])
# def register():

#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         verify = request.form['verify']

#         if not email:
#             flash('Email was left blank', "error")
#         if not password:
#             flash('Password was left blank', "error")
#         if not verify:
#             flash('Password verification left blank', "error")

#         if not (password == verify):
#             flash("Passwords do not match", "error")
    return render_template('signup.html')

# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     return render_template('login.html')

# @app.route('/index')
# def index():
#     return render_template('index.html')

if __name__ == '__main__':
    app.run()
