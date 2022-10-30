from dependency_injector import containers, providers
from services import RecommenderService
from utils import load_model


class Models(containers.DeclarativeContainer):
    config = providers.Configuration()

    retrieval = providers.Singleton(load_model, config.retrieval_path)

    ranking = providers.Singleton(load_model, config.ranking_path)


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    models = providers.Container(Models, config=config.models)

    recommender = providers.Factory(
        RecommenderService,
        retrieval_model=models.retrieval,
        ranking_model=models.ranking,
    )
