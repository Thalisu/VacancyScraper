from rq import Worker, Queue
from redis import Redis

redis_conn = Redis(host="localhost", port=6379)

worker = Worker(
    queues=[Queue(connection=redis_conn)],
    connection=redis_conn,
    default_worker_ttl=None,
)
worker.work()
