import os
import logging

class Logme:
    def __init__(self, fn: str = 'process.log', root_logger_name: str = 'my_logger'):
        self.fn = os.path.join('logs', fn)
        self.root_logger_name = root_logger_name
        self._is_initialized = False

    def create(self):
        """
        Создание основного логгера и добавление к нему обработчиков.
        Дочерние логгеры будут наследовать обработчики через propagate.
        """
        logger = logging.getLogger(self.root_logger_name)
        logger.setLevel(logging.DEBUG)

        if not logger.handlers:
            os.makedirs(os.path.dirname(self.fn), exist_ok=True)

            file_handler = logging.FileHandler(self.fn)
            file_handler.setLevel(logging.DEBUG)

            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)

            logger.addHandler(file_handler)

        self._is_initialized = True
        return logger

    def get_logger(self, permalink: str):
        """
        Возвращает дочерний логгер (по сути, namespace под основным логгером).
        Обработчики не добавляются, но propagate=True позволяет использовать обработчики родителя.
        """
        if not self._is_initialized:
            raise RuntimeError("Logger not initialized. Call create() first.")

        logger = logging.getLogger(f"{self.root_logger_name}.{permalink}")
        logger.setLevel(logging.DEBUG)
        logger.propagate = True  # Лог передаётся родителю
        return logger


# import os
# import logging
# import inspect



# class Logme:

#     def __init__(self, fn:str = 'process.log'):
#         self.fn = os.path.join('logs', fn)
#         self.logger = None


#     def get_logger(self, permalink):
#         # current_function = inspect.stack()[1].function
#         self.logger = logging.getLogger(f"my_logger.{permalink}")
#         self.logger.setLevel(logging.DEBUG)
#         self.logger.propagate = True  # ← Передаёт сообщения родителю
#         return self.logger


#     def create(self, name:str='my_logger'):
#         # Создание логгера
#         self.logger = logging.getLogger(name)
#         self.logger.setLevel(logging.DEBUG)  # Уровень логирования: DEBUG, INFO, WARNING, ERROR, CRITICAL

#         # Проверяем, чтобы не добавлять обработчики повторно при импортах
#         if not self.logger.handlers:

#             # Создание обработчика для записи в файл
#             file_handler = logging.FileHandler(self.fn)
#             file_handler.setLevel(logging.DEBUG)

#             # Формат логирования
#             formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#             file_handler.setFormatter(formatter)

#             # Добавление обработчика к логгеру
#             self.logger.addHandler(file_handler)
#         return self.logger
        