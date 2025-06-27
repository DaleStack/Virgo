# Virgo 🌌 — A Beginner-Friendly Python Web Framework

**Virgo** is a minimal, batteries-included web framework written in Python.  
Built for learning — inspired by Django, but simplified for clarity.

---

## 📦 Features
- WSGI-compatible dev server
- Gunicorn(Linux/MacOS) and Waitress(Windows) Ready
- CLI for starting new apps
- App-based Structure
- Dynamic Routing
- Per-app templates and static files
- Jinja2-powered Templating engine
- Context Passing Support
- SQLite Database
- SQLAlchemy-powered ORM
- Query Helper
---

## 🚀 Getting Started

## Create a new app

```bash
#bash
py virgo.py lightstart blog

```

#### Creates:
```bash
apps/
  blog/
    __init__.py
    models.py
    routes.py
    templates/
    static/
```

#### Routes Initial View:
```Python
#apps/blog/routes.py
from virgo.core.routing import routes
from virgo.core.response import Response, redirect
from virgo.core.template import render

def sample(request):
    return Response("Welcome to Virgo!")
routes["/sample"] = sample
```
--
## Run The Server

#### Import your app in virgo.py:
```Python
#virgo.py
import apps.blog.routes
```

#### Then start the dev server:
```bash
#bash
py virgo.py lightserve
```

#### Visit:
```bash
http://127.0.0.1:8000/sample
```

## Creating Own Function

#### Create new function:
```Python
#apps/blog/routes.py
from virgo.core.routing import routes
from virgo.core.response import Response, redirect
from virgo.core.template import render

def sample(request):
    return Response("Welcome to Virgo!")
routes["/sample"] = sample

# Define new function
def new_function(request):
  return Response("This is a new function")
routes["/"] = new_function
# routes["/"] is the Route Path
# new_function is the name of the function
```

#### Remember to import your app in virgo.py (If you haven't done it yet):
```Python
#virgo.py
import apps.blog.routes
```

#### Start the dev server again:
```bash
#bash
py virgo.py lightserve
```

#### Visit:
```bash
http://127.0.0.1:8000/
```

## Dynamic Routing

#### Define a function with an extra parameter:
```Python
def profile_view(request, name):
  return Response(f"This is {name}'s Profile")
routes["/profile/<name>"] = profile_view
```

#### Restart the dev server:
```bash
#bash
py virgo.py lightserve
```

#### Visit:
```bash
http://127.0.0.1:8000/profile/JohnDoe
```

#### Result:
```bash
This is JohnDoe's Profile
```

## Templating

#### File Structure:
```bash
apps/
  example_app/
    __init__.py
    models.py
    routes.py
    templates/
    static/
```

#### Navigate to routes.py and create a function that will return a render() function:

```Python
def example(request):
  return render("home.html", app="example_app")
routes["/example"] = example

# "home.html" is the name of the template
# app="example_app" is the name of the app
```

#### Create a template in your app's templates folder:
```bash
apps/
  example_app/ # app="example_app" is referring to this
    __init__.py
    models.py
    routes.py
    templates/
      home.html #Your Template
    static/
```

#### Navigate to home.html and build your template:

```HTML
<!--example_app/templates/home.html-->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Example Template</title>
</head>
<body>
  <h1>This is my template</h1>
</body>
</html>
```

#### Import your app in virgo.py:
```Python
#virgo.py
import apps.example_app.routes
```

#### Run the dev server:
```bash
#bash
py virgo.py lightserve
```

#### Visit:
```bash
http://127.0.0.1:8000/example
```

## Static File

#### Create a stylesheet in your app's static folder:
```bash
apps/
  example_app/ 
    __init__.py
    models.py
    routes.py
    templates/
      home.html 
    static/ 
      style.css # Your stylesheet
```

#### Add style:
```CSS
/** example_app/static/style.css */

h1 {
  background-color: chocolate;
}

```

#### Go back to your template and link your stylesheet:

```HTML
<!--example_app/templates/home.html-->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Example Template</title>
  <link rel="stylesheet" href="static/example_app/style.css"></link> 
  <!-- This is how you should link: static/<app_name>/<stylesheet name> -->
</head>
<body>
  <h1>This is my template</h1>
</body>
</html>
```

#### Re-run the dev server:
```bash
#bash
py virgo.py lightserve
```

#### Visit:
```bash
http://127.0.0.1:8000/example
```
and you should see the styles working.

## Context Passing

### There are TWO ways to pass a context:

#### First:
```Python
def example(request):

  context = {
    "name":"John Doe"
    "age": 30
  }

  return render("home.html", context, app="example_app") # Context should be in the middle
routes["/example"] = example
```

#### Second:
```Python
def example(request):
  name = "John Doe"
  age = 30

  return render("home.html", {"name":name, "age":age}, app="example_app") 
routes["/example"] = example
```

### Calling context from a template:
```HTML
<!--example_app/templates/home.html-->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Example Template</title>
</head>
<body>
  <h1>Hello my name is {{ name }}</h1>
  <h3>I am {{ age }} years old</h3>
</body>
</html>
```

## Database

### Model

