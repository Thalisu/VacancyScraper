from rq import Worker, Queue
from .connection import redis_conn

if __name__ == "__main__":
    worker = Worker(
        queues=[Queue(connection=redis_conn)],
        connection=redis_conn,
        default_worker_ttl=None,
    )
    worker.work()
