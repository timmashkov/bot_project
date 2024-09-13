from config import settings
from domains.user.message_handlers import UserActionRouter
from infractructure.server import Server

running_bot = Server(
    token=settings.TOKEN,
    logging_config=settings.LOG_LEVEL,
    start_callbacks=[UserActionRouter.register_handlers],
)
