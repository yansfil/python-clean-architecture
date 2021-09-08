from typing import Callable, Dict, List, Type

from app.domains.events import DeleteUserPosts, Event, SendEmail, SendSlack
from app.services.handlers import delete_post, send_email, send_slack


def handle_event(event: Event):
    handlers = EVENT_HANDLERS[type(event)]
    for handler in handlers:
        handler(event)


EVENT_HANDLERS: Dict[Type[Event], List[Callable]] = {
    SendEmail: [send_email],
    SendSlack: [send_slack],
    DeleteUserPosts: [delete_post],  # 엄밀히는 Command
}
