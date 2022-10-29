import logging
import os
import random
import typing as tp
from dataclasses import dataclass


import tensorflow as tf
import pymongo


logger = logging.getLogger(__name__)


@dataclass(slots=True)
class MovieInfo:
    movie_id: str
    timestamp: int


@dataclass(slots=True)
class RatingInfo:
    user_id: str
    movie_id: str
    rating: int


def collect(
    loader: tp.Callable[[], tp.Generator],
    writer: tp.Callable[[], tp.Generator],
    transformer: tp.Callable[[tp.Any], tp.Iterable],
) -> None:
    loader, writer = loader(), writer()

    n_objects = next(loader)
    progress_bar = tf.keras.utils.Progbar(n_objects)

    writer.send(None)

    for objs in loader:
        for obj in objs:
            transformed_objs = next(transformer(obj))
            writer.send(transformed_objs)
            progress_bar.add(1)

    try:
        writer.send(None)
    except StopIteration as e:
        print(e.value)


class Collector:
    def __init__(
        self,
        loader: tp.Callable[[], tp.Generator],
        writer: tp.Callable[[], tp.Generator],
        transformer: tp.Callable[[tp.Any], tp.Iterable],
    ):
        self.loader = loader()
        self.writer = writer()
        self.transformer = transformer

    def __call__(self):
        n_objects = next(self.loader)
        progress_bar = tf.keras.utils.Progbar(n_objects)

        self.writer.send(None)

        for objs in self.loader:
            for obj in objs:
                transformed_objs = next(self.transformer(obj))
                self.writer.send(transformed_objs)
                progress_bar.add(1)

        try:
            self.writer.send(None)
        except StopIteration as e:
            print(e.value)


class MongoLoader:
    def __init__(self, collection):
        self.collection = collection

    def __call__(self):
        n_objects = self.collection.count_documents({})
        yield n_objects

        batch = []

        for obj in self.collection.find():
            batch.append(obj)
            if len(batch) == 100:
                random.shuffle(batch)
                yield batch
                batch = []

        if batch:
            yield batch


class ProtoWriter:
    def __init__(
        self,
        output_dir: str,
        train_filename: str,
        test_filename: str,
        train_size: int = 9,
    ):
        if not tf.io.gfile.exists(output_dir):
            tf.io.gfile.makedirs(output_dir)

        self.train_filename = os.path.join(output_dir, train_filename)
        self.test_filename = os.path.join(output_dir, test_filename)

        self.train_size = train_size

    def __call__(self) -> tp.Generator[None, tp.Iterable[tf.train.Example], int]:
        with tf.io.TFRecordWriter(
            self.train_filename
        ) as train_writer, tf.io.TFRecordWriter(self.test_filename) as test_writer:
            n = 0
            to_train = 0
            to_test = 0

            examples = yield

            while examples := (yield):
                for example in examples:
                    serialized_example = example.SerializeToString()

                    if (n + 1) % (self.train_size + 1) == 0:
                        test_writer.write(serialized_example)
                        to_test += 1
                    else:
                        train_writer.write(serialized_example)
                        to_train += 1

                    n += 1

            return to_train / n, to_test / n


class RatingsTransformer:
    def __call__(self, obj):
        user_id = obj["user_id"]

        examples = []

        for movie_id, rating in obj["ratings"].items():
            feature = {
                "user_id": tf.train.Feature(
                    bytes_list=tf.train.BytesList(value=[user_id.encode()])
                ),
                "movie_id": tf.train.Feature(
                    bytes_list=tf.train.BytesList(value=[movie_id.encode()])
                ),
                "rating": tf.train.Feature(
                    int64_list=tf.train.Int64List(value=[rating])
                ),
            }
            examples.append(
                tf.train.Example(features=tf.train.Features(feature=feature))
            )

        yield examples


class ViewsTransformer:
    def __init__(self, max_views_length: int):
        self.max_views_length = max_views_length

    def __call__(self, obj):
        views = [
            MovieInfo(movie_id=movie_id, timestamp=ts)
            for movie_id, ts in sorted(obj["views"].items(), key=lambda view: view[1])
        ]

        yield self._generate_examples_from_views(views)

    def _generate_examples_from_views(
        self, views: list[MovieInfo]
    ) -> tp.Generator[list[tf.train.Example], None, None]:
        examples = []

        for label_idx in range(1, len(views)):
            start_idx = max(0, label_idx - self.max_views_length)
            context = views[start_idx:label_idx]

            while len(context) < self.max_views_length:
                context.append(MovieInfo(movie_id="0", timestamp=0))

            label_movie_id = [views[label_idx].movie_id.encode()]
            movie_id = [movie.movie_id.encode() for movie in context]

            feature = {
                "movie_id": tf.train.Feature(
                    bytes_list=tf.train.BytesList(value=movie_id)
                ),
                "label_movie_id": tf.train.Feature(
                    bytes_list=tf.train.BytesList(value=label_movie_id)
                ),
            }
            example = tf.train.Example(features=tf.train.Features(feature=feature))
            examples.append(example)

        return examples
