import typing as tp

import tensorflow as tf
import tensorflow_recommenders as tfrs


class UserModel(tf.keras.Sequential):
    def __init__(self, vocalulary: tp.Any, embedding_dim: int):
        layers = [
            tf.keras.layers.StringLookup(vocabulary=vocalulary, mask_token=None),
            tf.keras.layers.Embedding(len(vocalulary) + 1, embedding_dim),
        ]

        super().__init__(layers)


class MovieModel(tf.keras.Sequential):
    def __init__(self, vocalulary: tp.Any, embedding_dim: int):
        layers = [
            tf.keras.layers.StringLookup(vocabulary=vocalulary, mask_token=None),
            tf.keras.layers.Embedding(len(vocalulary) + 1, embedding_dim),
        ]

        super().__init__(layers)


class RankingModel(tf.keras.Model):
    def __init__(
        self, user_model: tf.keras.Model, movie_model: tf.keras.Model, units: list[int]
    ):
        super().__init__()

        self.user_model = user_model
        self.movie_model = movie_model

        assert len(units) == 2

        self.ratings = tf.keras.Sequential(
            [
                tf.keras.layers.Dense(units[0], activation="relu"),
                tf.keras.layers.Dense(units[1], activation="relu"),
                tf.keras.layers.Dense(1),
            ]
        )

    def call(self, features: dict[str, tf.Tensor]) -> tf.Tensor:
        user_id = features["user_id"]
        movie_id = features["movie_id"]

        user_embedding = self.user_model(user_id)
        movie_embedding = self.movie_model(movie_id)

        return self.ratings(tf.concat([user_embedding, movie_embedding], axis=1))


class Model(tfrs.models.Model):
    def __init__(self, ranking_model: tf.keras.Model, **kwargs):
        super().__init__()

        self.ranking_model = ranking_model
        self.task: tf.keras.layers.Layer = tfrs.tasks.Ranking(**kwargs)

    def call(self, features: dict[str, tf.Tensor]) -> tf.Tensor:
        return self.ranking_model(features)

    def compute_loss(self, features: dict[str, tf.Tensor], training=False) -> tf.Tensor:
        labels = features.pop("rating")

        rating_predictions = self(features)

        return self.task(
            labels=labels, predictions=rating_predictions, compute_metrics=not training
        )
