__version__ = "0.5.2"

from .client import Client
from .sync_support import add_sync_support

add_sync_support()
