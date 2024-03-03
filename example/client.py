import redis
import time

r = redis.Redis(host="localhost",port=6379)
start = time.time()
for i in range(0,20_000):
    print(i," ",r.set("key-"+str(i),"value-"+str(i)))

end = time.time()

print(" total time in sec: " ,end - start)