from sqlalchemy.orm import Session

from app.domains.user import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User):
        self.session.add(user)

    def find_one_by_id(self, user_id: str) -> User:
        return self.session.query(User).filter_by(user_id=user_id).first()

    def find_one(self, user_id: str, password: str) -> User:
        return (
            self.session.query(User)
            .filter_by(user_id=user_id, password=password)
            .first()
        )
