# Celery Summary - Distributed Task Queue

This document provides a comprehensive summary of Celery, covering its core concepts, installation, application setup (especially with Redis), task definition, worker operation, monitoring, and best practices.

## Overview & Core Concepts

Celery is an open-source, simple, flexible, and reliable distributed system to process vast amounts of messages, while providing operations with the tools required to maintain such a system. It’s a task queue with a focus on real-time processing, while also supporting task scheduling.

- **Task:** A unit of work, typically a Python function or method that you want to run asynchronously or periodically. In Celery, you define tasks by decorating Python functions with `@app.task`.
- **Broker:** A message transport service (e.g., Redis, RabbitMQ) that mediates communication between clients (task publishers, i.e., your application code) and workers. The client adds a message to the queue, and the broker delivers it to a worker.
- **Worker (`celery worker`):** Processes that run on one or more servers. They continuously monitor task queues for new work. When a new task arrives, a worker picks it up and executes the corresponding Python function.
- **Result Backend (Optional):** A datastore (e.g., Redis, database, RabbitMQ RPC-style) used to store the state (e.g., PENDING, STARTED, SUCCESS, FAILURE) and results of tasks. Essential if you need to know if a task completed, its return value, or if it failed.
- **Celery Application (`celery.Celery` instance):** The heart of a Celery setup. An instance of `celery.Celery` is used to define tasks, configuration, and integrate Celery into your project.

## Installation

- **Core Celery Package:**
    ```bash
    pip install celery
    ```
- **With Broker/Backend Specific Dependencies:**
    - For Redis support (as both broker and result backend):
        ```bash
        pip install "celery[redis]"
        ```
        This will also install `redis-py` if not already present.
    - For RabbitMQ (using `librabbitmq` or `py-amqp`):
        ```bash
        pip install "celery[librabbitmq]"
        # or
        pip install "celery[amqp]"
        ```

## Basic Application Setup (with Redis)

Typically, you define a Celery application instance. This can be in a dedicated module (e.g., `celery_app.py` or `proj/celery.py`).

**Example (`celery_app.py` or `tasks.py`):**
```python
from celery import Celery
import time # For example task

# Create a Celery application instance
# The first argument is the name of the current module (or a project name),
# important for Celery to auto-discover tasks.
app = Celery('my_project_tasks',
             broker='redis://localhost:6379/0',    # DB 0 for broker
             backend='redis://localhost:6379/1')   # DB 1 for results (good practice)
             # include=['your_project.tasks_module']) # Optional: list of modules to import when worker starts

# Optional: Load configuration from a separate configuration file (e.g., celeryconfig.py)
# app.config_from_object('celeryconfig')
# Or configure directly:
# app.conf.update(
#     task_serializer='json',
#     accept_content=['json'],
#     result_serializer='json',
#     timezone='UTC',
#     enable_utc=True,
#     broker_transport_options={'visibility_timeout': 3600} # 1 hour
# )

# Example task definition
@app.task
def add(x, y):
    return x + y

@app.task
def long_running_task(duration):
    time.sleep(duration)
    return f"Task completed after {duration} seconds"
```
- `broker_url`: URL for the message broker.
- `result_backend`: URL for the result store.

## Configuration (`celeryconfig.py` or `app.conf.update(...)`)

Celery offers many configuration options. Set them directly on `app.conf` or use `app.config_from_object('yourconfigmodule')`.

**Example `celeryconfig.py`:**
```python
# celeryconfig.py

# Broker settings
broker_url = 'redis://localhost:6379/0'

# Result backend settings
result_backend = 'redis://localhost:6379/1'
result_expires = 3600  # Expire results after 1 hour (in seconds)

# Task serialization settings
task_serializer = 'json'  # Default is pickle; json is safer and more portable for cross-language/version compatibility.
result_serializer = 'json'
accept_content = ['json'] # Specify accepted content types (important for security)

# Timezone settings (recommended for scheduled tasks / ETA)
timezone = 'UTC'
enable_utc = True # Ensure Celery uses UTC internally

# Broker transport options (specific to the broker, e.g., Redis)
broker_transport_options = {
    'visibility_timeout': 43200  # 12 hours (in seconds). Adjust based on longest task.
                                 # For Redis, this prevents tasks from being re-delivered if a worker
                                 # is processing it for longer than this timeout.
}

# Result backend transport options (if applicable)
# result_backend_transport_options = {'visibility_timeout': 3600}

# Other common settings
# task_acks_late = True # Acknowledge task after completion/failure. Requires idempotent tasks.
# worker_prefetch_multiplier = 1 # For long tasks, especially with acks_late=True.
# worker_concurrency = 4 # Set default number of worker processes.
# worker_max_tasks_per_child = 100 # Recycle worker processes after 100 tasks.
# worker_max_memory_per_child = 500000 # Recycle worker if it exceeds 500MB RAM (in KB).
```
**Loading config:** `app.config_from_object('celeryconfig')`

