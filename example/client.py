import redis

r = redis.Redis(host="localhost",port=6379)
print(r.set("redis","hello"))
print(r.get("redis"))