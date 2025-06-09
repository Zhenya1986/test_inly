
from fastapi import APIRouter, Depends, status, Request
from repository.complaint import ComplaintRepository
from auth.middleware import srv_auth

router = APIRouter(
    prefix="/complaint",
    tags=["complaint"],
)

@router.get("/{advert_id}", status_code=status.HTTP_200_OK)
@srv_auth()
async def get_complaint(
    request: Request,
    advert_id: int,
    limit: int = 10,
    is_approved: bool = False,
    complaint_repository: ComplaintRepository = Depends()
):
    return await complaint_repository.get_list_complaint(advert_id=advert_id,limit=limit, is_approved=is_approved)
