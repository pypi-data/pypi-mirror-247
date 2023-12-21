from .send_message import SendMessage
from .create_poll import CreatePoll
from .delete_messages import DeleteMessages
from .edit_message import EditMessage
from .forward_messages import ForwardMessages
from .request_send_file import RequestSendFile


class Messages(
    SendMessage,
    CreatePoll,
    DeleteMessages,
    EditMessage,
    ForwardMessages,
    RequestSendFile,
):
    pass