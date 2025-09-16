from .logger2 import Logme

logme = Logme('log.log', 'main')
logger = logme.create()

def logger_decorator(func):
    def inner(*args, **kwargs):
        log = logger.getChild(func.__name__)
        
        args_list = []
        kwargs_list = []

        for arg in args:
            msg = "{0}".format(arg)
            print('msg', msg)
            args_list.append(msg)

        for k, v in kwargs.items():
            msg = "{0}={1}".format(k, v)
            print('msg', msg)
            kwargs_list.append(msg)

        args_msg = ", ".join(args_list)
        kwargs_msg = ", ".join(kwargs_list)

        log.info(args_msg + " / " + kwargs_msg)
        func(*args, **kwargs)
    return inner