#### Creating a Model:
Inside your app's models.py, create a simple model:
```Python
# apps/post/models.py
from sqlalchemy import Column, Integer, String
from virgo.core.database import Base
from virgo.core.mixins import BaseModelMixin

class Post(Base, BaseModelMixin):
  __tablename__ = "posts"

  id = Column(Integer, primary_key=True)
  title = Column(String)
  content = Column(String)
```

#### Run migrate:
```bash
py virgo.py lightmigrate
```
This command migrates of all the model and automatically creates a table.

You should see a **virgo.db** created at a project-level. (If it does not exist yet)

### Using the Model

#### Creating:
```Python
# apps/post/routes.py
from virgo.core.routing import routes
from virgo.core.response import Response, redirect
from virgo.core.template import render
from .models import Post # import your model

def post_create(request):
  if request.method == "POST":
    data = request.POST
    title = data.get("title")
    content = data.get("content")

    Post.create(title=title, content=content)
    # .create() is used to create a data in the model
    return redirect("/") # Go back to post list after submitting
    
  return render("post_create.html", app=post)
routes["/create"] = post_create
```

Creating data in the template:

```HTML
<!-- apps/post/templates/post_create.html -->
<h1>Create Post</h1>

<form method="POST"> <!-- it should be a POST method -->
  <input type="text" name="title" placeholder="Title"/>
  <textarea name="content" placeholder="Content"></textarea>
  <button type="submit">Create Post</button>
</form>
```

#### Reading/Listing:
```Python
# apps/post/routes.py
from virgo.core.routing import routes
from virgo.core.response import Response, redirect
from virgo.core.template import render
from .models import Post 

def post_list(request):
  posts = Post.all() 
  # .all() is used to fetch all the data in the model
  return render("post_list.html", {"posts":posts}, app=post)
routes["/"] = post_list
```

Looping through the data in the template:

```HTML
<!-- apps/post/templates/post_list.html -->
<h1>Post List</h1>

{% for post in posts %}
  <p>{{ post.title }}</p>
  <p>{{ post.content }}</p>
{% endfor %}
```

#### Updating:
```Python
# apps/post/routes.py
from virgo.core.routing import routes
from virgo.core.response import Response, redirect
from virgo.core.template import render
from .models import Post 

def post_update(request, id):
  post = Post.get(id)

  if not post:
    return Response("Post not found", status=404)
  
  if request.method == "POST":
    data = request.POST
    title = data.get("title")
    content = data.get("cpntent")
    post.update(title=title, content=content)
    # post is the instance
    # .update() is used for updating a data in the model
    return redirect("/")

  return render("post_update.html", {"post":post}, app=post)
routes["/update/<id>"] = post_update
```

Updating data in the template:

```HTML
<!-- apps/post/templates/post_update.html -->
<h1>Update Post</h1>

<form method="POST"> <!-- it should be a POST method -->
  <input type="text" name="title" value="{{ post.title }}"/>
  <textarea name="content" placeholder="Content">{{ post.content }}</textarea>
  <button type="submit">Update Post</button>
</form>
```

#### Deleting:
```Python
# apps/post/routes.py
from virgo.core.routing import routes
from virgo.core.response import Response, redirect
from virgo.core.template import render
from .models import Post 

def post_delete(request, id):
  post = Post.get(id)

  if not post:
    return Response("Post not found", status=404)
  
  post.delete() 
  # .delete() is used to remove an instance in the database
  return redirect("/")

  return render("post_delete.html", app=post)
routes["/delete/<id>"] = post_delete
```

Using the functon in the template:

```HTML
<!-- apps/post/templates/post_list.html -->
<h1>Post List</h1>

{% for post in posts %}
  <p>{{ post.title }}</p>
  <p>{{ post.content }}</p>
  <a href="/delete/{{ post.id }}">Delete</a> <!-- Deleting -->
  <a href="/update/{{ post.id }}">Edit</a>
{% endfor %}
```

## Authentication

### Built-in UserModel

#### Creating a User model:
```Python
# apps/user/models.py
from sqlalchemy import Column, Integer, String
from virgo.core.database import Base
from virgo.core.mixins import BaseModelMixin
from virgo.core.auth import UserModel # import built-in User Model

class User(UserModel):
  pass
```

Run migrate in terminal:
```bash
py virgo.py lightmigrate
```
this should put a users table in the database.

#### Register a User:
```Python
# apps/user/routes.py
from virgo.core.routing import routes
from virgo.core.response import Response, redirect
from virgo.core.template import render
from virgo.core.auth import UserAlreadyExists # import this Exception
from .models import User # import your User model

def register_view(request):
  if request.method == "POST":
    data = request.POST
    username = data.get("username")
    password = data.get("password")

    try:
      User.register(username, password) # .register() is used to register a user
      return User.authenticate(request, username, password)
    except UserAlreadyExists:
      error = "Username already taken."
      return render("register.html", {"error":error}, app="user")

  return render("register.html", app="user")
routes["/register"] = register_view
```

#### Registration template view:
```HTML
<!-- apps/user/templates/register.html -->
<h1>Register User</h1>
<form action="" method="POST">
    {% if error %}
        <p style="color: red;">{{ error }}</p>
    {% endif %}
    <input type="text" name="username" placeholder="username">
    <input type="password" name="password" placeholder="password">
    <button type="submit">Register</button>
</form>
```




