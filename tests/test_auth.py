import pytest
from virgo.core.auth import UserModel, UserAlreadyExists
from virgo.core.database import Base, engine, SessionLocal
from virgo.core.session import create_session, get_session
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

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_logout_clears_session_and_cookie():
    # Register and simulate login
    user = UserModel.register("logoutuser", "topsecret")
    session_id = create_session(user.id)

    # Create a mock request with session_id cookie
    mock_env = {"HTTP_COOKIE": f"session_id={session_id}"}
    mock_request = SimpleNamespace(environ=mock_env)

    # Call logout
    response = user.logout(mock_request)

    # Cookie should be cleared in headers
    cleared_cookie_header = any(
        "session_id=;" in h[1] and "Max-Age=0" in h[1]
        for h in response.headers
    )
    assert cleared_cookie_header, "Session cookie was not cleared"

    # Session should no longer exist
    assert get_session(session_id) is None, "Session was not destroyed"

    # Confirm redirection
    assert response.status == "302 Found"