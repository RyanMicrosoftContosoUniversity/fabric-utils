# Make submodules and key symbols visible at package import time.

# Submodules to expose at fabric_utils.<name>
__all__ = ["credential_utils", "layers", "logging", "shortcut", "CredentuialUtils", "credential_utilities"]

# Import submodules so they appear in dir(fabric_utils)
from . import credential_utils, layers, logging, shortcut

# Hoist important symbols to the top level
from .credential_utils import CredentuialUtils

# Optional alias if you expect 'credential_utilities'
credential_utilities = credential_utils

def __dir__():
    return sorted(list(globals().keys()) + [n for n in __all__ if n not in globals()])