from rq import Worker, Queue
from redis import Redis

from src.utils.config import get_config

port: int = get_config("REDIS_PORT") or 6379
redis_conn = Redis(host="localhost", port=port)

worker = Worker(
    queues=[Queue(connection=redis_conn)],
    connection=redis_conn,
    default_worker_ttl=None,
)
worker.work()
