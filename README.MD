# Дипломная работа: Рекомендательная система
[![Generic badge](https://img.shields.io/badge/Changelog-<COLOR>.svg)](./CHANGELOG.md)
[![Generic badge](https://img.shields.io/badge/Our-Team-<COLOR>.svg)](#команда)


Этот сервис будет предлагать фильмы для пользователя и будет использовать 2 подхода в рекомендациях:
- На основе контента из описания к фильмам
- Коллаборативная фильтрация на основе просмотров другими пользователями 


[Ссылка на приватный репозиторий с командной работой.](https://github.com/RuslanSibgatulin/graduate_work)


## Используемые технологии
- Код приложения на Python + fastapi.
- Транзакционное хранилище (OLTP) - Kafka.
- Сборщик логов - ELK.
- Все компоненты системы запускаются через Docker-compose.

# Запуск приложения
## Клонировать репозиторий
    git clone git@github.com:RuslanSibgatulin/graduate_work.git

## Подготовка окружения

Подготовить файлы с переменными окружения по аналогии с файлами `docker/envs/*.example` и пересохранить в файлы `*.env`


## Запуск
Выполнить в терминале:

    make start

# Команда
- [Ruslan Sibgatulin (lead)](https://github.com/RuslanSibgatulin)
- [Maxim Speshilov](https://github.com/paaanic)
- [Fedor Kuzminov](https://github.com/Riyce)