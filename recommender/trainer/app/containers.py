import collect
from dependency_injector import containers, providers
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from train import ranking, retrieval


class Collect(containers.DeclarativeContainer):

    config = providers.Configuration()

    client = providers.Singleton(
        MongoClient,
        host=config.mongo.host,
        port=config.mongo.port,
    )

    db = providers.Factory(Database, client=client, name=config.mongo.db_name)

    profiles_collection = providers.Factory(
        Collection, database=db, name=config.mongo.profiles_collection
    )

    mongo_loader = providers.Factory(collect.MongoLoader, profiles_collection)

    movies_api_loader = providers.Factory(
        collect.MoviesApiLoader,
        host=config.movies_api.host,
        port=config.movies_api.port,
    )

    ratings_writer = providers.Factory(
        collect.ProtoWriter,
        output_dir=config.ratings_output_dir,
        train_filename="train.tfrecord",
        test_filename="test.tfrecord",
    )

    views_writer = providers.Factory(
        collect.ProtoWriter,
        output_dir=config.views_output_dir,
        train_filename="train.tfrecord",
        test_filename="test.tfrecord",
    )

    movies_writer = providers.Factory(
        collect.MoviesProtoWriter,
        output_dir=config.movies_output_dir,
        filename="movies.tfrecord",
    )

    collectors = providers.Dict(
        movies=providers.Factory(
            collect.Collector,
            loader=movies_api_loader,
            transformer=providers.Factory(collect.MoviesTransformer),
            writer=movies_writer,
        ),
        ratings=providers.Factory(
            collect.Collector,
            loader=mongo_loader,
            transformer=providers.Factory(collect.RatingsTransformer),
            writer=ratings_writer,
        ),
        views=providers.Factory(
            collect.Collector,
            loader=mongo_loader,
            transformer=providers.Factory(
                collect.ViewsTransformer, max_views_length=config.max_views_length
            ),
            writer=views_writer,
        ),
    )


class Train(containers.DeclarativeContainer):

    config = providers.Configuration()

    retrieval = providers.Callable(
        retrieval.train_retrieval,
        movies_input_dir=config.movies_input_dir,
        views_input_dir=config.views_input_dir,
        model_output_dir=config.retrieval_output_dir,
        max_views_length=config.max_views_length,
    )

    ranking = providers.Callable(
        ranking.train_ranking,
        ratings_input_dir=config.ratings_input_dir,
        model_output_dir=config.ranking_output_dir,
    )


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    wiring_config = containers.WiringConfiguration(modules=["handlers"])

    collect = providers.Container(Collect, config=config.collect)

    train = providers.Container(Train, config=config.train)
