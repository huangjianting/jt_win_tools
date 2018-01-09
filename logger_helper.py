# coding: utf-8
import logging
import sys
import os
import time
from logging import Logger
from logging.handlers import TimedRotatingFileHandler
from app_core.common.func import check_dir
import uuid


def init_logger(logger_name):
    check_dir('log')
    if logger_name not in Logger.manager.loggerDict:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        # handler all
        handler = TimedRotatingFileHandler('./log/all.log', when='midnight', backupCount=7)
        # handler = TimedRotatingFileHandler('./log/all.log', when='S',backupCount=7)
        # datefmt = "%Y-%m-%d %H:%M:%S,%f"
        # format_str = "[%(asctime)s]: %(name)s %(levelname)s %(lineno)s %(message)s"
        # format_str = '[%(asctime)-15s]: <%(name)s> %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
        format_str = '[%(asctime)-15s]: <%(name)s> %(levelname)s %(message)s'
        formatter = logging.Formatter(format_str)
        handler.setFormatter(formatter)
        # handler.setLevel(logging.DEBUG)
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)
        # handler error
        handler = TimedRotatingFileHandler('./log/error.log', when='midnight',backupCount=7)
        # datefmt = "%Y-%m-%d %H:%M:%S"
        format_str = '[%(asctime)-15s]: <%(name)s> %(levelname)s %(message)s'
        formatter = logging.Formatter(format_str)
        handler.setFormatter(formatter)
        handler.setLevel(logging.ERROR)
        logger.addHandler(handler)

    logger = logging.getLogger(logger_name)
    return logger


class LoggerRunner(object):

    def __init__(self, logger_name):
        self.logger_instance = init_logger(logger_name)

    def info(self, msg, msg_id=None):
        return self.say_log(self.logger_instance.info, msg, msg_id)

    def error(self, msg, msg_id=None):
        return self.say_log(self.logger_instance.error, msg, msg_id)

    def debug(self, msg, msg_id=None):
        return self.say_log(self.logger_instance.debug, msg, msg_id)

    def warning(self, msg, msg_id=None):
        return self.say_log(self.logger_instance.warning, msg, msg_id)

    def critical(self, msg, msg_id=None):
        return self.say_log(self.logger_instance.critical, msg, msg_id)

    def say_log(self, func, msg, msg_id):
        this_detail_trace = self.detail_trace()
        if msg_id is None:
            msg_id = uuid.uuid1()
        func("[%s], msg_id: %s, message: %s" % (this_detail_trace, msg_id, msg))
        return msg_id

    @staticmethod
    def detail_trace():
        u"""
        获取调用堆栈详情
        :return: 
        """
        ret_str = ""
        f = sys._getframe()
        f = f.f_back  # first frame is detailtrace, ignore it
        while hasattr(f, "f_code"):
            co = f.f_code
            ret_str = "%s(%s:%s)->" % (
                os.path.basename(co.co_filename),
                co.co_name,
                f.f_lineno) + ret_str
            f = f.f_back
        return ret_str[:-2]

logger_runner = LoggerRunner("windows_gazer")
# log_instance = init_logger('windows_gazer_instance')


if __name__ == '__main__':
    import time
    logger02 = init_logger('test')
    logger02.error("test-error")
    # time.sleep(1)
    logger02.info("test-info")
    # time.sleep(1)
    logger02.warn("test-warn")
    # time.sleep(1)
    # logger02.error("test-error")
    # time.sleep(1)
    # logger02.info("test-info")
    # time.sleep(1)
    # logger02.warn("test-warn")
    # time.sleep(1)
    # logger02.error("test-error")
    # time.sleep(1)
    # logger02.info("test-info")
    # time.sleep(1)
    # logger02.warn("test-warn")
    # time.sleep(1)
    # logger02.error("test-error")
    # time.sleep(1)
    # logger02.info("test-info")
    # time.sleep(1)
    # logger02.warn("test-warn")
    # time.sleep(1)
    # logger02.error("test-error")
    # time.sleep(1)
    # logger02.info("test-info")
    # time.sleep(1)
    # logger02.warn("test-warn")
    logger_runner.info('test1')
    logger_runner.warning('test2')
    logger_runner.error('test3')