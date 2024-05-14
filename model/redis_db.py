import redis
from contextlib import contextmanager
import logging


class RedisClient:
    def __init__(self, host, port, password, db, max_connections=50, timeout=10):
        self.connection_pool = redis.ConnectionPool(
            host=host,
            port=port,
            password=password,
            max_connections=max_connections,
            db=db,
            decode_responses=True
        )
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)

    @contextmanager
    def get_connection(self):
        conn = None
        try:
            conn = redis.Redis(connection_pool=self.connection_pool)
            yield conn
        except redis.exceptions.RedisError as e:
            self.logger.error(f"Redis error: {e}")
            raise e
        finally:
            if conn is not None:
                conn.close()

    def set(self, key, value, ex=None, nx=False, xx=False):
        with self.get_connection() as conn:
            try:
                return conn.set(key, value, ex=ex, nx=nx, xx=xx)
            except redis.exceptions.RedisError as e:
                return False

    def get(self, key):
        with self.get_connection() as conn:
            try:
                return conn.get(key)
            except redis.exceptions.RedisError as e:
                return False

    def lpush(self, key, *values):
        with self.get_connection() as conn:
            try:
                return conn.lpush(key, *values)
            except redis.exceptions.RedisError as e:
                return False

    def rpush(self, key, *values):
        with self.get_connection() as conn:
            try:
                return conn.rpush(key, *values)
            except redis.exceptions.RedisError as e:
                return False

    def lrange(self, key, start, end):
        with self.get_connection() as conn:
            try:
                return conn.lrange(key, start, end)
            except redis.exceptions.RedisError as e:
                return False

    def ltimeset(self, key, time):
        with self.get_connection() as conn:
            try:
                return conn.expire(key, time)
            except redis.exceptions.RedisError as e:
                return False

    def zadd(self, key, *args, **kwargs):
        with self.get_connection() as conn:
            try:
                return conn.zadd(key, *args, **kwargs)
            except redis.exceptions.RedisError as e:
                return False

    def zrange(self, key, start, end, desc=False, withscores=False, score_cast_func=float):
        with self.get_connection() as conn:
            try:
                return conn.zrange(key, start, end, desc=desc, withscores=withscores, score_cast_func=score_cast_func)
            except redis.exceptions.RedisError as e:
                return False

    def delete(self, *keys):
        with self.get_connection() as conn:
            try:
                return conn.delete(*keys)
            except redis.exceptions.RedisError as e:
                return False

    def key_exists(self, key):
        with self.get_connection() as conn:
            try:
                return conn.exists(key)
            except redis.exceptions.RedisError as e:
                return False

    def close(self):
        self.connection_pool.disconnect()

    def keys(self, pattern):
        with self.get_connection() as conn:
            try:
                return conn.keys(pattern)
            except redis.exceptions.RedisError as e:
                return None


redis_client = RedisClient(host='192.168.17.129', port=6379, password='', db=1)