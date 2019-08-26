#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" 
Декораторы и логгирование
"""
import logging



def createLogger(file="main.log"):
    log = logging.getLogger("DecLogger")
    log.setLevel(logging.INFO)
    fh = logging.FileHandler(file) 
    fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    log.addHandler(fh)
    return log
    

def try_exept_dekorator(name, text):
    """ 
    Декоратор try_exept. Нужен для отказа от повторений кода с отловом ошибок
    """
    def dekorator(function):
        def wrapper(*args, **kwargs):
            try:
                rez = function(*args, **kwargs)
                return rez
            except Exception as error:
                raise Exception(name + ", " + function.__name__ + ": " +
                                 text + " " +  str(error) + "\n" +
                                 str(args)) from None
        return wrapper
    return dekorator


def try_exept_pyqt_dekorator(log, name, text):
    """ 
    Декоратор try_exept. Нужен для отказа от повторений кода с отловом ошибок
    """
    def dekorator(function):
        def wrapper(*args, **kwargs):
            try:
                rez = function(*args, **kwargs)
                return rez
            except Exception as error:
                message = name + ", " + function.__name__ + ": " + text + \
                " " +  str(error) + "\n" + str(args)
                log.exception(message)
                print(message)
        return wrapper
    return dekorator

def logger_dekorator(log, name, text):
    """ 
    Декоратор логгирования
    """
    def dekorator(function):
        def wrapper(*args, **kwargs):
            rez = function(*args, **kwargs)
            message = name + ": " + text + ": " + str(args)
            log.info(message)
            return rez
        return wrapper
    return dekorator
# x = 0
# if x==0:
#     raise Exception("qwe")
# else:
#     print(1)