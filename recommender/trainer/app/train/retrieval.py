from functools import partial

import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
import tensorflow_recommenders as tfrs
from models import retrieval
from train.utils import init_training


def train_retrieval(
    *,
    views_input_dir: str,
    model_output_dir: str,
    max_views_length: int,
    recs_length: int = 50,
):
    train, test, cp_callback = init_training(views_input_dir, model_output_dir)

    movies, unique_movie_ids = _load_movies()

    query_model = retrieval.QueryModel(unique_movie_ids)
    candidate_model = retrieval.CandidateModel(unique_movie_ids)

    metric = tfrs.metrics.FactorizedTopK(
        candidates=movies.batch(128).map(candidate_model)
    )

    model = retrieval.Model(query_model, candidate_model, metrics=metric)
    model.compile(optimizer=tf.keras.optimizers.Adagrad(learning_rate=0.1))

    train_ds, test_ds = _prepare_datasets(train, test, max_views_length)

    cached_train = train_ds.shuffle(10_000).batch(15_000).cache()
    cached_test = test_ds.batch(2_000).cache()

    model.fit(cached_train, epochs=3, callbacks=[cp_callback])
    print(model.evaluate(cached_test, return_dict=True))

    index = tfrs.layers.factorized_top_k.BruteForce(model.query_model, k=recs_length)
    index.index_from_dataset(
        tf.data.Dataset.zip(
            (movies.batch(100), movies.batch(100).map(model.candidate_model))
        )
    )

    index(tf.constant([["0" for _ in range(max_views_length)]]))

    tf.saved_model.save(index, model_output_dir)


def _prepare_datasets(train, test, max_views_length: int):
    features = {
        "movie_id": tf.io.FixedLenFeature(
            max_views_length,
            tf.string,
            default_value=np.repeat("0", max_views_length),
        ),
        "label_movie_id": tf.io.FixedLenFeature([1], tf.string, default_value="0"),
    }

    parse_example = partial(tf.io.parse_single_example, features=features)

    train_ds = train.map(parse_example)
    test_ds = test.map(parse_example)

    return train_ds, test_ds


def _load_movies() -> tuple:
    movies = tfds.load("movielens/1m-movies", split="train")
    movies = movies.map(lambda x: x["movie_id"])
    movie_ids = movies.batch(1_000)
    unique_movie_ids = np.unique(np.concatenate(list(movie_ids)))
    return movies, unique_movie_ids
