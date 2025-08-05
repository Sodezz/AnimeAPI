import sys
from loguru import logger

logger.remove()

logger.add(
    sys.stderr,
    level="WARNING",
    format="<green>{time}</green> | <level> {level} </level> | <cyan> {name} </cyan>: <cyan> {function} </cyan>: <cyan> {line} </cyan> - <level> {message} </level>",
    colorize=True,
)

logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time}</green> | <level> {level} </level> | <cyan> {name} </cyan>: <cyan> {function} </cyan>: <cyan> {line} </cyan> - <level> {message} </level>",
    colorize=True,
)

logger.add(
    sys.stdout,
    level="DEBUG",
    format="<blue>{time}</blue> | <level> {level} </level> | <cyan> {name} </cyan>: <cyan> {function} </cyan>: <cyan> {line} </cyan> - <level> {message} </level>",
    colorize=True,
)
