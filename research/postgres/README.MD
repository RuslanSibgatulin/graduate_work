# Тестирование Postgres
Для тестирования был поднят инстанс PostgreSQL 13 в docker.
Эта СУБД использует следующие алгоритмы сжатия:
- LZ4 (Postgres 14)
- PGLZ 

## Запуск
1. Запустить инфраструктуру

    make start

2. Тестирование

    make full-test

## Запись 
Для тестирования скорости записи были произведены операции на добавление 1M документов в коллекцию профилей пользователей. Результат:

1M      - 295.49s
100k    - 33.92s
1k      - 3.97s

## Коллаборативная подборка фильмов (чтение)
Чтение производилось с агрегированием для формирования массива данных под задачи проекта.

Случайный выбор профиля пользователя с набором просмотренных фильмов и поиск по базе (1M ползьователей) аналогичных просмотров занимает
от 0.08 до 0.12 сек

Пример запроса для профиля с просмотрами (2928, 4334, 8875, 27075):

    SELECT user_id, array_agg(film_id) user_films FROM film_scores 
    WHERE user_id in (
        SELECT user_id FROM (
            SELECT user_id, (count(film_id)/4 :: float) as similarity FROM film_scores 
            WHERE film_id in (2928, 4334, 8875, 27075)
            GROUP BY user_id
            ORDER BY similarity DESC
            LIMIT 10
        ) as similar_users
    )
    AND film_id NOT IN (2928, 4334, 8875, 27075)
    GROUP BY user_id