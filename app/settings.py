import logging
import os
from os.path import dirname, join

log = logging.getLogger()
log.setLevel(logging.DEBUG)

TOKEN = os.getenv('TOKEN')
DATA_DIR = join(dirname(__file__), '..', 'data')

if __name__ == "__main__":
    print(DATA_DIR)
    print(TOKEN)
