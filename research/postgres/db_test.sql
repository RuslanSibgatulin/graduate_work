-- Active: 1663267042134@@127.0.0.1@5432
DROP TABLE film_scores;

CREATE TABLE IF NOT EXISTS film_scores (
    user_id uuid NOT NULL,
    film_id int NOT NULL,
    score int,
    created timestamp with time zone,
    CONSTRAINT pk_user_film PRIMARY KEY ( user_id, film_id)
); 