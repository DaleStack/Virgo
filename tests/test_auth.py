import pytest
from virgo.core.auth import UserModel, UserAlreadyExists
from virgo.core.database import Base, engine, SessionLocal
from types import SimpleNamespace
from virgo.core.response import Response

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Create tables before each test
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables after each test
    Base.metadata.drop_all(bind=engine)
    SessionLocal.remove()  # Clear any lingering sessions

def test_user_register_and_duplicate():
    user = UserModel.register(username="keidev", password="supersecret")
    assert user.username == "keidev"

    with pytest.raises(UserAlreadyExists):
        UserModel.register(username="keidev", password="hacked")

def mock_request():
    """Simulates a minimal request object with cookie access."""
    return SimpleNamespace(environ={"HTTP_COOKIE": ""})

def test_successful_login():
    # First register a user
    user = UserModel.register(username="keilogger", password="pass123")

    # Login with the registered user
    response = UserModel.authenticate(mock_request(), "keilogger", "pass123")

    assert isinstance(response, Response)
    assert response.status == "302 Found"  # Redirect expected
    assert any("session_id=" in h[1] for h in response.headers)

def test_failed_login():
    # Login with a non-existent user
    UserModel.register(username="ghost", password="invisible")

    response = UserModel.authenticate(mock_request(), "ghost", "wrongpass")

    assert isinstance(response, Response)
    assert response.status == "401 Unauthorized"
    assert "Invalid credentials" in response.body.decode()