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
Here I want to mention that we can pass button map that its key is submit button and its bootstrap class is primary, for more info about quick form parameters you can check this documentation **[Here](https://pythonhosted.org/Flask-Bootstrap/forms.html#form-macro-reference)**.

Finally after we create our new post you will see that this post showing html tags so we need to fix it by not skip the html tags and render is as will and we can do that by using filter safe as below in our post html web page like this.  

```html
<div class="col-lg-8 col-md-10 mx-auto">
  <p>
    {{ post.body | safe }}
  </p>
   <hr>
   <div class="clearfix">
  <a class="btn btn-primary float-right" href="{{ url_for('edit_post',post_id=post.id, action='Edit Post')}}">Edit Post</a>
</div>
  </div>
```
last problem after submitting our Blog Post is when we check our post the body content will look like this:

![skip html tags](https://user-images.githubusercontent.com/57592040/164704451-bc95d698-0ded-4a94-99e4-8608a595e4e2.PNG)

To fix it we need to use safe filter when we load our post body with jinja expressions  as below:

```jinja2
{{ post.body | safe}}
```

## Attention

Using safe to render html tags in body content is dangerous, because any black hat could use this   **Security Bug** to Perform an attack called **XSS** or [**Cross Site Scripting**](https://owasp.org/www-community/attacks/xss/) in simple way it is an attack where the attacker injected your website with malicious scripts as showing below:

![XSS](https://user-images.githubusercontent.com/57592040/164716934-39926112-bc3a-493e-b87c-70e497b37efd.gif)

After you try to edit the same post you will not find the script tag that you wrote it but it is already saved on your Blogpost database as below:

![script saved  in db](https://user-images.githubusercontent.com/57592040/164718835-903b4a45-4d04-4d07-9df5-facbed4149a7.gif)

So I do not know how can I edit this configuration in Ckeditor but we can add side server process to clean the Markup string with bleach library  like code below:

```python
import bleach
 
## strips invalid tags/attributes
def strip_invalid_html(content):
    allowed_tags = ['a', 'abbr', 'acronym', 'address', 'b', 'br', 'div', 'dl', 'dt',
                    'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img',
                    'li', 'ol', 'p', 'pre', 'q', 's', 'small', 'strike',
                    'span', 'sub', 'sup', 'table', 'tbody', 'td', 'tfoot', 'th',
                    'thead', 'tr', 'tt', 'u', 'ul']
 
    allowed_attrs = {
        'a': ['href', 'target', 'title'],
        'img': ['src', 'alt', 'width', 'height'],
    }
 
    cleaned = bleach.clean(content,
                           tags=allowed_tags,
                           attributes=allowed_attrs,
                           strip=True)
 
    return cleaned
 
## use strip_invalid_html-function before saving body
body=strip_invalid_html(article.body.data)
 
## you can test the code by using strong-tag
```

And this code I got it from [Here](https://gist.github.com/angelabauer/7dbf4554ebba5fcccc5197bc1b857b7e) so before passing the Markup content from CKEditor to our database we are going to clean it first using the `strip_invalid_html(content)` function.

## STEP THREE : Edit Existing Blog Posts

And to do so we are going to add another end point that allow us to **Edit Existing Blog Post** and then add it to our **Edit Post button** so our end point route function will look like this:

```python
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    check_action = request.args.get("action")
    today_date = datetime.now()
    date_format = today_date.strftime("%B %d, %Y")
    post = db.session.query(BlogPost).filter(BlogPost.id == post_id).first()
    # Here we auto-populate the fields in the WTForm with the blog posts data.
    load_form_data = CreatePostForm(title=post.title,
                                    subtitle=post.subtitle,
                                    author=post.author,
                                    img_url=post.img_url,
                                    body=post.body
                                    )
    if request.method == "POST":
        if load_form_data.validate_on_submit():
            body_content = strip_invalid_html(request.form.get('body'))
            post.title = request.form.get('title')
            post.subtitle = request.form.get('subtitle')
            post.date = date_format
            post.author = request.form.get('author')
            post.img_url = request.form.get('img_url')
            post.body = body_content
            db.session.commit()
            return redirect(url_for('get_all_posts'))
    return render_template("make-post.html", form=load_form_data, action=check_action)
```

And I want to mention that to update the page heading from **New Blog Post** to **Edit Post** we can pass **action** parameter when we use `url_for` when the user click on Add New Blog Post or Edit Post as below:

for adding new post:

```html
<a class="btn btn-primary float-right" href="{{ url_for('add_new_post',post_id=None, action='New Post')}}">Create New Post</a>
```

And for edit post:

```html
<a class="btn btn-primary float-right" href="{{ url_for('edit_post',post_id=post.id, action='Edit Post')}}">Edit Post</a>
```

There is another way as Angela Yu provide [Here](https://gist.github.com/angelabauer/20715bb39cb3b2f824e0a3a282b5b9e5)

And why we didn't use PUT/PATCH Methods because HTML forms  Only use GET, POST Methods for more information [Here](https://softwareengineering.stackexchange.com/questions/114156/why-are-there-no-put-and-delete-methods-on-html-forms)

## STEP FOUR : DELETE Blog Posts

Final step in this project is to be able to delete Blog Posts and to do that we can add `/delete-post/<int:post_id>` end point and the route function will look as below:

```python
@app.route("/delete-post/<int:post_id>")
def delete_post(post_id):
    post = db.session.query(BlogPost).filter(BlogPost.id == post_id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("get_all_posts"))
```

and we add it to our home page as ✘ after the date of each post so when click on it the post will be delated and redirect you to the home page again:

```html
<a href="{{ url_for('delete_post', post_id=post.id) }}">✘</a>
```
