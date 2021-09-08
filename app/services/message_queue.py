from __future__ import annotations

import asyncio

from app.domains.events import Event

message_queue: asyncio.Queue[Event] = asyncio.Queue()
