from .advanced import Advanced
from .utilities import Utilities
from .users import Users
from .auth import Auth
from .messages import Messages
from .chats import Chats
from .groups import Groups
from .decorators import Decorators


class Methods(
    Advanced,
    Utilities,
    Users,
    Auth,
    Messages,
    Chats,
    Groups,
    Decorators,
):
    pass