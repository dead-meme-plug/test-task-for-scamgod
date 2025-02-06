from .start import router as start_router
from .admin import router as admin_router

router = start_router
router.include_router(admin_router)
