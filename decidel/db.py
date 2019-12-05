from flask_redis import FlaskRedis

redis_store = FlaskRedis(decode_responses=True)
