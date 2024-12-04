import os


def get_config(name):
    return os.environ.get(name)
