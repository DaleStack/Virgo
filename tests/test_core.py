from .user import User
from virgo.core.session import get_session

def test_user_registration_and_authentication():
    username = "testuser"
    password = "testpassword"

    user = User.register(username=username, password=password)
    assert user.username == username

    # Test Login
    fake_request = type('Request', (), {"environ": {}})
    response = User.authenticate(fake_request, username=username, password=password)

    assert response.status.startswith("302")
    cookies = dict(response.headers)
    assert "Set-Cookie" in cookies
    session_id = cookies["Set-Cookie"].split("=")[1].split(";")[0]
    session = get_session(session_id)
    assert session["user_id"] == user.id