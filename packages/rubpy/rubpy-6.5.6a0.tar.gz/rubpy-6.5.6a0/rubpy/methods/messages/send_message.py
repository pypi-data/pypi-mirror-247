from typing import Optional, Union
from random import random


class SendMessage:
    async def send_message(
            self,
            object_guid: str,
            text: Optional[str] = None,
            reply_to_message_id: Union[int, str] = None,
            file_inline: Optional[dict] = None,
            type: Optional[str] = 'FileInline',
    ):
        if text is not None:
            text = text.strip()

        if reply_to_message_id is not None:
            reply_to_message_id = str(reply_to_message_id)

        input = {
            'object_guid': object_guid,
            'text': text,
            'reply_to_message_id': reply_to_message_id,
            'rnd': int(random() * 1e6 + 1),
        }

        return await self.builder('sendMessage', input=input)