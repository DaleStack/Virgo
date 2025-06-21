# Virgo 🌌 — A Beginner-Friendly Python Web Framework

**Virgo** is a minimal, batteries-included web framework written in Python.  
Built for learning — inspired by Django, but simplified for clarity.

---

## 📦 Features

- Dynamic Routing
- WSGI-compatible dev server
- Per-app templates and static files
- CLI for starting new apps

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