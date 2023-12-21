from .update_handler import UpdateHandler
from ..objects import Message


class MessageHandler(UpdateHandler):
    can_handle = Message

    def __init__(self, callback, condition=None):
        super().__init__(callback, condition)
