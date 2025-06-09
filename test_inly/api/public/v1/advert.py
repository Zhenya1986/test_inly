from schemas.advert import AdvertIn, AdvertOut

from fastapi import APIRouter, HTTPException, Depends, status, Query, Request
from repository.advert import AdvertRepository, AdvertType


router = APIRouter(
    prefix="/advert",
    tags=["advert"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_advert(
    advert_data: AdvertIn, advert_repository: AdvertRepository = Depends()
):
    advert = await advert_repository.create_advert(
        title=advert_data.title,
        description=advert_data.description,
        advert_type=advert_data.type,
        user_id=advert_data.user_id,
        is_active=advert_data.is_active,
    )

    return advert


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_advert(
    request: Request,
    advert_id: int,
    advert_repository: AdvertRepository = Depends(),
):
    advert = await advert_repository.get(advert_id)
    if not advert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Advert not found"
        )
    current_user_id = request.state.user.id
    # TODO: перенести вы сервесный слой, так как проект маленький не стал городить
    if advert.user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await advert_repository.delete_advert(advert_id=advert_id)


@router.get("/", response_model=list[AdvertOut], status_code=status.HTTP_200_OK)
async def get_all_advert(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=10),
    advert_type: AdvertType = Query(None),
    is_active: bool = Query(True),
    advert_repository: AdvertRepository = Depends(),
):
    return await advert_repository.get_list_advert(
        offset=offset, limit=limit, advert_type=advert_type, is_active=is_active
    )


@router.get("/{advert_id}", status_code=status.HTTP_200_OK)
async def get_advert(advert_id: int, advert_repository: AdvertRepository = Depends()):
    advert = await advert_repository.get(advert_id)
    if not advert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Advert not found"
        )
    return advert
