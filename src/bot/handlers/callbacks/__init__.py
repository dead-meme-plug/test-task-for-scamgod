from .admin import router as admin_router
from .digest import router as digest_router
from .subscribe import router as subscribe_router

router = admin_router
router.include_router(digest_router)
router.include_router(subscribe_router)