## Defining Tasks

Tasks are Python functions decorated with `@app.task`.
- **Task Naming:** Automatically generated (e.g., `your_module.task_function`) or explicitly set via `name` argument in the decorator (`@app.task(name='custom.task.name')`).
- **Bound Tasks (`@app.task(bind=True)`):**
    - The first argument to the task becomes `self` (the task instance itself).
    - Allows access to `self.request` (task context: ID, args, retries, etc.) and methods like `self.retry()`.
- **Logging:**
    ```python
    from celery.utils.log import get_task_logger
    logger = get_task_logger(__name__) # Logger is configured by Celery

    @app.task
    def my_logged_task():
        logger.info("Task started, processing data...")
    ```
- **Retrying Tasks:**
    - Call `self.retry(exc=exception, countdown=seconds, max_retries=N)`. Requires `bind=True`.
    - `autoretry_for=(SpecificException, AnotherException)`: Decorator argument to automatically retry on these exceptions.
    - `retry_backoff=True`, `retry_backoff_max=700`, `retry_jitter=True`: Decorator arguments for exponential backoff with jitter.
    ```python
    from .celery_app import app # Assuming app is defined in celery_app.py
    import time

    @app.task(bind=True, max_retries=3, default_retry_delay=60) # default_retry_delay in seconds
    def my_retry_task(self, data_id):
        try:
            # Simulate fetching data and processing, which might fail
            data = fetch_data_from_external_service(data_id, self.request.retries)
            if not data:
                logger.warning(f"Data ID {data_id} not found, retrying... (Attempt {self.request.retries + 1})")
                # Exponential backoff for retries, using default_retry_delay as base
                raise self.retry(exc=ValueError(f"Data not found for {data_id}"),
                                 countdown=int(self.default_retry_delay * (2 ** self.request.retries)))
            processed_data = process_data(data)
            return processed_data
        except ConnectionError as exc: # Example of specific exception handling for retry
            logger.error(f"Connection error for {data_id}, retrying... (Attempt {self.request.retries + 1})")
            raise self.retry(exc=exc, countdown=int(self.default_retry_delay * (1.5 ** self.request.retries))) # Different backoff
        except Exception as e:
            logger.exception(f"Unhandled exception for task {self.request.id}: {e}")
            # self.update_state(state='FAILURE', meta={'exc_type': type(e).__name__, 'exc_message': str(e)})
            raise # Re-raise to mark task as FAILED and propagate to result backend

    # Dummy functions for example
    def fetch_data_from_external_service(data_id, retries_attempted):
        if data_id == "fail_once" and retries_attempted == 0: return None
        if data_id == "conn_error" and retries_attempted == 0: raise ConnectionError("Simulated connection error")
        return {"id": data_id, "content": "some data"}
    def process_data(data): return f"Successfully processed {data['id']}"
    ```
- **Common Task Options (passed to decorator or set on task class):**
    - `name='custom.task.name'`
    - `acks_late=True`: Acknowledge task message *after* execution (success/failure). If worker crashes mid-task, task may re-run. Ensures at-least-once execution. Default is `False` (ack before execution - at-most-once if worker crashes). **Task should be idempotent if `acks_late=True`**.
    - `ignore_result=False`: Set to `True` if you don't need to store task result/state. Default is `False` if a `result_backend` is configured.
    - `max_retries=3`, `default_retry_delay=180` (seconds).
    - `rate_limit='10/m'`: Limit execution to 10 tasks per minute (per worker type or globally).
    - `serializer='json'`: Task-specific serializer.
    - `track_started=True`: Report 'STARTED' state to the result backend.

