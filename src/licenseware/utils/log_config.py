"""

Docs: 
https://github.com/Delgan/loguru


Basic functionality:

from loguru import logger

logger.debug("Debug log")
logger.info("Ingo log")
logger.success("Success log")
logger.warning("Warning log")
logger.error("Error log")
logger.critical("Critical log")

try:
    raise Exception("Demo exception")
except:
    logger.exception("Exception log")
    logger.trace("Trace log")


datetime | level | module_name:function_name:line - message

2021-05-27 10:00:35.276 | DEBUG    | m1:testm1:8 - Debug log
2021-05-27 10:00:35.277 | INFO     | m1:testm1:9 - Ingo log
2021-05-27 10:00:35.277 | SUCCESS  | m1:testm1:10 - Success log
2021-05-27 10:00:35.277 | WARNING  | m1:testm1:11 - Warning log
2021-05-27 10:00:35.278 | ERROR    | m1:testm1:12 - Error log
2021-05-27 10:00:35.278 | CRITICAL | m1:testm1:13 - Critical log
2021-05-27 10:00:35.278 | ERROR    | m1:testm1:18 - Exception log
Traceback (most recent call last):

  File "main.py", line 30, in <module>
    testm1()
    └ <function testm1 at 0x7f1ece69db80>

> File "/home/acmt/Documents/licenseware-sdk/logs/m1.py", line 16, in testm1
    raise Exception("Demo exception")

Exception: Demo exception


To see log colors in docker logs add the following in docker-compose file:

tty: true
environment:
    - 'TERM=xterm-256color'


"""

import os
from loguru import logger as log


debug = os.getenv('DEBUG') == 'true'
log_level = 'INFO' if debug else 'WARNING'
log_format = """<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | 

Module:<cyan>{name}</cyan>
Function:<cyan>{function}</cyan>
Line:<cyan>{line}</cyan>

{level}:
<level>{message}</level>

"""

log.add(
    "app.log", 
    rotation="monthly", 
    level=log_level, 
    format=log_format
)

