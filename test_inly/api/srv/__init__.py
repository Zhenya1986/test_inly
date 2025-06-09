from api.srv.user import router as srv_router
from api.srv.comment import router as srv_router_comment
from api.srv.complaint import router as srv_router_complaint
from fastapi import APIRouter


router = APIRouter(prefix='/api/srv')

router.include_router(srv_router)
router.include_router(srv_router_comment)
router.include_router(srv_router_complaint)
