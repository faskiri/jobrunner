import datetime
import logging
import os
import subprocess
import shlex
import time

from .config import Job

logger = logging.getLogger(__name__)

DATETIME_FORMAT = "%a %b %d %H:%M:%S %Y"

class Runner(object):
    """
    >>> os.remove('status.txt')
    >>> jobs = [Job(path='ls -ltr', id='Job1', frequency='daily'), Job(path='doo', id='Job2', frequency='daily')]
    >>> r = Runner(jobs)
    >>> r.run()
    1
    >>> r.run()
    0
    """
    def __init__(self, jobs):
        self._jobs = jobs
        self._status = {}
        self._load_status()

    def run(self):
        num_ok_jobs = 0
        for j in self._jobs:
            if not self._should_run(j): continue
            try:
                process = subprocess.Popen([
                    os.path.expanduser(x) for x in shlex.split(j.path)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
                out, err = process.communicate()
                logger.debug('%s output: %s err: %s', j.id, out, err)
                if process.returncode != 0: continue
                self._status[j.id] = time.strftime(DATETIME_FORMAT)
                num_ok_jobs += 1
            except:
                logger.exception('Could not run %s', j)
        self._store_status()
        return num_ok_jobs

    def _load_status(self):
        if not os.path.exists('status.txt'): return
        with open('status.txt', 'r') as f:
            for l in f:
                job, last = l.split(':', 1)
                self._status[job] = last.strip()

    def _store_status(self):
        with open('status.txt', 'w') as f:
            for j in self._status:
                f.write('%s:%s\n' % (j, self._status[j]))

    def _should_run(self, job):
        if self._status.get(job.id) is None:
            logger.debug('No info about %s', job)
            return True

        last = time.mktime(time.strptime(self._status[job.id], DATETIME_FORMAT))
        since = time.time() - last
        logger.debug('The job %s was last run %s secs ago', job, since)
        if job.frequency == 'daily' and since > 24 * 60 * 60:
            logger.debug('Running %s', job)
            return True
        return False

if __name__ == '__main__':
    import doctest
    logging.basicConfig(level=logging.DEBUG)
    doctest.testmod()
