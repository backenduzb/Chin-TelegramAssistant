from handlers.admin.auto_m import router as auto_m_router
from handlers.commands.story import router as story_router
from handlers.start import router as start_router
from handlers.users.message import router as message_router

ROUTERS = [
    auto_m_router,
    story_router,
    start_router,
    message_router
]
