import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from virgo.core.response import Response

# Create the environment with support for app-specific templates
def get_jinja_env(app=None):
    if app:
        template_dir = os.path.join(os.getcwd(), "apps", app, "templates")
    else:
        template_dir = os.path.join(os.getcwd(), "templates")

    return Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )

def render(template_name, context=None, app=None):
    context = context or {}
    env = get_jinja_env(app)

    try:
        template = env.get_template(template_name)
        html = template.render(**context)
        return Response(html)
    except Exception as e:
        return Response(f"Template error: {str(e)}", status="500 INTERNAL SERVER ERROR")
