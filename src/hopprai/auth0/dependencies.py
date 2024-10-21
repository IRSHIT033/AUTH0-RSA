from typing import List

from fastapi import Depends, HTTPException, Request,status

from hopprai.auth0.service import get_user_roles_inside_org
from hopprai.core.util import decode_access_token


class RoleChecker:
    def __init__(self, required_roles: List[str]):
        self.required_roles = required_roles

    def __call__(self,request:Request, current_user: any=Depends(decode_access_token) ):
        
        user_id=current_user.get("sub")
        org_id=current_user.get("org_id")
        
        # Check if the user belongs to the organization which is
        if org_id != request.path_params.get("org_id"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="You are not authorized to access this organization"
            )
        
        user_roles=get_user_roles_inside_org(user_id, org_id)
        
        if not any(role["name"] in self.required_roles for role in user_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="You are not authorized to access this resource"
            )
        
        return True
        
        

