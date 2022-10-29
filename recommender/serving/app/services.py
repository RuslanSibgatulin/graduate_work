import tensorflow as tf

from dto import MovieContextInfo


class RecommenderService:
    def __init__(self, retrieval_model: tf.keras.Model, ranking_model: tf.keras.Model):
        self.retrieval = retrieval_model
        self.ranking = ranking_model

    def recommend(self, user_id: str, views: list[MovieContextInfo]) -> list[str]:
        views_ids = [view.movie_id for view in views]
        _, movies_tensor = self.retrieval(tf.constant([views_ids]))
        recs = movies_tensor.numpy()[0]
        narrowed_recs = self.narrow_recommendations(user_id, recs)
        return [movie_id.decode() for movie_id in narrowed_recs]

    def narrow_recommendations(
        self, user_id: str, recs: list[str], *, return_size: int = 5
    ) -> list[str]:
        sorted_recs = sorted(
            recs, key=lambda movie_id: self.rate_movie(user_id, movie_id)
        )
        return sorted_recs[return_size:]

    def rate_movie(self, user_id: str, movie_id: str) -> float:
        return self.ranking(
            {"user_id": tf.constant([user_id]), "movie_id": tf.constant([movie_id])}
        ).numpy()[0][0]