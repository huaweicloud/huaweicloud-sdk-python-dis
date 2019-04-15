#!/usr/bin/python
# -*- coding:utf-8 -*-
import logging
def log(message, level='',filename=''):
    logger = logging.getLogger()
    if level=='info':
        logger.setLevel(logging.INFO)
    elif level=='debug':
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARNING)
    if filename:
        ch = logging.FileHandler(filename)
    else:
        ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    if level == 'info':
        logger.info(message)
    elif level == 'debug':
        logger.debug(message)
    else:
        logger.warning(message)
    logger.removeHandler(ch)
    return logger


