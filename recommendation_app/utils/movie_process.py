from models.movies_list import GerneMovies


class MovieProcessor:
    MOVIES_MAX: int = 5

    @classmethod
    def get_genre_movies(cls, movies_list: list[GerneMovies]) -> list[GerneMovies]:
        all_movies = set()
        for movie_obj in movies_list:
            movies = movie_obj.movies
            movie_obj.movies = []
            for movie in movies:
                if movie in all_movies:
                    continue
                all_movies.add(movie)
                movie_obj.movies.append(movie)
                if len(movie_obj.movies) == cls.MOVIES_MAX:
                    break
        return movies_list



