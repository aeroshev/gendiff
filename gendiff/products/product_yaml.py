from abc import ABC, abstractmethod
import yaml
from jsondiff import diff
from colorama import init, Fore


class AbstractYAML(ABC):

    def read(self, data: str):
        return yaml.load(data, yaml.Loader)

    def compare(self, input_1_yaml, input_2_yaml):
        return diff(input_1_yaml, input_2_yaml, syntax='symmetric')

    @abstractmethod
    def render(self, result):
        pass


class PlainYAML(AbstractYAML):

    def render(self, result):
        pass


class JsonYAML(AbstractYAML):

    def __init__(self):
        self.color = Fore.WHITE
        self.deep = 0
        init()

    def render(self, result):
        status = {'$insert', '$update', '$delete'}

        for key, value in result.items():
            if str(key) in status:
                if str(key) == '$insert':
                    if isinstance(value, list):
                        self.deep += 1
                        for item in value:
                            print(self.deep * ' ' + f'{Fore.GREEN}+ {item[1]}')
                        self.deep -= 1
                elif str(key) == '$delete':
                    if isinstance(value, list):
                        self.deep += 1
                        for item in value:
                            print(self.deep * ' ' + f'{Fore.RED}- {item[1]}')
                        self.deep -= 1
            else:
                if isinstance(value, list):
                    print(self.deep * ' ' + f'{Fore.RED}- {key}: {value[0]}')
                    print(self.deep * ' ' + f'{Fore.GREEN}+ {key}: {value[1]}')
                elif isinstance(value, dict):
                    print(self.deep * ' ' + f'{Fore.WHITE}{key}:')
                    self.deep += 1
                    self.render(value)
                    self.deep -= 1

                else:
                    if self.color == 'green':
                        print(self.deep * ' ' + f'{Fore.GREEN}+ {key}: {value}')
                    elif self.color == 'red':
                        print(self.deep * ' ' + f'{Fore.RED}- {key}: {value}')
        print(Fore.WHITE, end='')
