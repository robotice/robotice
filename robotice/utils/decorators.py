"Functions that help with dynamically creating decorators for views."
import logging

LOG = logging.getLogger(__name__)

def norecursion(default=None, callcount=2):
    '''Prevents recursion into the wrapped function.'''
    def entangle(f):
        def inner(*args, **kwds):
            if not hasattr(f, 'callcount'):
                f.callcount = 0
            if f.callcount >= callcount:
                LOG.warning("recursion detected %s calls deep. exiting." % f.callcount)
                return default
            else:
                f.callcount += 1
                x = f(*args, **kwds)
                f.callcount -= 1
                return x
        return inner
    return entangle