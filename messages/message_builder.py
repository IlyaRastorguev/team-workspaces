import time


class MessageConst:
    MESSAGE_ID = "messageId"
    MESSAGE_NAME = "messageName"
    PAYLOAD = "payload"


class MessageBuilder:
    def __init__(self, message_name) -> None:
        self._message_name = message_name

    def build(self, message_data: dict = {}) -> dict:
        return {
            MessageConst.MESSAGE_ID: self._get_message_id(),
            MessageConst.MESSAGE_NAME: self._message_name,
            MessageConst.PAYLOAD: message_data,
        }

    @classmethod
    def generate_message_id(cls) -> int:
        timestamp = time.time()
        return int(str(timestamp).replace(".", ""))

    def _get_message_id(self) -> int:
        return self.generate_message_id()
