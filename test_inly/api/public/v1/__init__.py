from fastapi import APIRouter
from api.public.v1.comment import router as comment_router
from api.public.v1.advert import router as advert_router
from api.public.v1.user import router as reg_router
from api.public.v1.complaint import router as complaint_router

router = APIRouter(prefix='/v1')

router.include_router(comment_router)
router.include_router(advert_router)
router.include_router(reg_router)
router.include_router(complaint_router)

