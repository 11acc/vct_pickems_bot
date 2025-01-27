
import redis


# Global redis connection
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def check_redis_connection(r):
    try:
        r.ping()
        return True
    except redis.ConnectionError:
        return False
