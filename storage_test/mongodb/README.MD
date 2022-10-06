# Тестирование MongoDB
Для тестирования был поднят кластер MongoDB в docker на основе образа mongo:6.0 из 2 шардов по 3 реплики, 3 сервера конфигурации и 2 маршрутизатора.
При использовании стандартного движка хранения WiredTiger, используются следующие алгоритмы сжатия:
- zstd (MongoDB 4.2)
- zlib


## Запуск
1. Запустить инфраструктуру

    make start

2. Выполнить первоначальную настройку. Убедиться, что инициализация прошла успешно. При ошибке повторить команду
    
    make init

3. Тестирование

    make full-test

## Запись 
Для тестирования скорости записи была произведена операця на добавление 500k документов в коллекцию профилей пользователей. Их результат:

- 1k    - 1.90s
- 10к   - 21.15s
- 100к  - 187.39s

## Чтение 
Чтение производилось с агрегированием для формирования массива данных под задачи проекта.

### Коллаборативная подборка фильмов
Случайный выбор профиля пользователя с набором просмотренных фильмов и поиск по базе (500к документов) аналогичных просмотров занимает
от 1.9s до 0.73s

## Результат pytest
Тестирование было проведено с использованием библиотеки pytest в асинхронном режиме.  

    ========================================== test session starts ===============================================================
    platform linux -- Python 3.10.6, pytest-7.1.2, pluggy-1.0.0 -- graduate_work/venv/bin/python3
    cachedir: .pytest_cache
    rootdir: graduate_work/storage_test/mongodb/tests, configfile: pytest.ini
    plugins: Faker-14.1.0, asyncio-0.18.3
    asyncio: mode=auto
    collected 27 items                                                                                                                                    

    tests/views_test.py::test_insert_users_with_views[1000] PASSED                                                                                  [  3%]
    tests/views_test.py::test_insert_users_with_views[10000] PASSED                                                                                 [  7%]
    tests/views_test.py::test_insert_users_with_views[1000000] PASSED                                                                               [ 11%]
    tests/views_test.py::test_insert_users_with_views[1000001] PASSED                                                                               [ 14%]
    tests/views_test.py::test_insert_users_with_views[1000002] PASSED                                                                               [ 18%]
    tests/views_test.py::test_insert_users_with_views[1000003] PASSED                                                                               [ 22%]
    tests/views_test.py::test_insert_users_with_views[89000] PASSED                                                                                 [ 25%]
    tests/views_test.py::test_user_views_similarity[0] PASSED                                                                                       [ 29%]
    tests/views_test.py::test_user_views_similarity[1] PASSED                                                                                       [ 33%]
    tests/views_test.py::test_user_views_similarity[2] PASSED                                                                                       [ 37%]
    tests/views_test.py::test_user_views_similarity[3] PASSED                                                                                       [ 40%]
    tests/views_test.py::test_user_views_similarity[4] PASSED                                                                                       [ 44%]
    tests/views_test.py::test_user_views_similarity[5] PASSED                                                                                       [ 48%]
    tests/views_test.py::test_user_views_similarity[6] PASSED                                                                                       [ 51%]
    tests/views_test.py::test_user_views_similarity[7] PASSED                                                                                       [ 55%]
    tests/views_test.py::test_user_views_similarity[8] PASSED                                                                                       [ 59%]
    tests/views_test.py::test_user_views_similarity[9] PASSED                                                                                       [ 62%]
    tests/views_test.py::test_user_views_similarity[10] PASSED                                                                                      [ 66%]
    tests/views_test.py::test_user_views_similarity[11] PASSED                                                                                      [ 70%]
    tests/views_test.py::test_user_views_similarity[12] PASSED                                                                                      [ 74%]
    tests/views_test.py::test_user_views_similarity[13] PASSED                                                                                      [ 77%]
    tests/views_test.py::test_user_views_similarity[14] PASSED                                                                                      [ 81%]
    tests/views_test.py::test_user_views_similarity[15] PASSED                                                                                      [ 85%]
    tests/views_test.py::test_user_views_similarity[16] PASSED                                                                                      [ 88%]
    tests/views_test.py::test_user_views_similarity[17] PASSED                                                                                      [ 92%]
    tests/views_test.py::test_user_views_similarity[18] PASSED                                                                                      [ 96%]
    tests/views_test.py::test_user_views_similarity[19] PASSED                                                                                      [100%]

    ========================================== slowest durations ==================================================================
    187.39s call     views_test.py::test_insert_users_with_views[1000003]
    185.68s call     views_test.py::test_insert_users_with_views[1000001]
    185.55s call     views_test.py::test_insert_users_with_views[1000000]
    184.31s call     views_test.py::test_insert_users_with_views[1000002]
    168.57s call     views_test.py::test_insert_users_with_views[89000]
    21.15s call     views_test.py::test_insert_users_with_views[10000]
    1.90s call     views_test.py::test_insert_users_with_views[1000]
    0.78s call     views_test.py::test_user_views_similarity[13]
    0.78s call     views_test.py::test_user_views_similarity[8]
    0.78s call     views_test.py::test_user_views_similarity[6]
    0.76s call     views_test.py::test_user_views_similarity[7]
    0.76s call     views_test.py::test_user_views_similarity[10]
    0.76s call     views_test.py::test_user_views_similarity[1]
    0.76s call     views_test.py::test_user_views_similarity[3]
    0.76s call     views_test.py::test_user_views_similarity[11]
    0.76s call     views_test.py::test_user_views_similarity[16]
    0.75s call     views_test.py::test_user_views_similarity[2]
    0.75s call     views_test.py::test_user_views_similarity[14]
    0.75s call     views_test.py::test_user_views_similarity[4]
    0.75s call     views_test.py::test_user_views_similarity[15]
    0.75s call     views_test.py::test_user_views_similarity[12]
    0.75s call     views_test.py::test_user_views_similarity[9]
    0.75s call     views_test.py::test_user_views_similarity[19]
    0.75s call     views_test.py::test_user_views_similarity[5]
    0.75s call     views_test.py::test_user_views_similarity[17]
    0.75s call     views_test.py::test_user_views_similarity[18]
    0.73s call     views_test.py::test_user_views_similarity[0]

    (51 durations < 0.005s hidden.  Use -vv to show these durations.)
    ========================================== 27 passed in 951.12s (0:15:51) ============================================================