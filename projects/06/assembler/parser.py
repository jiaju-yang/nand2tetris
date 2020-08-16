from enum import Enum, auto
from .symbols import SymbolTable
from . import code


class Parser:
    def __init__(self, code_text):
        commands = []
        labels = {}
        for line in code_text.splitlines():
            formatted = line.replace(' ', '')
            if not formatted or formatted.startswith('/'):
                continue
            if formatted.startswith('('):
                label = formatted[1:-1]
                address = len(commands)
                if label in labels:
                    raise ValueError(
                        'Duplicated label: "{}", at line {}!'.format(label, address))
                labels[label] = address
            else:
                commands.append(formatted.split('//', 1)[0])
        self.commands = commands

        symbols = SymbolTable()
        symbols.add_labels(labels)
        self.symbols = symbols

    def parse_command(self, command_str, line):
        if command_str.startswith('@'):
            value = command_str[1:]
            try:
                return format(int(value), '016b')
            except ValueError:
                symbol = value
                if not self.symbols.contains(symbol):
                    self.symbols.add_symbol(symbol)
                return self.symbols.address(symbol)

        if '=' in command_str and ';' in command_str:
            dest, comp, jump = command_str.replace('=', ';').split(';')
        elif '=' in command_str:
            dest, comp = command_str.split('=')
            jump = 'null'
        elif ';' in command_str:
            comp, jump = command_str.split(';')
            dest = 'null'
        try:
            return '111{}{}{}'.format(
                code.comp(comp),
                code.dest(dest),
                code.jump(jump)
            )
        except KeyError:
            raise ValueError(
                'Unknown instruction: "{}" at line {}!'.format(command_str, line))

    def __iter__(self):
        return ParserIterator(self)


class Command:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    class Type(Enum):
        A_COMMAND = auto()
        C_COMMAND = auto()


class ParserIterator:
    def __init__(self, parser, start=0):
        self.parser = parser
        self.current = start

    def __next__(self):
        if self.current < len(self.parser.commands):
            next_line = self.parser.commands[self.current]
            command = self.parser.parse_command(next_line, self.current)
            self.current += 1
            return command
        raise StopIteration()
