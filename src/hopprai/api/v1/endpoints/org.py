from fastapi import Depends
from hopprai.auth0.dependencies import RoleChecker
from hopprai.auth0.service import get_users_of_org,invite_user_to_org,remove_roles_from_user,add_roles_to_user,remove_user_from_org
from hopprai.model.schemas.org import AddRolesToUser, InviteUserToOrg, RemoveRolesFromUser
from fastapi import APIRouter


router = APIRouter(
    prefix="/orgs",
    tags=["orgs"]
)

@router.get("/{org_id}")
async def get_org_details(
    org_id: str,
    _=Depends(RoleChecker(required_roles=["admin"]))
):
    return {
        "message": "You are authorized to access this resource"
    }

@router.get("/{org_id}/members")
async def get_members(
    org_id: str,
    page: int = 0,
    per_page: int = 50,  
):
    return get_users_of_org(org_id, per_page,page)

@router.post("/{org_id}/invitations")
async def invite_user(
    org_id: str,
    invite_user: InviteUserToOrg,
    _=Depends(RoleChecker(required_roles=["admin"]))
):
    return invite_user_to_org(invite_user.inviter_name, invite_user.invitee_email, org_id)

@router.delete("/{org_id}/members/{user_id}")
async def remove_user(
    org_id: str,
    user_id: str,
    _=Depends(RoleChecker(required_roles=["admin"]))
):
    return remove_user_from_org(user_id, org_id)

@router.post("/{org_id}/members/{user_id}/roles")
async def add_roles(
    org_id: str,
    user_id: str,
    add_roles: AddRolesToUser,
    _=Depends(RoleChecker(required_roles=["admin"]))
):
    return add_roles_to_user(user_id, org_id, add_roles.roles)

@router.delete("/{org_id}/members/{user_id}/roles")
async def remove_roles(
    org_id: str,
    user_id: str,
    remove_roles: RemoveRolesFromUser,
):
    return remove_roles_from_user(user_id, org_id, remove_roles.roles)

