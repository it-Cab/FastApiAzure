# Setup

A short demo project. This example code is used to demonstrate how to quickly set up a FastAPI service and host it in an Azure container instance.

0. Build the Docker Image

````
docker build -t myimage .
docker-compose up --build -d
````

1. Install python dependencies

````
pip install -r requirements.txt
````

2. Start the Docker mycontainer and redis

````
docker run -d --name mycontainer -p 80:80 myimage && docker run -p 6379:6379 -it redis/redis-stack:latest
````
local swagger should appear >>> http://localhost/docs or http://127.0.0.1/docs


uvicorn app.main:app --reload