import os
import subprocess
import time
import glob

from collections import namedtuple

towatch = os.path.abspath('teamstrong11_9')

FileInfo = namedtuple("FileInfo", "filename timestamp")

def timestamps(directory):
    for filename in glob.glob(os.path.join(directory, '*.py')):
        timestamp = os.stat(filename).st_mtime
        yield FileInfo(filename, timestamp)

while True:

    # start up a new game, now begin polling for changes.
    original = set(timestamps('teamstrong11_9'))
    pygame = subprocess.Popen(['./bin/python', 'run_game.py'])

    # poll poll poll, eventually the modified timestamp will change.
    while True:

        time.sleep(1)
        updated = set(timestamps('teamstrong11_9'))

        # check if the sets don't match.
        if updated != original:
            break

    pygame.kill()






