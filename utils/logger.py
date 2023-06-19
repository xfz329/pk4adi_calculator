import logging
import logging.config
from pathlib import Path
import os, sys

BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)

LOG_PATH = os.path.join(BASE_DIR,'log')
print(LOG_PATH)
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)
DEBUG_FILE = os.path.join(LOG_PATH,'debug.log')
WARN_FILE = os.path.join(LOG_PATH,'warn.log')
INFO_FILE = os.path.join(LOG_PATH,'info.log')
FILES = [DEBUG_FILE, WARN_FILE, INFO_FILE]

for f in FILES:
    if not os.path.exists(f):
        if str(sys.platform).startswith('win'):
            with open(f, 'a+') as fp:
                fp.close()
        else:
            os.mknod(f)


config = {
    'version' : 1,
    'disable_existing_loggers' : False,
    'formatters': {
        'verbose': {
            'format': "{levelname} {asctime} {module}:{funcName}:{lineno} - {process:d} {thread:d} {message}",
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters' : {
    },
    'handlers': {
        'console' : {
            'level' : 'INFO',
            'class' : 'logging.StreamHandler',
            'formatter' : 'simple',
        },
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'log/debug.log'),
            'formatter' : 'verbose',
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 10,
            'encoding': 'utf-8',
        },
        'info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'log/info.log'),
            'formatter' : 'verbose',
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 10,
            'encoding': 'utf-8',
        },
        'warn': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'log/warn.log'),
            'formatter' : 'verbose',
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 10,
            'encoding': 'utf-8',
        },
    },
    'loggers' : {
        'pk_gui' : {
            'handlers' : ['console', 'debug','info','warn'],
            'level' : 'DEBUG',
        }
    }
}
class Logger:
    def __init__(self,logger_name="pk_gui"):
        logging.config.dictConfig(config)
        self.__logger=logging.getLogger(logger_name)

    def get_logger(self):
        return self.__logger

if __name__ == "__main__":
    t=Logger('pk_gui').get_logger()
    t.debug("debug")
    t.info("info")
    t.warning("warning")
    t.error("error")