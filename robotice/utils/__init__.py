
from robotice.utils.database import PickledRedis
from robotice.utils.decorators import norecursion
from robotice.utils.dictionary import dict_merge
from robotice.utils.subprocess import call_command

import logging

LOG = logging.getLogger(__name__)

__all__ = [
    "PickledRedis",
    "norecursion",
    "dict_merge",
    "call_command",
]

from functools import partial, wraps

PENDING_DEPRECATION_FMT = """
    {description} is scheduled for deprecation in \
    version {deprecation} and removal in version v{removal}. \
    {alternative}
"""

def warn_deprecated(description=None, deprecation=None,
                    removal=None, alternative=None, stacklevel=2):
    ctx = {'description': description,
           'deprecation': deprecation, 'removal': removal,
           'alternative': alternative}
    if deprecation is not None:
    	# for now only log warn
        LOG.warning(PENDING_DEPRECATION_FMT.format(**ctx))

def deprecated(deprecation=None, removal=None,
               alternative=None, description=None):
    """Decorator for deprecated functions.
    A deprecation warning will be emitted when the function is called.
    :keyword deprecation: Version that marks first deprecation, if this
      argument is not set a ``PendingDeprecationWarning`` will be emitted
      instead.
    :keyword removal:  Future version when this feature will be removed.
    :keyword alternative:  Instructions for an alternative solution (if any).
    :keyword description: Description of what is being deprecated.
    """
    def _inner(fun):

        @wraps(fun)
        def __inner(*args, **kwargs):
            warn_deprecated(description=description or fun.__name__,
                            deprecation=deprecation,
                            removal=removal,
                            alternative=alternative,
                            stacklevel=3)
            return fun(*args, **kwargs)
        return __inner
    return _inner