import logging
from log_server import config

format_str: str = (
    '%(asctime)s - %(name)s - %(levelname)s - [Line: %(lineno)d] - %(message)s'
)
logging.basicConfig(
    format=format_str,
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)
socket_handler = logging.handlers.SocketHandler(
    config.SERVER_ENV['LOCAL_IP'], 
    int(
        config.SERVER_ENV['SERVER_PORT']
    )
)
logger.addHandler(socket_handler)
