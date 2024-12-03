from src.authenticate import Auth
import sys

try:
    where = sys.argv[1]
except IndexError:
    print("Please specify where to authenticate")
    sys.exit(0)

auth = Auth(where)
auth.authenticate()
