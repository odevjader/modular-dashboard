# Redis Summary

This document provides a comprehensive summary of key Redis concepts, its use cases (particularly as a cache and a message broker for Celery), installation, client usage, configuration, and monitoring.

## Core Concepts

Redis is an open-source, in-memory data structure store, used as a database, cache, message broker, and streaming engine.
- **In-Memory:** Primarily stores data in RAM, which allows for very low-latency operations.
- **Data Types:** Supports various data structures:
    - Strings: Basic text or binary data.
    - Hashes: Field-value pairs, ideal for representing objects.
    - Lists: Ordered sequences, often used for queues.
    - Sets: Unordered collections of unique strings.
    - Sorted Sets (ZSETs): Sets where each member has an associated score, ordered by score. Useful for leaderboards, rate limiters.
    - Streams: Append-only log-like structures for managing streaming data with consumer groups.
    - JSON: Native support for JSON documents.
    - Bitmaps & HyperLogLogs: For space-efficient analytics.
    - Geospatial indexes: For location-based data.
- **Single-Threaded (for commands):** Redis executes commands one at a time (single-threaded), which simplifies its data model and avoids race conditions without requiring locks. However, I/O operations (like network communication) are multiplexed and can be handled by other threads, allowing Redis to handle many concurrent connections efficiently. Long-running commands can still block other clients.
- **Clients:** Many client libraries are available for different programming languages (Python, Java, Node.js, etc.).

## Installation

