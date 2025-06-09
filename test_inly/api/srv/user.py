from fastapi import APIRouter, Depends, Request

from repository.user import UserRepository
from auth.middleware import srv_auth
from schemas.user import UserUpdate

router = APIRouter(
    prefix="/user",
    tags=["user"],
)



@router.patch("/")
@srv_auth()
async def patch_user(
    request: Request,
    user_id: int,
    user_update: UserUpdate,
    user_repository: UserRepository = Depends(),
):
    return await user_repository.update(user_update=user_update, user_id=user_id)


@router.patch("/")
@srv_auth()
async def ban_unban(
    request: Request,
    user_id: int,
    user_update: UserUpdate,
    user_repository: UserRepository = Depends(),
):
    return await user_repository.update(user_update=user_update, user_id=user_id)

