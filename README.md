# Aciniformes-project

Проект пингера сервисов профкома ФФ МГУ. Позволяет пользователю просто и быстро проверять работоспособность любого сайта и сервиса и получать отчет через telegram бота.


# Функционал

1. Опрос любого сервиса или сайта на работоспособность
2. Создание расписания проверок указанных сайтов/сервисов
3. Получение удобного отчета о проверке через telegram бота

# Разработка
Backend разработка – https://github.com/profcomff/.github/wiki/%5Bdev%5D-Backend-разработка


# Quick Start
1. Перейдите в папку проекта

2. Создайте виртуальное окружение командой:
`foo@bar:~$ python3 -m venv ./venv/`
3. Установите библиотеки командой:
`foo@bar:~$ pip install -m requirements.txt`
4. Установите все переменные окружения (см. CONTRIBUTING.md)
5. Запускайте приложение!
`foo@bar:~$ python -m services-backend`


# Использование
## Настройка сервиса через Docker Compose
```yml
version: '3.8'

services:
  postgres:
    image: postgres:14
    restart: always
    volumes:
      - postgres:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: pinger
      POSTGRES_PASSWORD: qwerty123

  backend:
    image: ghcr.io/profcomff/aciniformes-project:latest
    restart: always
    ports:
      - 80:80
    depends_on:
      - postgres
      - migration
    environment:
      - DB_DSN=postgresql://pinger:qwerty123@postgres:5432/postgres
      - AUTH_URL=https://api.profcomff.com/auth

  pinger:
    image: ghcr.io/profcomff/aciniformes-project:latest
    restart: always
    depends_on:
      - postgres
      - migration
    environment:
      - DB_DSN=postgresql://pinger:qwerty123@postgres:5432/postgres
      - AUTH_URL=https://api.profcomff.com/auth
    command: python -m aciniformes_project worker

volumes:
  postgres:
```

## API запросы
1. Создание получателя сообщений
   1. Получить или узнать токен telegram бота, через которого будет посылаться сообщение
   2. Узнать id чата-получателя в telegram
   3. Создать получателя сообщений, выполнив запрос POST /receiver с телом: `{"url": "https://api.telegram.org/bot{токен_бота}/sendMessage", "method": "post", "receiver_body": {"chat_id": id_получателя, "text": текст_сообщения}`

2. Создание опрашиваемого сервиса
   1. Выполнить запрос POST /fetcher с телом: `"{
  "type_": "get/post/ping",
  "address": "ссылка на опрашиваемый сайт",
  "fetch_data": "{}" (Имеет смысла заполнять только если в type_ указан post запрос),
  "delay_ok": частота опроса при успешном запросе,
  "delay_fail": частота опроса при неудавшемся запросе
}"`

# Параметризация и плагины
BOT_TOKEN - токен бота-отправителя отчетов

# Ссылки
Документация проекта - https://api.test.profcomff.com/?urls.primaryName=pinger#
Backend разработка – https://github.com/profcomff/.github/wiki/%5Bdev%5D-Backend-разработка
