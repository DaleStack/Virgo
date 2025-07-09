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

## 📄 License

Virgo Framework is open source under the [MIT License](LICENSE).


## 🚀 Getting Started

## Clone Repository
```bash
git clone --depth=1 https://github.com/DaleStack/Virgo.git .
```

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

Registration template view:
```HTML
<!-- apps/user/templates/register.html -->
<h1>Register User</h1>
{% if error %}
  <p style="color: red;">{{ error }}</p>
{% endif %}
<form action="" method="POST">
    <input type="text" name="username" placeholder="username">
    <input type="password" name="password" placeholder="password">
    <button type="submit">Register</button>
</form>
```

#### Login as a User:
```Python
# apps/user/routes.py
from virgo.core.routing import routes
from virgo.core.response import Response, redirect
from virgo.core.template import render
from virgo.core.auth import UserAlreadyExists 
from .models import User 

def login_view(request):
  if request.method == "POST":
    data = request.POST
    username = data.get("username")
    password = data.get("password")

    user = User.first_by(username=username)
    if not user or not user.check_password(password):
      error = "Invalid username or password"
      return render("login.html", {"error":error}, app="user")
    
    return User.authenticate(request, username, password)
    

  return render("login.html", app="user")
routes["/login"] = login_view
```

Login template view:
```HTML
<!-- apps/user/templates/login.html -->
<h1>Login User</h1>
{% if error %}
  <p style="color: red;">{{ error }}</p>
{% endif %}
<form action="" method="POST">
    <input type="text" name="username" placeholder="username">
    <input type="password" name="password" placeholder="password">
    <button type="submit">Login</button>
</form>
```

#### Redirecting after authentication:

Open up your settings.py:
```Python
# settings.py

LOGIN_REDIRECT_ROUTE="/example" 
# Usage: What /<route> do you want users to be redirected to, after authenticating

LOGIN_ROUTE="/login" # This is your login page route
# This will be used for redirecting users who are unauthorized and accessing protected routes
# We'll get back to this in a minute...

LOGOUT_REDIRECT_ROUTE="/" 
# Used for redirecting users after logging out 
```

#### Protected routes:
```Python
# apps/user/routes.py
from virgo.core.routing import routes
from virgo.core.response import Response, redirect
from virgo.core.template import render
from virgo.core.auth import UserAlreadyExists 
from .models import User 
from virgo.core.decorators import login_required # import this login_required decorator

@login_required(User) # pass your user model as the parameter
def dashboard(request):
  user = request.user # request.user is used to fetch the currently logged-in user

  return render("dashboard.html", {"user":user}, app="user")
routes["/dashboard"] = dashboard
```

Dashboard template view:
```HTML
<!-- apps/user/templates/dashboard.html -->
<h1>Hello, {{ user.username }}!</h1>
```

This is also where **LOGIN_ROUTE** comes to play:

If a user who is not logged-in tries to access "/dashboard" (a protected route),
They will be redirected to the login page, preventing them from accessing protected data.

#### Logout:
```Python
# apps/user/routes.py
from virgo.core.routing import routes
from virgo.core.response import Response, redirect
from virgo.core.template import render
from virgo.core.auth import UserAlreadyExists 
from .models import User 
from virgo.core.decorators import login_required

@login_required(User)
def logout_view(request):
  user = request.user 

  if user:
    return user.logout(request) # .logout is used to clear session
    # LOGOUT_REDIRECT_ROUTE will be executed upon logout
routes["/logout"] = logout_view
```

Dashboard template view:
```HTML
<!-- apps/user/templates/dashboard.html -->
<h1>Hello, {{ user.username }}!</h1>
<a href="/logout">Logout</a>
```

### Role-based Routing

#### Modifying the UserModel:
Go to virgo/core/auth.py
```Python
# virgo/core/auth.py
class UserModel(Base, BaseModelMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="student") # add a role column eg. student or teacher
    # make sure it's also called exactly "role" because virgo has a built-in decorator
```

Run migrate:
```bash
py virgo.py lightmigrate
```

For role to be accepted in registration:

```Python
# virgo/core/auth.py
@classmethod
    def register(cls, username, password, role): # pass the role as a parameter
        if cls.first_by(username=username):
            raise UserAlreadyExists("Username already taken")

        hashed = cls.hash_password(password)
        return cls.create(username=username, password=hashed, role=role) # also pass here for the role to be created
```

