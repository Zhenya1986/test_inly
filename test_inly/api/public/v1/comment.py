from requests import Response
from fastapi import APIRouter, Depends, status, Response, Request, HTTPException
from schemas.comment import CommentIn
from repository.comments import CommentRepository

router = APIRouter(
    prefix="/comment",
    tags=["comment"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_comment(
    comment_data: CommentIn, comment_repository: CommentRepository = Depends()
):
    await comment_repository.create_comment(comment_data)
    return Response(content="Comment created")


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    request: Request,
    comment_id: int, comment_repository: CommentRepository = Depends()
):
    comment = await comment_repository.get(comment_id)

    current_user_id = request.state.user.id
    if comment.user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await comment_repository.del_comment(comment_id=comment_id)
