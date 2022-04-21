# Building a RESTful Blog with Editing!
### Overview
##### This Capstone project is a part of [100 days of python code with Angela Yu](https://www.udemy.com/course/100-days-of-code) Where we are going to update our blog that we did before so we need to download the starter code folder to start this project or you can start it from scratch as will here the [Starter Code](https://att-c.udemycdn.com/2021-11-09_16-49-47-da8341ecf42d031e24b28e1e95c0e635/original.zip?response-content-disposition=attachment%3B+filename%3DStarting%2BFiles%2B-%2BRESTful-blog-start.zip&Expires=1650590444&Signature=U~BHMCN9VfauqoVIxeUKfnfo7zywwykNRfKhL9XsTmYr8ToOjLZ7VxIVktYwMHvvLZxUjjhFH4YQFGzq1TcHBLTvJKCxsycL3Xa4DzT2n8pzzVdLhvz4GbblWOCW0TbYOq-~z1ZBpz8N9mzrnacR5JW-a-pM2WFSjwE2F2HZJy7DVk719Gl~tsILIcvsZ53FkqwiBEs0IPTSF1UBEZbjsbh05WAo-h0n7lJMbax8vyTp0zWXnI07JflY2b15beY2tnCIVus47F9rn4cgkQzDBl8eLSgQXp4WXxqW1l3lu-bTTtw545cvsfvn0WpsmGkPfiZiz8CjDEK-KHsen9iPyA__&Key-Pair-Id=APKAITJV77WS5ZT7262A).

![final results2](https://user-images.githubusercontent.com/57592040/164546312-94a7ce71-77e6-4ce1-81cf-828f3d69e4c9.gif)

## STEP ONE : GET Blog Post Items
As we know that to have RESTful API you need to fellow the most two important roles:
1- Use HTTP Methods

2- Use Route and Endpoints

So our first step is to load our posts and render it to our home page and to do so we need to load all posts from **BlogPost** Model that will create a table for our database.

Here our **BlogPost Model** Columns contained:

```python
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
```

and now we need to create our route function as below:

```python
@app.route('/')
def get_all_posts():
    posts = [post for post in db.session.query(BlogPost).all()]
    # Or you can load posts by this way : BlogPost.query.all()
    return render_template("index.html", all_posts=posts)
```

and in our home page we can loop throw **all_posts** with Jinja 2 like this:

```html
{% for post in all_posts %}
<div class="post-preview">
  <a href="{{ url_for('show_post', index=post.id) }}">
    <h2 class="post-title">
      {{post.title}}
    </h2>
    <h3 class="post-subtitle">
      {{post.subtitle}}
    </h3>
  </a>
  <p class="post-meta">Posted by
    <a href="#">{{post.author}}</a>
    on {{post.date}} <a href="{{ url_for('delete_post', post_id=post.id) }}">✘</a></p>
</div>
<hr>
{% endfor %}
```

So far we are done from first step and we load all post in our home page.

## STEP TWO : POST a NEW Blog Post

Here we are going to add a new route that let us add a new post when the user click on the **"Create New Post"**  as below:

![creat new post](https://user-images.githubusercontent.com/57592040/164560203-9c9d9c2a-c0d4-43d6-af21-3a2deb98446d.gif)

as we see when I click on **Create New Post** it will render make-post.html page and the amazing thing we gonna learn is using Flask CKEditor package to make the Blog Content (body) input in the WTForm into a full CKEditor.

**First** we need to install this package by

```python
$ pip install flask-ckeditor
```

Second we need to import CKEditor and CKEditorField from flask_ckeditor like this:

```python
from flask_ckeditor import CKEditor, CKEditorField
```

And Finally this extension needs to be initialized in the usual way before it can be used:

```python
ckeditor = CKEditor(app)
```

and Our WTForm CreatePostForm will look like this:

```python
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")
```

as you see with body form attribute we used CKEditorField that will create the editor for us.
to create our form we are going to use Flask Bootstrap package to create quick form and we explain how to do that before and if you need more info you can take a look for the documentation [here](https://pythonhosted.org/Flask-Bootstrap/forms.html).

Now we need to create our route function like this :

```python
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
```

As you see I create an instance form from **CreatePostForm WTForm** then we checked which action we are going to do if we are going to **Create New post** or **Edit Post** by clicking the button, so if I clicked **Create New post button** we will pass New Blog Post to update our h1 page heading else if we clicked on **Edit post button** we will pass Edit Post as showing below:
![update heading as action](https://user-images.githubusercontent.com/57592040/164565163-a128052b-a48f-4d5b-a668-b2954465415c.gif)

Now we are going edit our make-post web page to add our WTForm and load ckeditor as well as below:

```html
<div class="container">
  <div class="row">
    <div class="col-lg-8 col-md-10 mx-auto">
      
        <!-- This is where the form will go -->
      <!-- Load ckeditor -->
      {{ ckeditor.load() }}

      <!-- Configure the ckeditor to tell it which field in WTForm will need to be a CKEditor. -->
      {{ ckeditor.config(name='body') }}

      <!-- Add WTF quickform -->
      {{ wtf.quick_form(form,button_map= {'submit': 'primary'},novalidate=True) }}

    </div>
  </div>
</div>
```
