# Project #2 - Примитивная база данных

## Управление таблицами
- create_table <имя> <столбцы> - создать таблицу
- list_tables - список таблиц
- drop_table <имя> - удалить таблицу
- help - справка
- exit - выход

## Пример
Введите команду: create_table users name:str age:int
Таблица "users" успешно создана

## CRUD-операции
- insert into таблица values (значения) - добавить запись
- select from таблица - показать все записи
- select from таблица where условие - найти записи
- update таблица set столбец=значение where условие - обновить
- delete from таблица where условие - удалить

## Демонстрация asciinema с демонстрацией всех операций:
https://asciinema.org/a/y8s5FswFm3cqY7a4N3ZvZokPw
