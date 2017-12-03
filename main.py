from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

def getBlogs():
    return Blog.query.all()

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(40))
    text = db.Column(db.String(255))

    def __init__(self, title, text):
        self.title = title
        self.text = text

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        title_error = ''
        text_error = ''
        error_list = []
        title = request.form['title']
        text = request.form['text']
        if not title: # if title is empty
            error_list.append("Title was left empty")
            title_error = "*Blog title required"
        if not text: # if text is left empty
            error_list.append("Text was left empty")
            text_error = "*Blog text required"
        if title_error or text_error:
            return render_template('newpost.html', title_value=title, \
                text_value=text, errors=error_list, \
                text_error=text_error, \
                title_error=title_error)
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

if __name__ == '__main__':
    app.run()
