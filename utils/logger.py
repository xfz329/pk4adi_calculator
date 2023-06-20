import logging
import logging.config
from utils.dirs import init_log_files

file_dict = init_log_files()

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
            'filename': file_dict.get("debug"),
            'formatter' : 'verbose',
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 10,
            'encoding': 'utf-8',
        },
        'info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': file_dict.get("info"),
            'formatter' : 'verbose',
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 10,
            'encoding': 'utf-8',
        },
        'warn': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': file_dict.get("warn"),
            'formatter' : 'verbose',
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 10,
            'encoding': 'utf-8',
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': file_dict.get("error"),
            'formatter' : 'verbose',
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 10,
            'encoding': 'utf-8',
        },
    },
    'loggers' : {
        'pk_gui' : {
            'handlers' : ['console', 'debug','info','warn', 'error'],
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