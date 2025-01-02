from redis import Redis
from src.utils.config import get_config

host: str = get_config("REDIS_HOST") or "localhost"
port: int = get_config("REDIS_PORT") or 6379

redis_conn = Redis(host=host, port=port)
