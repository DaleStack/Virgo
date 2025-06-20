import os
from virgo.core.response import Response

def render(template_name, context=None, app=None):
    context = context or {}

    # Determine template path
    if app:
        template_path = os.path.join(os.getcwd(), "apps", app, "templates", template_name)
    else:
        template_path = os.path.join(os.getcwd(), "templates", template_name)

    if not os.path.exists(template_path):
        return Response("Template not found", status="500 INTERNAL SERVER ERROR")
    
    with open(template_path, "r", encoding="utf-8") as f:
        content = f.read()

    for key, value in context.items():
        content = content.replace(f"{{{{ {key} }}}}", str(value))

    return Response(content)