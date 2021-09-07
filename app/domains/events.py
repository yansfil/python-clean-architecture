from dataclasses import dataclass


@dataclass
class Event:
    ...


@dataclass
class SendEmail(Event):
    msg: str


@dataclass
class DeleteUserPosts(Event):
    user_id: int
