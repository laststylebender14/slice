Slice
===
Slice is an ultra-simple, Python-based, in-memory key-value store that communicates using the RESP protocol (redis use this for communication).

```
 ____  _ _            ____  ____  
/ ___|| (_) ___ ___  |  _ \| __ ) 
\___ \| | |/ __/ _ \ | | | |  _ \ 
 ___) | | | (_|  __/ | |_| | |_) |
|____/|_|_|\___\___| |____/|____/ 

```

## Why should you care?

Building a database from scratch can be an exhilarating experience. With Slice, you can:

- build a database from scratch
- learn database internals, starting with Redis
- learn about advanced data structures, algorithms, and event loops (io multiplexing)
- collaborate with other engineers and contribute back to Open Source

## Why Use Slice?

While production use of Slice might not be ideal, it offers a perfect platform for:

Educational Purposes: Learn the fundamentals of key-value stores and database systems in a practical way.
Experimentation and Prototyping: Rapidly test and validate data storage concepts for small-scale projects.
Building a Foundation for Redis: Get comfortable with the RESP protocol used by Redis before diving into the full-fledged server.


## Getting Started

To run SliceDB locally, you'll need:

### Using Python

You'll need:
1. **Python 3+**
2. A supported platform environment:
   - Linux-based environment
   - OSX (Darwin) based environment

```
$ git clone https://github.com/ranjitmahadik/slice-db
$ cd slice-db
$ pip3 install -r requirements.txt
$ mv .example.env .env
$ python3 main.py
```

### Using Docker

You'll need:
1.  **Docker**
```
$ git clone https://github.com/ranjitmahadik/slice-db
$ cd slice-db
$ mv .example.env .env
$ docker compose up -d
```


## Slice in action

Slice communicates in the Redis dialect, allowing seamless integration with any Redis client. To interact with Slice:

- Use a [Redis CLI](https://redis.io/docs/manual/cli/) for quick access.
- Programmatically connect using your preferred Redis library in the language of your choice.

**Example:**
```python
import redis

client = redis.Redis(host='localhost', port=6379)
client.set('key', 'value')
print(client.get('key'))  # Output: b'value'
```

## Get Involved

Ready to dive into Slice? Join our community and contribute to the project on [GitHub](https://github.com/ranjitmahadik/slice-db). Whether you're a seasoned developer or just starting out, there's room for everyone to learn and grow together.