## Running Workers
Workers are started from the command line using the `celery` command.
- **Basic command:** (assuming `app` is discoverable in `your_project.celery_app` or `your_project.tasks`)
  ```bash
  celery -A your_project.celery_app worker --loglevel=INFO
  ```
  (Replace `your_project.celery_app` with the actual Python path to your Celery app instance).
- **Specify concurrency (number of child worker processes/threads):**
  ```bash
  celery -A your_project.celery_app worker -c 4 --loglevel=INFO
  ```
  (Default is the number of CPU cores). For I/O bound tasks, you might use more threads/gevent workers.
- **Specify queues:**
  ```bash
  celery -A your_project.celery_app worker -Q important_tasks,default_tasks -c 8
  ```
- **Set a unique node name (hostname):** Essential for multiple workers on different machines or even the same machine.
  ```bash
  celery -A your_project.celery_app worker -n worker1@%h -c 4
  ```
  (`%h` is replaced by hostname, including domain).
- **Other useful options:**
    - `--max-tasks-per-child <N>`: Restart worker child process after N tasks (helps manage memory leaks).
    - `--max-memory-per-child <KILOBYTES>`: Restart worker child process if RSS memory exceeds this.
    - `--time-limit <SECONDS>` (hard), `--soft-time-limit <SECONDS>`: Task execution time limits. Soft limit raises an exception, hard limit terminates the task.
- **Stopping Workers:**
    - `TERM` signal (Ctrl+C once): Warm shutdown (finishes current tasks before exiting).
    - `QUIT` signal (Ctrl+\\ or second Ctrl+C): Cold shutdown (terminates active tasks immediately unless soft shutdown is configured).
- **Daemonization:** For production, use tools like `systemd` or `supervisor` to manage worker processes. (See `Daemonization` guide in Celery docs).

## Calling Tasks
- **`.delay(*args, **kwargs)`:** A convenient shortcut to `apply_async` with default parameters.
    ```python
    from .tasks import add # Assuming tasks.py contains the 'add' task

    result_object = add.delay(4, 5)
    print(f"Task ID: {result_object.id}")
    ```
- **`.apply_async(args=None, kwargs=None, countdown=None, eta=None, queue=None, expires=None, ...)`:** Provides more control.
    ```python
    from datetime import datetime, timedelta

    add.apply_async(args=(10, 20), countdown=10) # Execute in 10 seconds
    eta_time = datetime.utcnow() + timedelta(hours=2)
    add.apply_async(kwargs={'x': 5, 'y': 5}, eta=eta_time) # Execute at specific UTC time
    add.apply_async((100,100), queue='priority_tasks', priority=0) # Send to specific queue, set priority (broker dependent)
    ```

### AsyncResult Object
Calling a task returns an `AsyncResult` object, used to check state, wait for completion, and get results (if a result backend is configured).
```python
result_obj = add.delay(2, 2)

print(f"Task ID: {result_obj.id}")
print(f"Is task ready? {result_obj.ready()}") # False initially

# Wait for the result (blocking call)
# result_value = result_obj.get(timeout=10) # Waits up to 10 seconds
# print(f"Result: {result_value}") # Raises exception if task failed, unless propagate=False

# Check status without blocking
# print(f"Task state: {result_obj.state}") # PENDING, STARTED, SUCCESS, FAILURE, RETRY, REVOKED
# if result_obj.successful(): print(f"Result: {result_obj.result}")
# if result_obj.failed(): print(f"Traceback: {result_obj.traceback}")

# result_obj.forget() # If you don't need the result, this can free resources in some backends.
```

## Canvas: Designing Workflows
Celery allows composing complex workflows using primitives:
- **Signature (`.s()` or `.si()` for immutable):** A task call blueprint. `add.s(2, 3)` creates `add(2, 3)`.
- **Chain:** Links tasks sequentially; output of one becomes input of the next. `chain(add.s(2, 2) | multiply.s(8))()`.
- **Group:** Executes a list of tasks in parallel. `group(add.s(i, i) for i in range(3))()`.
- **Chord:** Executes a group (header) in parallel, then passes their results as a list to a callback task. `chord([add.s(i, i) for i in range(10)])(tsum.s())`.
- **Chunks:** Split an iterable of work into smaller parts.
- **Map/Starmap:** Similar to Python's built-in `map`.

