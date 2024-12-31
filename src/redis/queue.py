from redis import Redis

from rq import Queue

redis_connection = Redis(host="localhost", port=6379)
main_task_queue = Queue("main_task_queue", connection=redis_connection)


if __name__ == "__main__":
    main_task_queue.empty()
