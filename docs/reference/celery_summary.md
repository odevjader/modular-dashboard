# Celery Summary

This document summarizes key Celery concepts, focusing on its setup with Redis, defining tasks, and operating workers.

## Core Concepts

Celery is a distributed task queue system.
- **Task:** A unit of work, typically a Python function.
- **Broker:** A message transport service (e.g., Redis, RabbitMQ) that mediates communication between clients (task publishers) and workers.
- **Worker:** A process that executes tasks. It fetches tasks from the broker.
- **Result Backend:** A store (e.g., Redis, database) used to save the state and results of tasks.
- **Celery Application:** An instance of `celery.Celery` that defines tasks, configuration, etc.

## Basic Setup (with Redis)

1.  **Installation:**
    ```bash
    pip install "celery[redis]"
    ```

2.  **Application Initialization (`tasks.py` or similar):**
    ```python
    from celery import Celery

    # For Redis as broker and backend
    app = Celery('my_project_tasks',
                 broker='redis://localhost:6379/0',
                 backend='redis://localhost:6379/1') # DB 1 for results

    # Example task
    @app.task
    def add(x, y):
        return x + y
    ```
    - `broker_url`: URL for the message broker.
    - `result_backend`: URL for the result store.

3.  **Configuration:**
    - Can be set directly on the `app.conf` object:
      ```python
      app.conf.task_serializer = 'json'
      app.conf.accept_content = ['json']  # Specify accepted content types
      app.conf.result_serializer = 'json'
      app.conf.timezone = 'UTC'
      app.conf.enable_utc = True
      app.conf.broker_transport_options = {'visibility_timeout': 3600} # Example for Redis
      ```
    - Or via a separate configuration module (e.g., `celeryconfig.py`):
      ```python
      # celeryconfig.py
      broker_url = 'redis://localhost:6379/0'
      result_backend = 'redis://localhost:6379/1'
      task_serializer = 'json'
      # ... other settings
      ```
      And then loaded: `app.config_from_object('celeryconfig')`

## Defining Tasks

- Use the `@app.task` decorator on a function.
- **Task Naming:** Automatically generated (e.g., `module.task_function`) or explicitly set via `name` argument.
- **Bound Tasks (`@app.task(bind=True)`):**
    - The first argument to the task becomes `self` (the task instance).
    - Allows access to `self.request` (task context: ID, args, retries, etc.).
    - Necessary for using `self.retry()`.
- **Common Task Options (passed to decorator or set on task class):**
    - `name='custom.task.name'`
    - `acks_late=True`: Acknowledge task message *after* execution. If worker crashes mid-task, task may re-run. Ensures at-least-once execution. Default is `False` (ack before execution - at-most-once if worker crashes). Task should be idempotent if `acks_late=True`.
    - `ignore_result=True`: Don't store task result/state.
    - `max_retries=5`: Max number of retries for `self.retry()`.
    - `default_retry_delay=60` (seconds): Default delay for retries.
    - `rate_limit='10/m'`: Limit execution to 10 tasks per minute (per worker).
    - `serializer='json'`: Task-specific serializer.
    - `track_started=True`: Report 'STARTED' state.
- **Retrying Tasks:**
    - Call `self.retry(exc=exception, countdown=seconds, max_retries=N)`. Requires `bind=True`.
    - `autoretry_for=(SpecificException, AnotherException)`: Automatically retry on these exceptions.
    - `retry_backoff=True`: Enable exponential backoff for automatic retries.
    - `retry_jitter=True`: Add random jitter to backoff delays (default).
- **Logging:**
    ```python
    from celery.utils.log import get_task_logger
    logger = get_task_logger(__name__)

    @app.task
    def my_task():
        logger.info("Task started")
    ```

## Running Workers

- **Command:**
  ```bash
  celery -A <app_module_name> worker -l INFO
  ```
  - `-A myapp.celery_app_instance`: Specify the Celery application instance.
  - `-l INFO`: Logging level.
  - `-c <number>` or `--concurrency <number>`: Number of child worker processes/threads (defaults to CPU cores).
  - `-n <name>@%h`: Set a unique node name, essential for multiple workers.
  - `-Q <queue1>,<queue2>`: Consume from specific queues.
  - `--max-tasks-per-child <N>`: Restart worker child process after N tasks.
  - `--max-memory-per-child <KILOBYTES>`: Restart worker child process if RSS memory exceeds this.
  - `--time-limit <SECONDS>` (hard), `--soft-time-limit <SECONDS>`: Task execution time limits.
- **Stopping Workers:**
    - `TERM` signal (Ctrl+C once): Warm shutdown (finishes current tasks).
    - `QUIT` signal: Cold shutdown (terminates active tasks immediately unless soft shutdown is configured).
- **Daemonization:** For production, use tools like `systemd` or `supervisor`. (See `Daemonization` guide in Celery docs).

## Key Celery Concepts for this Project

- **Using Redis as Broker:**
    - URL: `redis://your_redis_host:6379/0` (DB 0 for broker).
    - Reliable and fast.
    - `visibility_timeout` in `broker_transport_options` is important: how long a task can be unacknowledged before being redelivered.
- **Using Redis as Result Backend:**
    - URL: `redis://your_redis_host:6379/1` (e.g., DB 1 for results).
    - Stores task state and return values.
- **Task Idempotence:** Design tasks so they can be run multiple times with the same arguments without causing unintended side effects, especially if using `acks_late=True` or if retries are possible.
- **Error Handling & Retries:** Implement robust error handling and use Celery's retry mechanisms for transient errors.

References:
- First Steps: https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html
- Using Redis: https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html
- Tasks Guide: https://docs.celeryq.dev/en/stable/userguide/tasks.html
- Workers Guide: https://docs.celeryq.dev/en/stable/userguide/workers.html
- Configuration: https://docs.celeryq.dev/en/stable/userguide/configuration.html
