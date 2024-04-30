import redis

class RedisConnection(object):
    
    def __init__(self) -> None:
        pass

    def redis_connection(self, host=None):
        
        return redis.Redis(host='localhost', port=6379, decode_responses=True, db=1)

    def redis_connection_pipeline(self):
        return self.redis_connection().pipeline()