## Monitoring
- **Flower:** Real-time web-based monitoring and administration tool.
    - Install: `pip install flower`
    - Run: `celery -A your_project.celery_app flower --broker=redis://localhost:6379/0 --port=5555`
- **Celery CLI:**
    - `celery -A app status`: Active workers.
    - `celery -A app inspect active`: Active tasks.
    - `celery -A app inspect scheduled`: Scheduled (ETA) tasks.
    - `celery -A app control enable_events`: Enable events for monitoring.
- **Broker-Specific Tools:** Redis: `redis-cli monitor`, `redis-cli llen <queue_name>`. RabbitMQ: Management Plugin UI.

## Best Practices & Optimization
- **Idempotent Tasks:** Crucial if `task_acks_late=True` or if retries are possible.
- **Visibility Timeout (Redis/SQS):** Set `broker_transport_options = {'visibility_timeout': ...}` longer than your longest task.
- **Task Acknowledgement (`task_acks_late`):** `True` for reliability (requires idempotency), `False` for speed if some task loss is acceptable on worker crash.
- **Prefetch Multiplier (`worker_prefetch_multiplier`):** Default is 4. For long tasks, set to 1, especially with `acks_late=True`.
- **Worker Concurrency (`-c`):** Adjust based on CPU cores and task type (CPU-bound vs. I/O-bound).
- **Memory Management (`worker_max_tasks_per_child`, `worker_max_memory_per_child`):** Recycle worker children to manage memory.
- **Separate Queues & Routing:** Use different queues for different task priorities or types.
- **Error Handling & Retries:** Implement robust error handling and use Celery's retry mechanisms.
- **Task Logging:** Use Python's `logging` module.
- **Keep Tasks Small & Focused:** Break down large operations into smaller tasks, orchestrated with Canvas.
- **Redis Key Eviction:** If using Redis, ensure its `maxmemory-policy` is `noeviction` or one less likely to evict Celery's internal keys/queues.
- **Key Celery Concepts for this Project (Recap):**
    - **Using Redis as Broker/Backend:** Reliable and fast. Remember `visibility_timeout` and separate DBs for broker/backend.
    - **Task Idempotence:** Essential for tasks that might be retried or re-run due to `acks_late=True`.
    - **Error Handling & Retries:** Leverage `self.retry()`, `autoretry_for` for robust task execution.

## References
- Celery Official Documentation: [https://docs.celeryq.dev/en/stable/](https://docs.celeryq.dev/en/stable/)
- First Steps with Celery: [https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html](https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html)
- Using Redis with Celery: [https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html](https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html)
- Tasks Guide: [https://docs.celeryq.dev/en/stable/userguide/tasks.html](https://docs.celeryq.dev/en/stable/userguide/tasks.html)
- Workers Guide: [https://docs.celeryq.dev/en/stable/userguide/workers.html](https://docs.celeryq.dev/en/stable/userguide/workers.html)
- Canvas - Designing Workflows: [https://docs.celeryq.dev/en/stable/userguide/canvas.html](https://docs.celeryq.dev/en/stable/userguide/canvas.html)
- Routing Tasks: [https://docs.celeryq.dev/en/stable/userguide/routing.html](https://docs.celeryq.dev/en/stable/userguide/routing.html)
- Monitoring Guide: [https://docs.celeryq.dev/en/stable/userguide/monitoring.html](https://docs.celeryq.dev/en/stable/userguide/monitoring.html)
- Optimizing Guide: [https://docs.celeryq.dev/en/stable/userguide/optimizing.html](https://docs.celeryq.dev/en/stable/userguide/optimizing.html)
- Configuration and Defaults: [https://docs.celeryq.dev/en/stable/userguide/configuration.html](https://docs.celeryq.dev/en/stable/userguide/configuration.html)
- Flower (Monitoring Tool) Documentation: [https://flower.readthedocs.io/en/latest/](https://flower.readthedocs.io/en/latest/)
