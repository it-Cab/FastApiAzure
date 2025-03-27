import redis
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class Item(BaseModel):
    id: str
    name: str
    price: float


redis_client = redis.StrictRedis(
    host="redis-fastapi.redis.cache.windows.net",
    port=6380,
    password="ESkfRmdDYGRTMj9MFWvMoMKqQjGAunkReAzCaN9YlSU=",
    ssl=True,
)


@app.get("/")
async def read_item():
    res = redis_client.ping()
    print(res)
    return {"message": "Welcome to our app"}


@app.get("/hello/{name}")
async def read_item(name):
    return {"message": f"Hello {name}, how are you?"}


@app.post("/items/")
async def create_item(item: Item):
    return {"message": f"{item.name} is priced at £{item.price}"}


@app.get("/api/areas")
async def get_area(id):
        res = redis_client.get(id)
        return res or None