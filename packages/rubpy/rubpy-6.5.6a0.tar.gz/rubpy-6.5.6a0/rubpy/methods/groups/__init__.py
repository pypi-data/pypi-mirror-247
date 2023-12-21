from .add_group import AddGroup
from .add_group_members import AddGroupMembers
from .ban_group_member import BanGroupMember
from .create_group_voice_chat import CreateGroupVoiceChat
from .delete_no_access_group_chat import DeleteNoAccessGroupChat
from .edit_group_info import EditGroupInfo
from .get_banned_group_members import GetBannedGroupMembers
from .get_group_admin_access_list import GetGroupAdminAccessList
from .get_group_info import GetGroupInfo


class Groups(
    AddGroup,
    AddGroupMembers,
    BanGroupMember,
    CreateGroupVoiceChat,
    DeleteNoAccessGroupChat,
    EditGroupInfo,
    GetBannedGroupMembers,
    GetGroupAdminAccessList,
    GetGroupInfo,
):
    pass