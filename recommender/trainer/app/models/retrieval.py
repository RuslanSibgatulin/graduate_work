import typing as tp

import tensorflow as tf
import tensorflow_recommenders as tfrs


class QueryModel(tf.keras.Sequential):
    def __init__(self, vocabulary: tp.Any):
        layers = [
            tf.keras.layers.StringLookup(vocabulary=vocabulary, mask_token=None),
            tf.keras.layers.Embedding(len(vocabulary) + 1, 32),
            tf.keras.layers.GRU(32),
        ]

        super().__init__(layers)


class CandidateModel(tf.keras.Sequential):
    def __init__(self, vocabulary: tp.Any):
        layers = [
            tf.keras.layers.StringLookup(vocabulary=vocabulary, mask_token=None),
            tf.keras.layers.Embedding(len(vocabulary) + 1, 32),
        ]

        super().__init__(layers)


class Model(tfrs.Model):
    def __init__(
        self, query_model: tf.keras.Model, candidate_model: tf.keras.Model, **kwargs
    ):
        super().__init__()

        self.query_model = query_model
        self.candidate_model = candidate_model
        self.task = tfrs.tasks.Retrieval(**kwargs)

    def compute_loss(self, features: dict[str, tf.Tensor], training=False):
        views = features["movie_id"]
        label = features["label_movie_id"]

        query_embedding = self.query_model(views)
        candidate_embedding = self.candidate_model(label)

        return self.task(
            query_embedding, candidate_embedding, compute_metrics=not training
        )
