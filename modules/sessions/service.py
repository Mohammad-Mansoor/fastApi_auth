from .repository import SessionRepository


class SessionService:
    def __init__(self):
        self.sessionRepo = SessionRepository()