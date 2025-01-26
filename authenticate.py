import asyncio
from src.authenticate import Auth
import sys

try:
    where = sys.argv[1]
except IndexError:
    print("Please specify where to authenticate")
    sys.exit(0)

if __name__ == "__main__":
    asyncio.run(Auth(where).authenticate())
