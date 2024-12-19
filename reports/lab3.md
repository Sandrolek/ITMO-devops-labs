# Отчет по 3 лабораторной работе

Я поставил себе задачу реализовать CI/CD для работы с докером и `Dockerhub`, соответственно проверять процесс сборки контейнера и его запуска, а также публикации на `Dockerhub` образа

## Приложение

Написал простое приложение на js, которое создает сервер на localhost:3000

index.js
```javascript
const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.send('Hello, Docker World!');
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
```

И простой `Dockerfile`
```Dockerfile
FROM node:14

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
```

## Bad practices `ci-cd.yml`

```yaml
name: Docker build & publish

on: push

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@latest

      - uses: docker/setup-buildx-action@latest

      - uses: docker/login-action@latest
        with:
          username: username
          password: P@ssw0rd

      - run: |
          docker build -t username/lab3-docker:ci_cd lab3/

      - run: |
          docker push username/lab3-docker:ci_cd

      - run: |
          docker run -d -p 3000:3000 username/lab3-docker:ci_cd
          sleep 5
          curl http://localhost:3000
```

## Best practices

### 1. Использование timeout

Указывать параметр timeout для джобы, чтобы github actions не крутился несколько часов с ошибкой.

Было:
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
```

Стало:
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 10
```

### 2. Точное указание триггеров

Нет нужды вызывать джобу связанную с функционалом одной ветки при пуше в другую

Было:
```yaml
on: push
```

Стало:
```yaml
on:
  push:
    branches:
      - lab3
  pull_request:
    branches:
      - main
```

### 3. Описания для шагов

Лучше всегда подписывать шаги в джобе, чтобы было нагляднее проверять процесс

Было:
```yaml
steps:
    - uses: actions/checkout@latest
```

Стало:

```yaml
steps:
    - name: Checkout code
    uses: actions/checkout@v2
```

### 4. Фиксирование версий

Чтобы не нарваться на ошибки в новых версиях, или на ошибки взаимодействия новейших версий одних продуктов с другими, лучше всегда фиксировать конкретную версию, с которой работаем

Было:
```yaml
steps:
    - uses: actions/checkout@latest
```

Стало:

```yaml
steps:
    uses: actions/checkout@v2
```

### 5. Не хранить креды для подключения в коде

Тут довольно все очевидно, не хранить в plaintext креды внутри конфига. Best Practice включает в себя работу с `BitWarden`

Было:
```yaml
- uses: docker/login-action@latest
    with:
        username: username
        password: P@ssw0rd
```

Стало:

```yaml
- name: Log in to Docker Hub
    uses: docker/login-action@v2
    with:
        username: ${{ env.DOCKERHUB_USERNAME }}
        password: ${{ env.DOCKERHUB_TOKEN }}
```


## Best practices `ci-cd.yml`

```yaml
name: Docker build & publish

on:
  push:
    branches:
      - lab3
  pull_request:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Bitwarden secrets
        uses: bitwarden/sm-action@v2
        with:
          access_token: ${{ secrets.BITWARDEN_ACCESS_TOKEN }}
          base_url: https://vault.bitwarden.com
          secrets: |
            1d141966-9cef-4330-b528-b24b0116f428 > DOCKERHUB_USERNAME
            598586dd-78b8-49e4-bd9d-b24b011703d4 > DOCKERHUB_TOKEN

      - name: Log in to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ env.DOCKERHUB_USERNAME }}
          password: ${{ env.DOCKERHUB_TOKEN }}

      - name: Build Docker image
        run: |
          docker build -t ${{ env.DOCKERHUB_USERNAME }}/lab3-docker:ci_cd lab3/

      - name: Push Docker image
        run: |
          docker push ${{ env.DOCKERHUB_USERNAME }}/lab3-docker:ci_cd

      - name: Run Docker container
        run: |
          docker run -d -p 3000:3000 ${{ env.DOCKERHUB_USERNAME }}/lab3-docker:ci_cd
          sleep 5
          curl http://localhost:3000
```

### BitWarden

Хранение секретов во внешнем хранилище намного лучше, чем в переменных самого CI/CD. 
- Доступ к данным можно ограничить, конкретному проекту будут доступны лишь конкретные секреты по конкретному **access token**.
- Хранилище секретов можно поднять локально в закрытом контуре, что в комплексе с собственным CI/CD сервером создает хорошую схему.
- Не надо вручную обновлять секреты, ведь по одному **access token**-у у джобы, она получит доступ к новым данным автоматически.

Как пример я использовал BitWarden, так как это довольно простой `secret vault`

В своем аккаунте я сделал проект, в которой добавил 2 секрета - учетку от `Dockerhub`, и создал `Machine acoount`, для которой сделал **access token** и его я и прокинул в файл CI/CD.

#### Использование BitWarden файле CI/CD

```yaml
- name: Bitwarden secrets
        uses: bitwarden/sm-action@v2
        with:
          access_token: ${{ secrets.BITWARDEN_ACCESS_TOKEN }}
          base_url: https://vault.bitwarden.com
          secrets: |
            1d141966-9cef-4330-b528-b24b0116f428 > DOCKERHUB_USERNAME
            598586dd-78b8-49e4-bd9d-b24b011703d4 > DOCKERHUB_TOKEN

      - name: Log in to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ env.DOCKERHUB_USERNAME }}
          password: ${{ env.DOCKERHUB_TOKEN }}
```

### Финальная проверка
Проверки все проходятся, если же будет что-то нарушено - неверные креды для `DockerHub`, не собирается образ - то Actions упадут на соответствующем шаге.

![Result](/reports/images/ci-cd-good.png)

![Result](/reports/images/docker-image.png)