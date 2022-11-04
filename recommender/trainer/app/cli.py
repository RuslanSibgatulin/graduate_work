import argparse

import handlers

root = argparse.ArgumentParser(prog="Trainer")

subparsers = root.add_subparsers(
    title="Commands", dest="command", help="commands", required=True
)

collect = subparsers.add_parser("collect", help="Collect data for future training")
collect.add_argument(
    "data",
    nargs="+",
    help="Type of data to be collected. One of: ratings, movies, views",
)
collect.set_defaults(handler=handlers.collect)

train = subparsers.add_parser("train", help="Train a model")
train.add_argument(
    "model",
    nargs="+",
    help="Type of model to be trained. One of: ranking, retrieval",
)
train.set_defaults(handler=handlers.train)
