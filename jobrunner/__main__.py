import logging
import logging.handlers
import os
import time

from .config import Config
from .runner import Runner

logger = logging.getLogger(__name__)

def main():
    c = Config()
    c.load('jobs.ini')
    r = Runner(c.jobs)
    r.run()

def init_logs():
    root_logger = logging.getLogger()
    handler = logging.handlers.RotatingFileHandler(
            filename='jobrunner.log',
            maxBytes=1024 * 1024,
            backupCount=1)
    handler.setFormatter(
            logging.Formatter("%(levelname)s %(asctime)s [%(process)d] %(name)s - %(message)s"))
    root_logger.addHandler(handler)
    root_logger.setLevel(level=logging.DEBUG)

def trylock(lockfile):
    logging.debug('Trying to acquire %s', lockfile)
    if os.path.exists(lockfile):
        lockstats = os.stat(lockfile)
        since = time.time() - lockstats.st_ctime
        logging.debug('Lock created %s secs ago', since)
        if since < 60 * 60:
            logging.debug('Lock fresh, skip')
            return False
    with open(lockfile, 'a') as f:
        f.write(str(os.getpid()))
    return True

if __name__ == '__main__':
    init_logs()
    lockfile='jobrunner.lock'
    if trylock(lockfile):
        try:
            main()
        except:
            logger.exception('Could not run')
        finally:
            os.unlink(lockfile)
