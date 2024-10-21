
from typing import Optional
from pydantic import BaseModel

class Roles(BaseModel):     
    roles: list[str]

class InviteUserToOrg(BaseModel):
    inviter_name: str
    invitee_email: str
    roles: Optional[list[str]] = None


class AddRolesToUser(Roles):
    pass

class RemoveRolesFromUser(Roles):
    pass

