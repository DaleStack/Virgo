# Virgo 🌌 — A Beginner-Friendly Python Web Framework

**Virgo** is a minimal, batteries-included web framework written in Python.  
Built for learning and hacking — inspired by Django, but simplified for clarity.

---

## 📦 Features

- Manual + typed routing (`<int:id>`, `<str:name>`)
- Dynamic Routing
- WSGI-compatible dev server
- Per-app templates and static files
- CLI for starting new apps

---

## 🚀 Getting Started

### Create a new app

```bash
py virgo.py lightstart blog

apps/
  blog/
    __init__.py
    routes.py
    templates/
    static/
