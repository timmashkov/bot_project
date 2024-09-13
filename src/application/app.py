from config import settings
from infractructure.server import Server

running_bot = Server(
    token=settings.TOKEN,
    logging_config=settings.LOG_LEVEL,
)
