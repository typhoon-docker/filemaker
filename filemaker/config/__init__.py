from config.default import *

try:
    from config.local import *
except ModuleNotFoundError:
    pass
