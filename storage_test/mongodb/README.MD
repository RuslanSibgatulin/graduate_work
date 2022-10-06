# Тестирование MongoDB
Для тестирования был поднят кластер MongoDB в docker на основе образа mongo:6.0 из 2 шардов по 3 реплики, 3 сервера конфигурации и 2 маршрутизатора.
При использовании стандартного движка хранения WiredTiger, используются следующие алгоритмы сжатия:
- zstd (MongoDB 4.2)
- zlib


## Запуск
1. Запустить инфраструктуру

    make start

2. Выполнить первоначальную настройку
    
    make db-init

3. Тестирование

    make full-test

## Запись 
Для тестирования скорости записи были произведены 3 последовательных операции на добавление 10k, 100k, 1M документов в коллекцию лайков. Их результат:
- 10к   - 17.56s
- 100к  - 154.23s
- 1М    - 1616.42s = 26min 56s

## Чтение 
Чтение производилось с агрегированием для формирования массива данных под задачи спринта.

### Топ рейтинговых фильмов
Рейтинг вычислялся на основе оценок пользователей для величины более 5.
Результат выборки:
- Топ-10   - 1.52s
- Топ-100  - 1.46s
- Топ-1000 - 1.72s

### Рейтинг одного фильма
Случайный выбор фильма из коллекции и его оценка заняли 0.23s.
В оценку входят операции агрегирования для получения массива данных:
- Количество лайков
- Количество дизлайков
- Средний рейтинг по всем оценкам
- Количество оценок для фильма

## Результат pytest
Тестирование было проведено с использованием библиотеки pytest в асинхронном режиме.  

    ================================================================ test session starts ============================================
    platform linux -- Python 3.10.4, pytest-7.1.2, pluggy-1.0.0
    cachedir: .pytest_cache
    rootdir: storage_test/Mongo/tests, configfile: pytest.ini
    plugins: anyio-3.6.1, Faker-14.1.0, asyncio-0.18.3
    asyncio: mode=auto
    collected 12 items                                                                                                                                   

    tests/mongo_test.py::test_insert_movies_likes[10000] Fill likes collection. 10000 docs. 
    PASSED  Inserted docs | 10000 | 100%
    tests/mongo_test.py::test_insert_movies_likes[100000] Fill likes collection. 100000 docs. 
    PASSED  Inserted docs | 100000 | 100%
    tests/mongo_test.py::test_insert_movies_likes[1000000] Fill likes collection. 1000000 docs. 
    PASSED  Inserted docs | 1000000 | 100%
    tests/mongo_test.py::test_insert_review_likes PASSED
    tests/mongo_test.py::test_insert_bookmarks[100] PASSED
    tests/mongo_test.py::test_insert_bookmarks[1000] PASSED
    tests/mongo_test.py::test_insert_bookmarks[10000] PASSED
    tests/mongo_test.py::test_top_movies[10] PASSED
    tests/mongo_test.py::test_top_movies[100] PASSED
    tests/mongo_test.py::test_top_movies[1000] PASSED
    tests/mongo_test.py::test_film_ratings PASSED
    tests/mongo_test.py::test_user_bookmarks PASSED

    ================================================================= slowest durations =============================================
    1616.42s call     mongo_test.py::test_insert_movies_likes[1000000]
    154.23s call     mongo_test.py::test_insert_movies_likes[100000]
    60.07s call     mongo_test.py::test_insert_review_likes
    39.88s call     mongo_test.py::test_insert_bookmarks[10000]
    17.56s call     mongo_test.py::test_insert_movies_likes[10000]
    3.79s call     mongo_test.py::test_insert_bookmarks[1000]
    1.72s call     mongo_test.py::test_top_movies[1000]
    1.52s call     mongo_test.py::test_top_movies[10]
    1.46s call     mongo_test.py::test_top_movies[100]
    0.40s call     mongo_test.py::test_insert_bookmarks[100]
    0.23s call     mongo_test.py::test_film_ratings
    0.00s call     mongo_test.py::test_user_bookmarks
    ========================================================== 12 passed in 1899.19s (0:31:39) ======================================
