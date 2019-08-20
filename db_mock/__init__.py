__version__ = "0.0.1"

import sys
from .mock_sync import DBMockSync

__all__ = ["DBMockSync"]

if sys.version_info[0] > 2:
    from .mock_async import DBMockAsync

    __all__.append("DBMockAsync")
    del sys
