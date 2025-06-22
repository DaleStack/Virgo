# Virgo 🌌 — A Beginner-Friendly Python Web Framework

**Virgo** is a minimal, batteries-included web framework written in Python.  
Built for learning — inspired by Django, but simplified for clarity.

---

## 📦 Features
- WSGI-compatible dev server
- CLI for starting new apps
- App-based Structure
- Dynamic Routing
- Per-app templates and static files
- Context Passing Support
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
    routes.py
    templates/
    static/
```

#### Routes Initial View:
```Python
#apps/blog/routes.py
from virgo.core.routing import routes
from virgo.core.response import Response
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
from virgo.core.response import Response
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

  return render("home.html",{"name":name, "age":age}, app="example_app") # Context should be in the middle
routes["/example"] = example
```