#### Register role-based model:
```Python
# apps/user/routes.py
def register_view(request):
    if request.method == "POST":
        data = request.POST
        username = data.get("username")
        password = data.get("password")
        role = data.get("role")

        try:
            user = User.register(username, password, role)
            return User.authenticate(request, username, password)
        except UserAlreadyExists:
            error = "Username already taken"
            return render("register.html", {"error": error}, app="post")
        
    return render("register.html", app="post")
routes["/register"] = register_view
```

#### Register role-based template:
```HTML
<h1>Register User</h1>
<form action="" method="POST">
    {% if error %}
        <p>{{ error }}</p>
    {% endif %}
    <input type="text" name="username" placeholder="username">
    <input type="password" name="password" placeholder="password">
    <select name="role" id="">
        <option value="student">Student</option>
        <option value="teacher">Teacher</option>
    </select>
    <button type="submit">Register</button>
</form>
```

If there are two or more roles, how can I get the LOGIN_REDIRECT_ROUTE to work if it only takes 1 route? you may ask. Here's how:
```Python
# settings.py

LOGIN_REDIRECT_ROUTE="/dashboard" 

LOGIN_ROUTE="/login"

LOGOUT_REDIRECT_ROUTE="/" 

# Virgo has this
ROLE_ROUTES = {
  "student": "/student/dashboard", # role first, then route
  "teacher": "/teacher/dashboard"
}

# If your system have no roles, leave ROLE_ROUTES empty, your fall back will be LOGIN_REDIRECT_ROUTE

FORBIDDEN_REDIRECT_ROUTE="/forbidden"
# This will be your role checker fall back, if a student tried to access "/teacher/dashboard" (vice versa)
# They will be redirected to this route

```

#### Role-based function:
```Python
# apps/user/routes.py
from virgo.core.routing import routes
from virgo.core.response import Response, redirect
from virgo.core.template import render
from virgo.core.auth import UserAlreadyExists 
from .models import User 
from virgo.core.decorators import login_required, role_required # import role_required from decorators

@login_required(User)
@role_required("student")
def student_dashboard(request):
  user = request.user

  return render("student_dashboard.html", {"user":user}, app="user")
routes["/student/dashboard"] = student_dashboard # route should be the same as the one in the ROLE_ROUTES

@login_required(User)
@role_required("teacher")
def teacher_dashboard(request):
  user = request.user

  return render("teacher_dashboard.html", {"user":user}, app="user")
routes["/teacher/dashboard"] = teacher_dashboard 

def forbidden(request):
  return render("forbidden.html", app="user")
routes["/forbidden"] = forbidden # this will be your FORBIDDEN_REDIRECT_ROUTE

```

## Relationships (ORM)

#### Create apps called post and user:
We will try to make an application with proper file structure that's why we will create two apps

```bash
py virgo.py lightstart post
```

```bash
py virgo.py lightstart user
```

#### Create Post model:
Navigate to your post app's **models.py**

```Python
# apps/post/models.py

from sqlalchemy import Column, Integer, String, ForeignKey # Import ForeignKey
from sqlalchemy.orm import relationship # Import relationship
from virgo.core.database import Base
from virgo.core.mixins import BaseModelMixin
from virgo.core.auth import UserModel # Import Base UserModel

class Post(Base, BaseModelMixin):
  __tablename__ = "posts"

  id = Column(Integer, primary_key=True)
  title = Column(String)

  user_id = Column(Integer, ForeignKey("users.id")) # Connect Post model to ForeignKey

  author = relationship("UserModel", back_populates="posts") # Create relationship to Base UserModel
```

#### Modify Base UserModel:
Navigate to virgo/core/auth.py

```Python
# virgo/core/auth.py

from sqlalchemy import Column, Integer, String
from virgo.core.database import Base
from virgo.core.mixins import BaseModelMixin
from virgo.core.session import create_session, get_session, destroy_session
from virgo.core.response import Response, redirect
from settings import LOGIN_REDIRECT_ROUTE, LOGOUT_REDIRECT_ROUTE, ROLE_ROUTES
import bcrypt
from sqlalchemy.orm import relationship # Import relationship

class UserModel(Base, BaseModelMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    posts = relationship("Post", back_populates="author") # Create relationship to Post Model
```
This alone won't be migrated in the database, that's why we need the user app.

#### Create User model:
```Python
# apps/user/models.py

from sqlalchemy import Column, Integer, String
from virgo.core.database import Base
from virgo.core.mixins import BaseModelMixin
from virgo.core.auth import UserModel # Import UserModel

class User(UserModel): # Pass UserModel as a parameter
    pass
```

Creating Login and Register function will just be the same.

