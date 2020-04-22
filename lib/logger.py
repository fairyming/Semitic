import sys
import logging
import time
import os

from lib.enums import CUSTOM_LOGGING

log_path = 'logs'
if os.path.isdir(log_path) is not True:
    os.mkdir(log_path, 0o755)


filename = time.strftime('%Y-%m-%d', time.localtime(time.time())) + ".log"
logfile = os.path.join(log_path, filename)

logging.addLevelName(CUSTOM_LOGGING.SYSINFO, "*")
logging.addLevelName(CUSTOM_LOGGING.SUCCESS, "+")
logging.addLevelName(CUSTOM_LOGGING.ERROR, "-")
logging.addLevelName(CUSTOM_LOGGING.WARNING, "!")
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s \tFile \"%(filename)s\"[line:%(lineno)d] %(levelname)s %(message)s',
                    filename=logfile,
                    filemode='a')

LOGGER = logging.getLogger("Semitic")

LOGGER_HANDLER = None
try:
    from thirdparty.ansistrm.ansistrm import ColorizingStreamHandler

    disableColor = False

    for argument in sys.argv:
        if "disable-col" in argument:
            disableColor = True
            break

    if disableColor:
        LOGGER_HANDLER = logging.StreamHandler(sys.stdout)
    else:
        LOGGER_HANDLER = ColorizingStreamHandler(sys.stdout)
        LOGGER_HANDLER.level_map[logging.getLevelName(
            "*")] = (None, "cyan", False)
        LOGGER_HANDLER.level_map[logging.getLevelName(
            "+")] = (None, "green", False)
        LOGGER_HANDLER.level_map[logging.getLevelName(
            "-")] = (None, "red", False)
        LOGGER_HANDLER.level_map[logging.getLevelName("!")] = (
            None, "yellow", False)
except ImportError:
    LOGGER_HANDLER = logging.StreamHandler(sys.stdout)

FORMATTER = logging.Formatter(
    "\r[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S")

LOGGER_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(LOGGER_HANDLER)
