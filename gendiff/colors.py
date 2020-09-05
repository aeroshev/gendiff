"""
Этот модуль содержит в себе класс с кодами
цветов
"""


class Colors:
    """
    Содержит в себе коды цветов
    для окраски текста отчёта
    """
    INSERT = '\033[92m'
    UPDATE = '\033[93m'
    DELETE = '\033[91m'
    SIMPLE = '\033[37m'

    @staticmethod
    def flush() -> str:
        """
        Сброс цветов вывода
        :return: default settings
        """
        return '\033[0m'
