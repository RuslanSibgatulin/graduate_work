# Дипломная работа: Рекомендательная система
[![Generic badge](https://img.shields.io/badge/Changelog-<COLOR>.svg)](./CHANGELOG.md)
[![Generic badge](https://img.shields.io/badge/Our-Team-<COLOR>.svg)](#команда)
[![Generic badge](https://img.shields.io/badge/Architecture-<COLOR>.svg)](./schema.jpg)


Этот сервис будет предлагать фильмы для пользователя и будет использовать 2 подхода в рекомендациях:
- На основе контента из описания к фильмам
- Коллаборативная фильтрация на основе просмотров другими пользователями 


[Ссылка на приватный репозиторий с командной работой.](https://github.com/RuslanSibgatulin/graduate_work)


## Используемые технологии
- Код приложения на Python + fastapi.
- Транзакционное хранилище (OLTP) - Kafka.
- Хранилище BigData - MongoDB.
- Сборщик логов - ELK.
- Все компоненты системы запускаются через Docker-compose.

# Запуск приложения
## Состав проекта
Для рекомендательной системы зависимостями являются разработанные ранее компоненты:

- [Панель администрирования фильмов](http://localhost/admin)
- [API фильмов](http://localhost/api/apidocs)
- [Сервис авторизации](http://localhost/auth/apidocs/)
- [Сервис UGC](http://localhost/ugc/apidocs)

Все они доступны из репозитория: https://github.com/Riyce/Admin_panel_sprint_2


## Клонировать репозиторий
    git clone git@github.com:RuslanSibgatulin/graduate_work.git

## Подготовка окружения

Подготовить файлы с переменными окружения по аналогии с файлами `docker/envs/*.example` и пересохранить в файлы `*.env`
    
    make env


## Запуск
Выполнить в терминале:

    make start

Документация сервиса будет доступна по ссылке http://localhost/recommendations/apidocs

# Команда
- [Ruslan Sibgatulin (lead)](https://github.com/RuslanSibgatulin)
- [Maxim Speshilov](https://github.com/paaanic)
- [Fedor Kuzminov](https://github.com/Riyce)