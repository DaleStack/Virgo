import uuid

SESSION_STORE = {}

def create_session(user_id):
    session_id = str(uuid.uuid4())
    SESSION_STORE[session_id] = {"user_id": user_id}
    return session_id

def get_session(session_id):
    return SESSION_STORE.get(session_id)

def destroy_session(session_id):
    SESSION_STORE.pop(session_id, None)
