import os
from functools import partial

import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
import tensorflow_recommenders as tfrs

from models import ranking
from train.utils import init_training


def train_ranking(*, ratings_input_dir: str, model_output_dir: str):
    train, test, cp_callback = init_training(ratings_input_dir, model_output_dir)

    train_ds, test_ds = _prepare_datasets(train, test)

    movie_ids = (
        train_ds.concatenate(test_ds).batch(1_000_000).map(lambda x: x["movie_id"])
    )
    user_ids = (
        train_ds.concatenate(test_ds).batch(1_000_000).map(lambda x: x["user_id"])
    )

    unique_movie_ids = np.unique(np.concatenate(list(movie_ids)))
    unique_user_ids = np.unique(np.concatenate(list(user_ids)))

    user_model = ranking.UserModel(unique_user_ids, 32)
    movie_model = ranking.MovieModel(unique_movie_ids, 32)
    ranking_model = ranking.RankingModel(user_model, movie_model, [256, 64])

    loss = tf.keras.losses.MeanSquaredError()
    metrics = [
        tf.keras.metrics.RootMeanSquaredError(),
        tf.keras.metrics.MeanAbsoluteError(),
    ]

    model = ranking.Model(ranking_model, loss=loss, metrics=metrics)
    model.compile(optimizer=tf.keras.optimizers.Adagrad(learning_rate=0.1))

    cached_train = train_ds.shuffle(100_000).batch(10_000).cache()
    cached_test = test_ds.batch(5_000).cache()

    model.fit(cached_train, epochs=10, callbacks=[cp_callback])

    print(model.evaluate(cached_train, return_dict=True))

    model({"user_id": tf.constant(["0"]), "movie_id": tf.constant(["0"])})

    tf.saved_model.save(model, model_output_dir)


def _prepare_datasets(train, test):
    features = {
        "movie_id": tf.io.FixedLenFeature([1], tf.string, default_value="0"),
        "rating": tf.io.FixedLenFeature([1], tf.int64, default_value=0),
        "user_id": tf.io.FixedLenFeature([1], tf.string, default_value="0"),
    }

    parse_example = partial(tf.io.parse_single_example, features=features)

    def _convert_to_singles(example: tf.train.Example):
        return {
            "movie_id": example["movie_id"][0],
            "user_id": example["user_id"][0],
            "rating": float(example["rating"][0]),
        }

    train_ds = train.map(parse_example).map(_convert_to_singles)
    test_ds = test.map(parse_example).map(_convert_to_singles)

    return train_ds, test_ds
