from abc import ABC, abstractmethod
import yaml


class AbstractYAML(ABC):

    @abstractmethod
    def read(self, data: str):
        pass


class PlainYAML(AbstractYAML):

    def read(self, data: str):
        pass


class JsonYAML(AbstractYAML):

    def read(self, data: str):
        result = yaml.load(data, yaml.Loader)
        return result
