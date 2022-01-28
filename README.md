# Avito Parser
![pexels-photo-1546168](https://user-images.githubusercontent.com/53881876/151635131-47f56091-4839-4322-8aea-de08124f706e.jpeg)


Helps to find the real-estate objects with interesting redemption value that you set, on Avito site (and may be others marketplaces in future). 
Sends notifications to telegram, stores information about checked objects, checks every single real-estate object to changes in them. 
Constant monitoring with necessary latency. Auto-start and auto-stop in certain time. Shows the status of work on parser's homepage. 

## Local development
At the root of the project, you will find two docker-compose files. In order to start local development of a project, you need to rename the docker-compose.yaml file to docker-compose-prod.yaml, and docker-compose-dev.yaml to docker-compose.yaml, in which the settings for local development are saved. After that, you just have to execute the command:

docker-compose up

The project will be available at the local address: http://127.0.0.1/

After making the necessary changes, rename the docker-compose files in reverse order. This will make the project ready for deployment.