### Standalone Redis Server
- **Official Documentation:** Detailed instructions at [https://redis.io/docs/latest/get-started/installing-redis/](https://redis.io/docs/latest/get-started/installing-redis/).
- **Package Managers:**
    - Linux (apt): `sudo apt-get update && sudo apt-get install redis-server`
    - Linux (yum): `sudo yum install redis`
    - macOS (Homebrew): `brew install redis`
- **Docker:** A common method for development and deployment:
    ```bash
    # Basic Redis instance
    docker run -d -p 6379:6379 --name my-redis redis:7 # Specify version, e.g., redis:7

    # Run with AOF persistence and a local data volume
    docker run -d -p 6379:6379 --name my-redis-persistent \
      -v /path/to/local/redis/data:/data \
      redis:7 redis-server --appendonly yes
    ```

### Python Client (`redis-py`)
- The official Python client for Redis.
- **Installation:**
    ```bash
    pip install redis
    ```
- For potentially faster parsing of Redis protocol responses, `hiredis` (a C library) can be used:
    ```bash
    pip install redis[hiredis]
    ```

## Basic `redis-py` Usage

### Connection
```python
import redis

# Basic connection to Redis server
try:
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.ping() # Check if connection is successful
    print("Connected to Redis!")
except redis.exceptions.ConnectionError as e:
    print(f"Could not connect to Redis: {e}")

# Connection that decodes responses from bytes to strings
try:
    r_decoded = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    r_decoded.ping()
    print("Connected to Redis (with response decoding)!")
except redis.exceptions.ConnectionError as e:
    print(f"Could not connect to Redis (decoded): {e}")

# Using a connection pool (recommended for applications making multiple connections)
pool = redis.ConnectionPool(host='localhost', port=6379, db=0, decode_responses=True)
r_pooled = redis.Redis(connection_pool=pool)
```

### Common Commands Example
```python
# Assuming r_decoded is a connected Redis instance with decode_responses=True

# --- String operations ---
r_decoded.set('mykey', 'Hello Redis!')
value = r_decoded.get('mykey') # Returns 'Hello Redis!'
print(f"Get 'mykey': {value}")

r_decoded.set('anotherkey', 'some value', ex=3600) # Set with 1-hour expiry (in seconds)
r_decoded.setnx('newkey', 'newvalue') # Set if key does not already exist

# --- Hash operations (for objects) ---
r_decoded.hset('user:1000', mapping={
    'username': 'johndoe',
    'email': 'john.doe@example.com',
    'visits': 10
})
username = r_decoded.hget('user:1000', 'username') # Returns 'johndoe'
print(f"Username from hash: {username}")

user_data = r_decoded.hgetall('user:1000') # Returns a dict
print(f"All user data: {user_data}")

r_decoded.hincrby('user:1000', 'visits', 1) # Increment hash field value

# --- List operations (can be used as a simple queue) ---
r_decoded.lpush('mylist', 'item1', 'item2', 'item3') # Pushes to the head (left)
# Current list: ['item3', 'item2', 'item1']
item = r_decoded.rpop('mylist') # Pops from the tail (right) -> 'item1' (FIFO if lpush/rpop)
print(f"Popped item: {item}")
length = r_decoded.llen('mylist') # Get list length
print(f"Current list length: {length}")
```

## Redis as a Cache

Redis is widely used as a cache to reduce latency and load on primary databases or services.
- **High Performance:** Sub-millisecond latency due to its in-memory nature.
- **Common Caching Patterns:**
    - **Cache-Aside:** The application code is responsible for checking the cache first. If data is present (cache hit), it's returned. If not (cache miss), the application fetches data from the database, stores it in the cache (with a TTL - Time To Live), and then returns it. Suitable for read-heavy workloads.
    - **Read-Through:** The cache itself (often a library or framework feature built on Redis) is responsible for loading data from the database on a cache miss. The application interacts as if Redis is the main data source.
    - **Write-Through:** Data is written to the cache and the database simultaneously (or cache writes to DB synchronously). Ensures cache and DB consistency but can add latency to writes.
    - **Write-Behind (Write-Back):** Data is written to the cache, which acknowledges the write. The cache then asynchronously writes the data to the database. Improves write performance but has a risk of data loss if the cache fails before data is persisted.
    - **Write-Around:** Data is written directly to the database. Only data that is read is then put into the cache.
- **Eviction Policies:** When Redis reaches its `maxmemory` limit, it can evict keys based on configured policies (e.g., `volatile-lru` (evict least recently used keys with an expiry set), `allkeys-lru` (evict any least recently used key), `volatile-ttl` (evict keys with shortest time-to-live)).

## Redis as a Message Broker

Redis can serve as a message broker, facilitating communication between different parts of an application.
- **Key Redis features for messaging:**
    - **Lists:** Can be used to implement simple FIFO (First-In, First-Out) message queues. `LPUSH` to add messages, `BRPOP` (blocking right pop) for workers to retrieve messages. This is a common pattern for Celery.
    - **Pub/Sub (Publish/Subscribe):** Allows messages to be broadcast to multiple subscribers. Clients subscribe to channels (topics), and publishers send messages to these channels. Useful for real-time notifications or when multiple consumers need the same message. Not typically used by Celery for primary task queuing but can be used for event notifications.
    - **Streams:** A more robust and persistent data structure for messaging. Streams are append-only logs that support consumer groups (allowing multiple consumers to cooperatively process messages from the same stream, with each message going to only one consumer in a group), message persistence, and explicit acknowledgments. More complex but offers better guarantees than Lists for reliable messaging.

## Redis for Celery

Celery is a distributed task queue system. Redis is a popular choice as both a message broker and a result backend for Celery due to its speed and simplicity.

### Celery Installation with Redis Support
```bash
pip install celery[redis]
```
This also installs `redis-py`.

### Celery Configuration
- **Broker URL:** Tells Celery where to connect to Redis for sending/receiving task messages.
    - Basic: `broker_url = 'redis://localhost:6379/0'` (DB 0 on localhost)
    - With Password: `broker_url = 'redis://:yourpassword@your_redis_host:6379/0'`
    - SSL: `broker_url = 'rediss://:yourpassword@your_redis_host:6379/0'`
    - Unix Socket: `broker_url = 'redis://localhost:6379/0?socket_timeout=5&path=/path/to/redis.sock'`
- **Result Backend URL:** If storing task results/states in Redis.
    - `result_backend = 'redis://localhost:6379/1'` (Use a different Redis DB, e.g., DB 1)
    - Similar password, SSL, socket options apply.
- **Key Transport Options (`broker_transport_options`):**
    - **`visibility_timeout` (Crucial):** How long a task message remains "invisible" after a worker retrieves it. If not acknowledged (task completion/failure) within this time, Redis makes it visible again for another worker.
        - **Set it longer than your longest task's expected completion time** to prevent tasks from running multiple times.
        - Example in `celery_app.conf`:
          ```python
          # app.conf.broker_transport_options = {'visibility_timeout': 3600} # 1 hour
          ```
    - Other options: `retry_policy`, `max_retries` for connection retries.
- **Result Backend Options (`result_backend_transport_options`):** Similar to broker options if applicable.
- **Task Result Expiry (`result_expires`):** Set a default expiry time for task results stored in Redis to prevent memory exhaustion.
    ```python
    # app.conf.result_expires = timedelta(days=1) # or in seconds
    ```

### Redis Persistence for Celery
- **Importance:** Crucial in production to prevent loss of task messages or results if the Redis server restarts.
- **RDB (Snapshots):** Point-in-time backups. Good for backups, faster restarts with large datasets. Potential data loss between snapshots.
    - Configured in `redis.conf` (e.g., `save 900 1`, `save 300 10`).
- **AOF (Append Only File):** Logs every write operation. Higher durability, less data loss. Can be slower to restart than RDB if the file is large.
    - Configured in `redis.conf` (e.g., `appendonly yes`, `appendfsync everysec`).
    - **Recommendation for Celery:** AOF with `appendfsync everysec` is generally a good balance for message queue durability.
- **Ensure your Redis server is configured for persistence in production.**

### Other Important Considerations for Celery + Redis
- **Database Numbers:** Use different logical Redis DBs for broker and results if on the same instance to avoid key collisions.
- **Connection Pooling:** `redis-py` manages connection pools. Celery has settings like `redis_max_connections` for its result backend pool.
- **Memory Management:** Monitor Redis memory. Long queues or many stored results can consume significant memory. Configure `maxmemory` and `maxmemory-policy` in `redis.conf` if Redis is shared or needs memory capping. For Celery queues, you generally don't want task messages to be evicted by memory policies.
- **Idempotent Tasks:** Design tasks to be idempotent if `visibility_timeout` issues or retries might cause them to run more than once.

## Basic Setup & Configuration (`redis.conf`)
- **Installation:** See "Installation" section above.
- **Configuration File:** `redis.conf`. Key settings:
    - `bind 127.0.0.1` (Bind to localhost, or specific IPs. `0.0.0.0` for all interfaces - ensure firewall if public).
    - `port 6379` (Default port).
    - `requirepass yourverycomplexpassword` (Enable password authentication).
    - Persistence options (RDB `save` lines, AOF `appendonly`, `appendfsync`).
    - `maxmemory <bytes>` (e.g., `maxmemory 2gb`).
    - `maxmemory-policy <policy>` (e.g., `volatile-lru`).
    - Logging (`logfile`, `loglevel`).
- **Security:**
    - Bind to trusted interfaces.
    - Use strong passwords (`requirepass`).
    - Network security (firewalls).
    - Rename or disable dangerous commands (e.g., `FLUSHALL`, `CONFIG`) for production environments accessible from untrusted clients using the `rename-command` directive in `redis.conf`.

## Monitoring Redis
- **`redis-cli monitor`**: Streams all commands processed by the Redis server. Useful for debugging.
- **`redis-cli info`**: Provides a wealth of information and statistics (memory, clients, persistence, keyspace, CPU usage).
    - `redis-cli info memory`
    - `redis-cli info stats`
    - `redis-cli info keyspace`
- **Redis Insight:** A free GUI tool from Redis Labs for monitoring and interacting with Redis.
- **Celery Monitoring Tools:** Tools like Flower can also provide insights into queue lengths, which indirectly reflect Redis state for Celery.

## References
- Redis Documentation: [https://redis.io/docs/latest/](https://redis.io/docs/latest/)
- Redis Get Started: [https://redis.io/docs/latest/get-started/](https://redis.io/docs/latest/get-started/)
- Develop with Redis: [https://redis.io/docs/latest/develop/](https://redis.io/docs/latest/develop/)
- Redis Data Types: [https://redis.io/docs/latest/develop/data-types/](https://redis.io/docs/latest/develop/data-types/)
- Redis Persistence: [https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/)
- Caching with Redis: [https://redis.io/solutions/caching/](https://redis.io/solutions/caching/)
- Messaging with Redis: [https://redis.io/solutions/messaging/](https://redis.io/solutions/messaging/)
- `redis-py` Client GitHub: [https://github.com/redis/redis-py](https://github.com/redis/redis-py)
- `redis-py` ReadTheDocs: [https://redis.readthedocs.io/en/stable/](https://redis.readthedocs.io/en/stable/)
- Celery Configuration (Redis Backend Settings): [https://docs.celeryq.dev/en/stable/userguide/configuration.html#redis-backend-settings](https://docs.celeryq.dev/en/stable/userguide/configuration.html#redis-backend-settings)
- Celery Broker Overview: [https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/index.html](https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/index.html)
