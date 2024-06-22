# Анализатор страниц
[![Actions Status](https://github.com/Eugen980/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Eugen980/python-project-83/actions)
[![Actions Status](https://github.com/Eugen980/python-project-83/actions/workflows/linter.yml/badge.svg)](https://github.com/Eugen980/python-project-83/actions)

***
## Анализатор страниц - _Эта программа предназначена для анализа содержимого веб-страниц с целью извлечения информации, такой как заголовки, метаданные, ключевые слова и другие элементы._


# Установка

1. Склонируйте реозиторий на своё устройство:
```
https://github.com/Eugen980/python-project-50.git
```
2. Установите зависимости:
```
make install
```
3. Создайте файл '.env' и создайте переменные 'SECRET_KEY' содержащую ваш секретный ключ и 'DATABASE_URL' ссылающуюся на базу данных(Пример: DATABASE_URL=postgresql://user:password@localhost:5432/database)


# Ограничения программы:

* Программа не является универсальным инструментом для всех задач анализа веб-сайтов.
* Результаты могут зависеть от структуры и содержания анализируемых страниц.
* Для корректной работы программы необходимо подключение к интернету.


# Запуск

### Для запуска сервера Flask с помощью Gunicorn выполните команду:
```
make start
```
### Для запуска в режиме разработки: 
```
make dev
```


Чтобы добавить веб-страницу введите в поле ввода её название. После добавление сайта можно запусить проверку на открывшейся странице конкретного сайта. 

Так же можно вывести список всех добавленных сайтов нажав "_Сайты_" в шапке страницы.

***
### Демонтсрация работы программы

![bandicam 2024-06-22 18-59-57-530](https://github.com/Eugen980/python-project-83/assets/144818317/81813e49-6b36-42c9-8476-de43f783b363)

[_https://python-project-83-q4ur.onrender.com_](https://python-project-83-q4ur.onrender.com)