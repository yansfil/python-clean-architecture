from sqlalchemy.orm import Session

from app.domains.user import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User):
        self.session.add(user)
