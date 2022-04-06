# Avito Parser
![pexels-photo-1546168](https://user-images.githubusercontent.com/53881876/151635131-47f56091-4839-4322-8aea-de08124f706e.jpeg)


Helps you find properties on the Avito website (and possibly in other markets in the future) with interesting redemption value that you set. 
Sends notifications to telegram, stores information about checked objects, checks every single real-estate object for price changes. 
Constant monitoring with necessary latency. Auto-start and auto-stop in certain time. Shows the work status on parser's homepage. 

## Local development
At the root of the project, you will find two docker-compose files. In order to start local development of a project, you need to rename the docker-compose.yaml file to docker-compose-prod.yaml, and docker-compose-dev.yaml to docker-compose.yaml, in which the settings for local development are saved. After that, you just have to execute the command:
```
docker-compose up
```
The project will be available at the local address: ```http://127.0.0.1:8000/```

After making the necessary changes, rename the docker-compose files in reverse order. This will make the project ready for deployment.

## Environment variables
You need to define environment variables with .env file in the project root directory before start the project:
- ENV_SECRET_KEY - secret project key, for example 'erofheronoirenfoernfx49389f43xf3984xf9384' 
- BOT_TOKEN - token to access the tTelegram HTTP API, for example '1363975876:AAF-XflZxV4UswWgc9g1JoHgI9v-nYcVHdM'
- CHAT_ID - Telegram chat id, for example '431690822' or '@nosov_develop'
- DEBUG - debug mode, True or False
- DB_ENGINE - for example 'django.db.backends.postgresql'
- DB_NAME - create database name
- POSTGRES_USER - create database username
- POSTGRES_PASSWORD - create database user password
- DB_HOST - database host, for example 'localhost' or name of service in docker compose
- DB_PORT - database port, by default it is 5432 
##### Superuser creating while first project start 
- DJANGO_SUPERUSER_USERNAME - create superuser name
- DJANGO_SUPERUSER_PASSWORD - create superuser password
- DJANGO_SUPERUSER_EMAIL - create superuser email
