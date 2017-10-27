class ThreadMessage:
    def __init__(self, message_id, data=None):
        if data is None:
            data = []
        self.message_id = message_id
        self.data = data
