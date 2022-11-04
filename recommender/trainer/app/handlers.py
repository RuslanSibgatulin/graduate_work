import typing as tp

from containers import Container
from dependency_injector.wiring import Provide, inject


@inject
def collect(
    args,
    collector_factory: dict[str, tp.Callable] = Provide[Container.collect.collectors],
):
    for data in args.data:
        collector = collector_factory.get(data)
        if not collector:
            raise

        collector()


@inject
def train(args, trainers: Container = Provide[Container.train]):
    for model in args.model:
        if model == "retrieval":
            trainers.retrieval()
        elif model == "ranking":
            trainers.ranking()
        else:
            raise
