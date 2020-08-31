from abc import ABC, abstractmethod


class AbstractProduct(ABC):

    @abstractmethod
    def read(self, data: str) -> dict:
        """
        :param data:
        :return:
        """

    @abstractmethod
    def compare(self, input_1: dict, input_2: dict) -> set:
        """
        :param input_1:
        :param input_2:
        :return:
        """

    @abstractmethod
    def render(self, result: set) -> None:
        """
        :param result:
        :return:
        """