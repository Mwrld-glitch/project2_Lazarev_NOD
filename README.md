# Project #2 - Примитивная база данных

**Автор:** Лазарев Виктор Самвелович. НОД.
## Установка базы данных
make install
## Запуск базы данных
make database
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

### Обработка ошибок
Централизованная обработка через декоратор @handle_db_errors:
- KeyError - таблица или столбец не найден
- ValueError - ошибки валидации данных
- FileNotFoundError - файлы данных не найдены

### Подтверждение действий
Опасные операции требуют подтверждения:
- `@confirm_action("удаление таблицы")` - для drop_table
- `@confirm_action("удаление записей")` - для delete

### Замер производительности  
Декоратор @log_time показывает время выполнения операций:
- insert, select - работа с файлами

### Кэширование
Замыкание create_cacher() ускоряет повторные запросы select

## Демонстрация asciinema с демонстрацией всех операций:
https://asciinema.org/a/y8s5FswFm3cqY7a4N3ZvZokPw

## Демонстрация asciinema с работой декораторов:
https://asciinema.org/a/DoJybCM1A4K554JjW4nwyFpZu

