# Обучение модели


Скопировать файл коллекции в контейнер

    docker cp profiles.json mongodb:/data/

Войти в контейнер

    docker exec -it mongodb bash

Импортировать файл

    mongoimport --db=recom_db --collection=profiles --file=/data/profiles.json --jsonArray

Запустить переобучение из каталога проекта graduate_work

    make train
