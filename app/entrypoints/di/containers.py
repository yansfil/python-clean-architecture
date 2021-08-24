from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
