# Setup Local

A short demo project. This example code is used to set up a FastAPI service and host it in an Azure container instance.


0. Build the Docker Image

````
docker build -t myimage .
````

1. Install python dependencies

````
pip install -r requirements.txt
````

2. Start the Docker mycontainer and redis

````
docker run --name mycontainer -p 80:80 myimage 
&& docker run -p 6379:6379 -it redis/redis-stack:latest
````
local swagger should appear >>> http://localhost:8080/docs or http://127.0.0.1:8080/docs


uvicorn app.main:app --reload

# Dploy to Azure

1. Build image
````
docker build --platform linux/amd64 -t rlexamplefastapi.azurecr.io/fastapi:build-tag-1 .
````

2. push
```
docker push rlexamplefastapi.azurecr.io/fastapi:build-tag-1  
````