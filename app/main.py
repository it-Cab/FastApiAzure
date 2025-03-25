import redis
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class Item(BaseModel):
    id: str
    name: str
    price: float

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.get("/")
async def read_item():
    try:
        # Check connection
        if redis_client.ping():
            print("Successfully connected to Redis!")
    except redis.ConnectionError as e:
        print(f"Failed to connect to Redis: {e}")
    return {"message": "Welcome to our app"}


@app.get("/hello/{name}")
async def read_item(name):
    return {"message": f"Hello {name}, how are you?"}


@app.post("/items/")
async def create_item(item: Item):
    cached_item = redis_client.set(item.id, {item.name, item.price})
    return {"message": cached_item}