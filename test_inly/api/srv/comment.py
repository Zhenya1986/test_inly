from fastapi import APIRouter, Depends, status, Request
from auth.middleware import srv_auth
from repository.comments import CommentRepository

router = APIRouter(
    prefix="/comment",
    tags=["comment"],
)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
@srv_auth()
async def delete_comment(
    request: Request,
    comment_id: int, comment_repository: CommentRepository = Depends()
):
    await comment_repository.del_comment(comment_id=comment_id)