import abc

from app.domains.events import Event


class Publisher(abc.ABC):
    def __init__(self, config):
        self.config = config

    @abc.abstractmethod
    def publish(self, event: Event):
        ...


class PubSubPublisher(Publisher):
    def publish(self, event: Event):
        print("publish to pubsub")
        ...


class KafkaPublisher(Publisher):
    def publish(self, event: Event):
        print("publish to kafka")
        ...
