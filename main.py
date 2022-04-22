from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
# enable CSRF protection
app.config['CKEDITOR_ENABLE_CSRF'] = True
csrf = CSRFProtect(app)
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


@app.route('/')
def get_all_posts():
    posts = [post for post in db.session.query(BlogPost).all()]
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = db.session.query(BlogPost).filter(BlogPost.id == index).first()
    return render_template("post.html", post=requested_post)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/make-post", methods=["POST", "GET"])
def add_new_post():
    form = CreatePostForm()
    check_action = request.args.get("action")
    today_date = datetime.now()
    date_format = today_date.strftime("%B %d, %Y")
    if request.method == "POST":
        if form.validate_on_submit():
            new_post = BlogPost(title=request.form.get('title'),
                                subtitle=request.form.get('subtitle'),
                                date=date_format,
                                author=request.form.get('author'),
                                img_url=request.form.get('img_url'),
                                body=request.form.get('body')
                                )
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('get_all_posts'))
    else:
        return render_template("make-post.html", form=form, action=check_action)


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    check_action = request.args.get("action")
    today_date = datetime.now()
    date_format = today_date.strftime("%B %d, %Y")
    post = db.session.query(BlogPost).filter(BlogPost.id == post_id).first()
    load_form_data = CreatePostForm(title=post.title,
                                    subtitle=post.subtitle,
                                    author=post.author,
                                    img_url=post.img_url,
                                    body=post.body
                                    )
    if request.method == "POST":
        if load_form_data.validate_on_submit():
            post.title = request.form.get('title')
            post.subtitle = request.form.get('subtitle')
            post.date = date_format
            post.author = request.form.get('author')
            post.img_url = request.form.get('img_url')
            post.body = request.form.get('body')
            db.session.commit()
            return redirect(url_for('get_all_posts'))
    return render_template("make-post.html", form=load_form_data, action=check_action)


@app.route("/delete-post/<int:post_id>")
def delete_post(post_id):
    post = db.session.query(BlogPost).filter(BlogPost.id == post_id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("get_all_posts"))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
