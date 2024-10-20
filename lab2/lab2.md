# Отчет по 2 лабораторной работе

## `Bad practices` в Dockerfile

В данной лабораторной работе я создал два `Dockerfile` для запуска некого приложения `app.py`
- *Dockerfile_bad* - Dockerfile c bad practices
- *Dockerfile_better* - Dockerfile с исправленными bad practices

### `Dockerfile_bad`

```
FROM python:3.10-slim

RUN apt-get update && apt-get install -y build-essential

RUN mkdir /app
RUN cd /app
RUN touch app.py

COPY . /app

WORKDIR /app

CMD ["python", "app.py"]
```

Разберем плохие практики по одной

### Установка пакетов без указания версии

`RUN apt-get update && apt-get install -y build-essential`

Так как суть docker контейнеров в том, что их можно запускать на любой конфигурации ОС и результат везде будет одинаковым, это может нарушиться из-за несоответсвия версий устанавливаемых пакетов.

Поэтому следует напрямую указывать версии пакетов, которые устанавливаются поверх исходного образа контейнера

### Чрезмерное количество слоёв

```
RUN mkdir /app
RUN cd /app
RUN touch app.py
```

Каждая команда RUN добавляет логический слой в образ (? не уверен в терминологии), и поэтому их плодить слишком много не обязательно, следует все объединить в один вызов

### Запуск рабочего приложения от `root`

```
COPY . /app

WORKDIR /app

CMD ["python", "app.py"]
```

Запуск приложения от имени супер пользователя (root) может быть опасен для приложения, так как при таком запуске приложение сможет делать абсолютно все что угодно, это может быть опасно.

### Dockerfile_better

Привожу листинг улучшенного *Dockerfile*

```
FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential=12.9 python3-dev=3.8.5

WORKDIR /app
COPY . /app

RUN useradd -m myuser && chown -R myuser:myuser /app
USER myuser

CMD ["python", "app.py"]
```

Пакеты установлены с указанием версий, лишние пакеты при установке убраны флагом `--no-install-recommends`

## Плохие практики по работе с контейнерами

### Запуск процессов вручную

Тут идет речь о взаимодействии с контейнерами, например, через `docker exeс`. Этот метод недопустим почти никогда, так как нарушает основные правила контейнеризации - масштабируемость и универсальность.

Лично я использую `docker exec` лишь в случаях, когда в лабораторных условиях мне надо проверить какую-либо особенность поведения приложения внутри контейнера, не более.

### Использование контейнеров для хранения данных

Не рекомендуется использовать контейнеры для хранения важной информации или данных без использования внешних хранилищ (docker volumes).

Это следует из принципов контейнеризации - контейнер может быть в любой момент удален, выключен, перемещен. Соответственно, в таком случае важная информация может быть утеряна.

# Задание со звездочкой

Плохие практики при написании docker-compose файлов

## `docker-compose_bad.yml`
```
version: '3'

services:
  web:
    image: nginx:latest
    ports:
      - "8080:80"
    environment:
      - DEBUG=true
    volumes:
      - ./app:/var/www/html

  db:
    image: postgres
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_PASSWORD=mysecretpassword
    volumes:
      - ./data:/var/lib/postgresql/data
    depends_on:
      - web
```

### Использование host network

По умолчанию каждый контейнер использует сеть хоста, то есть выкидывает все свои порты как обычный сервис на хосте.

Если же использовать `docker networks`, то сразу появляется возможность обращаться к контейнерам по доменным именам между ними, docker выставляет порт открытым лишь в эту сеть, а значит, что с меньшей вероятностью особенности хоста будут влиять на работу контейнеров.

### Привязка открытых портов к 0.0.0.0

```
  db:
    image: postgres
    ports:
      - "5432:5432"
```

В этом случае все запросы на порт `5432` на данную машину будут перенаправляться в контейнер.

И в общем случае это опасно, так как если вы работаете в команде, то нельзя быть уверенным, что у всех на рабочем компьютере правильно настроен firewall. Да и в продакшне тоже таких серьезных vulnerability допускать нельзя.

### Отсутствие лимитов ресурсов для контейнеров

Отсутствие указания лимитов по памяти и CPU может привести к неконтролируемому потреблению ресурсов контейнерами, что может негативно сказаться на производительности хоста и других контейнеров.

## `docker-compose_better.yml`

```
version: '3.8'

services:
  web:
    image: nginx:1.21.6
    ports:
      - "127.0.0.1:8080:80"
    environment:
      - DEBUG=false
    volumes:
      - ./app:/var/www/html
    networks:
      - app_network
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 512M

  db:
    image: postgres:13.4
    environment:
      POSTGRES_PASSWORD: mysecretpassword
    volumes:
      - db_data:/var/lib/postgresql/data
    networks:
      - app_network 
    deploy:
      resources:
        limits:
          cpus: '1.00'
          memory: 1G
    depends_on:
      - web

volumes:
  db_data:

networks:
  app_network:
    driver: bridge
```

### Разделение сервисов по сетям

Требуется настроить сервисы так, чтобы они поднимались вместе, в рамках одного compose преокта, но при этом не имели доступа друг к другу.

Реализовано через создание двух различных подсетей docker network, так, что каждый контейнер находится в своей сети.

Этот способ полезен тем, что позволяет изолировать критически важные сервисы от остальных, также позволяет разделить тестирование и отладку всей системы. Ну и конечно же ради безопасности и разграничения доступа.


```
version: '3.8'

services:
  web:
    image: nginx:1.21.6
    ports:
      - "127.0.0.1:8080:80"
    environment:
      - DEBUG=false
    volumes:
      - ./app:/var/www/html   # Mount the app folder for NGINX to serve
    networks:
      - web_network           # Web сервис подключен к своей сети
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 512M

  db:
    image: postgres:13.4
    environment:
      POSTGRES_PASSWORD: mysecretpassword
    volumes:
      - db_data:/var/lib/postgresql/data
    networks:
      - db_network            # DB сервис подключен к своей сети
    deploy:
      resources:
        limits:
          cpus: '1.00'
          memory: 1G
    depends_on:
      - web

volumes:
  db_data:

networks:
  web_network:               # Определение изолированной сети для web-сервиса
    driver: bridge
  db_network:                # Определение изолированной сети для db-сервиса
    driver: bridge
```