#### Creating Data in relation with the User
```Python
# apps/post/routes.py

from virgo.core.routing import routes
from virgo.core.response import Response, redirect
from virgo.core.template import render
from virgo.core.decorators import login_required
from apps.user.models import User
from .models import Post

@login_required(User)
def create_post(request):
    user = request.user
    
    if request.method == "POST":
        data = request.POST
        title = data.get("title")

        Post.create(title=title, user_id=user.id) # pass the data, as well as the currently logged-in user's id
        return redirect("/")
    return render("create_post.html", app="post")
routes["/create-post"] = create_post
```

#### Listing the Data
```Python
# apps/post/routes.py

from virgo.core.routing import routes
from virgo.core.response import Response, redirect
from virgo.core.template import render
from virgo.core.decorators import login_required
from apps.user.models import User
from .models import Post

@login_required(User)
def list_post(request):
    user = request.user
    posts = Post.filter_by(user_id=user.id, load=["author"])
    return render("list_post.html", {"posts":posts, "user":user}, app="post")
routes["/"] = list_post
```
This is a simple **One-to-Many** Relationship

### One-to-One
Soon
### Many-to-Many
Soon

## Querying
We will tackle all of the built-in query helpers available in Virgo

Let's say we have a Note model with only a title field
#### CREATE:
**.create()**
```Python
# apps/note/routes.py
from .models import Note

def create_note(request):
  if request.method == "POST":
    data = request.POST
    title = data.get("title")

    Note.create(title=title)

    return redirect("/")
  return render("create_note.html", app="note")
routes["/create_note"] = create_note
```

#### READ:
**.all()**
Can load relation
```Python
# apps/note/routes.py
from .models import Note

def list_post(request):
    user = request.user
    posts = Post.filter_by(user_id=user.id, load=["author"])
    return render("list_post.html", {"posts":posts, "user":user}, app="post")
routes["/"] = list_post
```

**.get()**
Note: get() is jsut a wrapper of get_by_id() so this will only work for id
```Python
# apps/note/routes.py
from .models import Note

def get_note(request, id):
  note = Note.get(id)

  if not note:
    return Response("Note not found!", status=404)
  
  return render("get_note.html", {"note":note}, app="note")
routes["/get_note/<id>"] = get_note
```

**.filter_by()**
Can load relation
```Python
# apps/note/routes.py
from .models import Note

def filtered_note(request):
  notes = Note.filter_by(title="hello")

  if not notes:
    return Response("No notes were found!", status=404)
  
  return render("filtered_note.html", {"notes":notes}, app="note")
routes["/filtered_note"] = filtered_note
```

**first_by()**
```Python
# apps/note/routes.py
from .models import Note

def filtered_note(request):
  note = Note.first_by(title="hello")

  if not note:
    return Response("No notes were found!", status=404)
  
  return render("first_note.html", {"note":note}, app="note")
routes["/first_note"] = first_note
```

**order_by()**
Can load relation
```Python
# apps/note/routes.py
from .models import Note

def ordered_note(request):
  notes = Note.order_by("title") # asc by default, add "desc" to make it descending ("title", "desc")

  if not notes:
    return Response("No notes were found!", status=404)
  
  return render("order_note.html", {"notes":notes}, app="note")
routes["/ordered_note"] = ordered_note
```

**filter_and_order_by()**
Can load relation
```Python
# apps/note/routes.py
from .models import Note

def filtered_and_ordered_note(request):
  user = request.user
  notes = Note.filter_and_order_by(user_id=user.id, order_field="title", direction="desc", load=["author"])

  if not notes:
    return Response("No notes were found!", status=404)
  
  return render("filter_order_note.html", {"notes":notes}, app="note")
routes["/filtered_and_ordered_note"] = filtered_and_ordered_note
```

#### UPDATE:
**.update()**
```Python
# apps/note/routes.py
from .models import Note

def update_note(request, id):
  note = Note.get(id)

  if not note:
    return Response("Note not found!", status=404)

  if request.method == "POST":
    data = request.POST
    title = data.get("title")
    note.update(title=title)
    return redirect("/")  
  return render("update_note.html", {"note":note}, app="note")
routes["/update_note/<id>"] = update_note
```

#### DELETE:
**.delete()**
```Python
# apps/note/routes.py
from .models import Note

def delete_note(request, id):
  note = Note.get(id)

  if not note:
    return Response("Note not found!", status=404)

  note.delete()
  return redirect("/")
  return render("delete_note.html", app="note")
routes["/delete_note/<id>"] = delete_note
```

