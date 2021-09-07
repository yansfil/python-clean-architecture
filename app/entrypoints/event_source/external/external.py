from enum import Enum

from app.domains.events import Event
from app.entrypoints.event_source.external.publisher import Publisher


class Upstream(Enum):
    GCP_PUBSUB = "GCP_PUBSUB"
    KAFKA = "KAFKA"
    ...


class ExternalEventEmitter:
    def __init__(self, publisher: Publisher):
        self.publisher = publisher

    async def emit(self, event: Event):
        self.publisher.publish(event)
