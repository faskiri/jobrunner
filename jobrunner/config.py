import ConfigParser
import collections
import logging

logger = logging.getLogger(__name__)

Job = collections.namedtuple('Job', ['path', 'id', 'frequency'])

class Config(object):
    """
    >>> import tempfile
    >>> t=tempfile.NamedTemporaryFile()
    >>> t.write(\"\"\"
    ... [Job1]
    ... path: foo
    ... frequency: daily
    ... 
    ... [Job2]
    ... path: doo
    ... frequency: daily
    ... \"\"\"
    ... )
    >>> t.flush()
    >>> c = Config()
    >>> c.load(t.name)
    >>> c.jobs
    [Job(path='foo', id='Job1', frequency='daily'), Job(path='doo', id='Job2', frequency='daily')]
    """

    def __init__(self):
        self.jobs = []

    def load(self, path):
        config = ConfigParser.SafeConfigParser()
        c = config.read([path])
        logger.debug('Found config: %s', c)
        for s in config.sections():
            self.jobs.append(Job(
                config.get(s, 'path'),
                s,
                config.get(s, 'frequency')))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
