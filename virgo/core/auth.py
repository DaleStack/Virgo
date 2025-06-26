from sqlalchemy import Column, Integer, String
from virgo.core.database import Base
from virgo.core.mixins import BaseModelMixin
from virgo.core.session import create_session
from virgo.core.response import Response, redirect
from settings import LOGIN_REDIRECT_ROUTE
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
            response = redirect(LOGIN_REDIRECT_ROUTE)
            response.headers.append(("Set-Cookie", f"session_id={session_id}; Path=/; HttpOnly"))
            return response
        return Response("Invalid credentials", status="401 Unauthorized")

    @classmethod
    def register(cls, username, password):
        if cls.first_by(username=username):
            raise UserAlreadyExists("Username already taken")

        hashed = cls.hash_password(password)
        return cls.create(username=username, password=hashed)
