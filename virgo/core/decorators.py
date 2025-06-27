from virgo.core.auth import get_user
from virgo.core.response import redirect
from settings import LOGIN_ROUTE, FORBIDDEN_REDIRECT_ROUTE

def login_required(UserModel):
    def decorator(view_func):
        def wrapped(request, *args, **kwargs):
            user = get_user(request, UserModel)
            if not user:
                return redirect(LOGIN_ROUTE)
            request.user = user  # Attach user to request
            return view_func(request, *args, **kwargs)
        return wrapped
    return decorator

def role_required(role):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            user = getattr(request, "user", None)
            if not user or getattr(user, "role", None) != role:
                return redirect(FORBIDDEN_REDIRECT_ROUTE)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

