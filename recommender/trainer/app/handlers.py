import typing as tp

from dependency_injector.containers import Container
from dependency_injector.wiring import Provide, inject

from collect import collect as collector
from containers import Container


@inject
def collect(
    args,
    collector_factory: dict[str, tp.Callable] = Provide[Container.collect.collectors],
):
    collector = collector_factory.get(args.data)
    if not collector:
        raise

    collector()


@inject
def train(args, trainers: Container = Provide[Container.train]):
    if args.model == "retrieval":
        trainers.retrieval()
    elif args.model == "ranking":
        trainers.ranking()
    else:
        raise
