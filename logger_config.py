import logging
from colorama import Fore, Style


class ColoredFilter(logging.Filter):
    def filter(self, record):
        if record.levelno == logging.INFO:
            record.msg = Fore.GREEN + record.msg + Style.RESET_ALL
            return True
        elif record.levelno == logging.WARNING:
            record.msg = Fore.YELLOW + record.msg + Style.RESET_ALL
            return True
        elif record.levelno == logging.ERROR:
            record.msg = Fore.RED + record.msg + Style.RESET_ALL
            return True
        return False


logging.basicConfig(
    format=f'{Style.BRIGHT}%(asctime)s %(message)s{Style.RESET_ALL}',
    datefmt='%d.%m.%Y %H:%M:%S',
    level=logging.INFO,
)

logger = logging.getLogger('')
logger.addFilter(ColoredFilter())
logger.setLevel(logging.INFO)
