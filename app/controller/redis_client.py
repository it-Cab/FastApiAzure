import redis
import os
import logging


class RedisClient:
    def __init__(self, ssl=True):
        self.host = "redis-fastapi.redis.cache.windows.net"
        self.port = 6380
        self.password = "ESkfRmdDYGRTMj9MFWvMoMKqQjGAunkReAzCaN9YlSU="
        self.ssl = ssl

        try:
            self.redis_client = redis.StrictRedis(
                host=self.host, port=self.port, password=self.password, ssl=self.ssl
            )
            # Ping to ensure the connection is established
            self.redis_client.ping()
            logging.info("Successfully connected to Azure Redis Cache!")
        except redis.ConnectionError as e:
            logging.error(f"Redis connection error: {e}")
            raise e

    def set(self, key, value):
        try:
            res = self.redis_client.set(key, value)
            return res
        except Exception as e:
            logging.error(f"Error setting key {key}: {e}")
            raise e

    def hashes_set(self, key, id, value):
        try:
            res = self.redis_client.hset(key, id, value)
            return res
        except Exception as e:
            logging.error(f"Error setting key {key}: {e}")
            raise e
        
    def hashes_set_assignment(self, key, id, value):
        try:
            res = self.redis_client.hset(key, id, value)
            self.redis_client.expire(key, 1800)
            return res
        except Exception as e:
            logging.error(f"Error setting key {key}: {e}")
            raise e

    def get_by_id(self, key, id):
        try:
            value = self.redis_client.hget(key, id)
            if value:
                return value.decode("utf-8")
            return None
        except Exception as e:
            logging.error(f"Error getting key {key}: {e}")
            raise e

    def hashes_get(self, key):
        try:
            res = self.redis_client.hgetall(key)
            return res
        except Exception as e:
            logging.error(f"Error setting key {key}: {e}")
            raise e

    def delete(self, key):
        try:
            res = self.redis_client.delete(key)
            if res != 0:
                return res
            return None
        except Exception as e:
            logging.error(f"Error deleting key {key}: {e}")
            raise e

    def hashes_delete(self, key, id):
        try:
            res = self.redis_client.hdel(key, id)
            if res != 0:
                return res
            return None
        except Exception as e:
            logging.error(f"Error deleting key {key}: {e}")
            raise e
