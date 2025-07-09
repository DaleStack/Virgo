from sqlalchemy import Column, Integer, String
from virgo.core.database import Base
from virgo.core.mixins import BaseModelMixin
from virgo.core.session import create_session, get_session, destroy_session
from virgo.core.response import Response, redirect
from settings import LOGIN_REDIRECT_ROUTE, LOGOUT_REDIRECT_ROUTE, ROLE_ROUTES
import bcrypt


class UserAlreadyExists(Exception):
    pass

class UserModel(Base, BaseModelMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)


    def check_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode(), self.password.encode())

    @staticmethod
    def hash_password(raw_password):
        hashed = bcrypt.hashpw(raw_password.encode(), bcrypt.gensalt())
        return hashed.decode()  # store as string in DB

    @classmethod
    def authenticate(cls, request, username, password):
        user = cls.first_by(username=username)
        if user and user.check_password(password):
            session_id = create_session(user.id)

            redirect_route = ROLE_ROUTES.get(getattr(user, "role", None), LOGIN_REDIRECT_ROUTE)

            response = redirect(redirect_route)
            response.headers.append(("Set-Cookie", f"session_id={session_id}; Path=/; HttpOnly"))
            return response
        return Response("Invalid credentials", status="401 Unauthorized")

    @classmethod
    def register(cls, username, password):
        if cls.first_by(username=username):
            raise UserAlreadyExists("Username already taken")

        hashed = cls.hash_password(password)
        return cls.create(username=username, password=hashed)
    
    def logout(self, request):
        # Extract session_id from cookie
        cookie = request.environ.get("HTTP_COOKIE", "")
        session_id = None

        for part in cookie.split(";"):
            if part.strip().startswith("session_id="):
                session_id = part.strip().split("=")[1]
                break

        if session_id:
            destroy_session(session_id)

        # Clear cookie + redirect
        response = redirect(LOGOUT_REDIRECT_ROUTE)
        response.headers.append((
            "Set-Cookie",
            "session_id=; Path=/; Max-Age=0; HttpOnly"
        ))
        return response
    
def get_user(request, UserModel):
    cookie = request.environ.get("HTTP_COOKIE", "")
    session_id = None

    for part in cookie.split(";"):
        if part.strip().startswith("session_id="):
            session_id = part.strip().split("=")[1]
            break

    if not session_id:
        return None

    session_data = get_session(session_id)
    if not session_data:
        return None

    user_id = session_data.get("user_id")
    return UserModel.get(user_id)
