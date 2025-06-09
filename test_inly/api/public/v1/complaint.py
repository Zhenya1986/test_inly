from requests import Response
from fastapi import APIRouter, Depends, status, Response, Request, HTTPException
from schemas.complaint import ComplaintIn, ComplaintOut
from repository.complaint import ComplaintRepository

router = APIRouter(
    prefix="/complaint",
    tags=["complaint"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_complaint(
    complaint_data: ComplaintIn, complaint_repository: ComplaintRepository = Depends()
):
    return await complaint_repository.create_complaint(complaint_data)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_complaint(
    request: Request,
    complaint_id: int, complaint_repository: ComplaintRepository = Depends()
):
    complaint = await complaint_repository.get(complaint_id)

    current_user_id = request.state.user.id
    if complaint.user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await complaint_repository.del_complaint(complaint_id=complaint_id)
