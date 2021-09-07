from __future__ import annotations

import asyncio
from typing import Callable, Dict, List, Type

from app.domains.events import DeleteUserPosts, Event, SendEmail
from app.services.handlers import delete_post, send_email

message_queue: asyncio.Queue[Event] = asyncio.Queue()


def handle_event(event: Event):
    handlers = EVENT_HANDLERS[type(event)]
    for handler in handlers:
        handler(event)


EVENT_HANDLERS: Dict[Type[Event], List[Callable]] = {
    SendEmail: [send_email],
    DeleteUserPosts: [delete_post],
}
