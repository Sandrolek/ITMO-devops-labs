# Отчет по 1 лабораторной работе

Задачу я поставил перед собой следующую - поднять `nginx` + 2 приложения на `FastAPI` в `docker compose`, предварительно настроив их образы через соответствующие `Dockerfiles`.

Решил сделать таким образом, так как знаком с `docker compose`, а также `FastAPI`, и сделать два маленьких приложения не составляет труда.

## 1. Приложения на `FastAPI`
Страница приложения `app1`. Просто и без воды

```
<html>
    <head>
        <title>App</title>
    </head>
    <body>
        <h1>App 1</h1>
    </body>
</html>
```

`Dockerfile` для приложения
> В requirements.txt лежат uvicorn и fastapi - просто небольшая `good practice`
```
FROM python:3.12

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 2. Nginx

### Сертификаты

Самоподписанные сертификаты сгенерированы с помощью инструмента `openssl`

В FQDN был указан `localhost`
```
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \ 
        -keyout nginx.key \
        -out nginx.crt
```

### Конфиг
Приведу куски `nginx.conf`, которые отвечают за части задания

Все части конфига будут приведены из секции `http` конфига, так как настроено для взаимодействия по `http/https`

*Запуск nginx не в бэкграунде, требуется для корректной работе в контейнере*
```
daemon off;
```

*Редирект с `http` на `https`*
```
http {
    ...
    server {
        listen 80;
        return 301 https://$host$request_uri;
    }
}
```
*Alias для обращения к приложению в конфиг файле*
```
http {
    ...
    upstream app1 {
        server app1:8000;
    }
}
```

*Самоподписанный сертификат и ключ для него*
```
http {
    ...
    server {
        listen 443 ssl;

        ssl_certificate /etc/nginx/ssl/nginx.crt;
        ssl_certificate_key /etc/nginx/ssl/nginx.key;
    }
}
```

*Роуты/алиасы для проксирования трафика внутри nginx*
```
http {
    ...
    server {
        ...
        location /app1 {
            proxy_pass http://app1/;
        }

        location /app2/ {
            proxy_pass http://app2/;
        }

        location /secret {
            alias /etc/nginx/html/data/;
        }
    }
}
```
---
### Dockerfile

Запуск nginx, предварительно скопировав туда необходимые файлы

```
FROM nginx:1.27.1-alpine

COPY html /etc/nginx/html

COPY nginx.conf /etc/nginx/nginx.conf
COPY nginx.crt /etc/nginx/ssl/nginx.crt
COPY nginx.key /etc/nginx/ssl/nginx.key

CMD ["nginx"]
```

## 3. Docker compose

*Каждое приложение как отдельный сервис, с указанием своего `Dockerfile` и именем*
```
services:
  ...
  
  app1:
    build: 
      context: app1
      dockerfile: Dockerfile
    container_name: app1
```

*Также указан свой `Dockerfile` и exposed порты. Добавлять зависимости от других контейнеров - необходимая практика в проектах с большим количеством контейнеров*
```
services:
  ...
  nginx:
    build:
      context: nginx
      dockerfile: Dockerfile
    container_name: nginx
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - app1
      - app2
```

## 4. Заключение

Результат запущенного проекта

![Result](/reports/images/lab1_res.png)

## 5. Вывод
В ходе выполнения лабораторной работы я вспомнил принципы работы `docker compose`, генерации сертификатов и созданию нескольких приложений в один проект.