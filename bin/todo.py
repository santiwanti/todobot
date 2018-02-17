class Todo(object):
    # The class "constructor" - It's actually an initializer
    def __init__(self, id_num, description, sender=None, recipient=None):
        self._id_num = id_num
        self._sender = sender
        self._recipient = recipient
        self._description = description
        self._done = done

    @property
    def id(self):
        return self._id_num

    @property
    def sender(self):
        return self._sender

    @property
    def recipient(self):
        return self._recipient

    @property
    def description(self):
        return self._description
