from abc import ABC, abstractmethod
from operator import add, sub, neg, eq, gt, lt, and_, or_, not_
import string


class Command(ABC):
    label_count = 0

    def __init__(self, command_str, domain):
        self.command_str = command_str
        self.domain = domain

    @abstractmethod
    def assembly_code(self):
        pass

    @classmethod
    def new_label(cls):
        result = 'AUTOGEN'+str(cls.label_count)
        cls.label_count += 1
        return result


def binary_arithmetic_operator(symbol):
    return '\n'.join(['@SP', 'AM=M-1', 'D=M', '@SP', 'AM=M-1', 'M=M'+symbol+'D', '@SP', 'M=M+1'])


def binary_compare_operator(symbol):
    return '\n'.join(['@SP', 'AM=M-1', 'D=M', '@SP', 'AM=M-1', 'D=M-D', '@{label1}', 'D;'+symbol, '@0', 'D=A', '@{label2}',
                      '0;JMP', '({label1})', 'D=-1', '({label2})', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1'])


def single_operator(symbol):
    return '\n'.join(['@SP', 'AM=M-1', 'M='+symbol+'M', '@SP', 'M=M+1'])


arithmetic_types = {
    'add': binary_arithmetic_operator('+'),
    'sub': binary_arithmetic_operator('-'),
    'neg': single_operator('-'),
    'eq': binary_compare_operator('JEQ'),
    'gt': binary_compare_operator('JGT'),
    'lt': binary_compare_operator('JLT'),
    'and': binary_arithmetic_operator('&'),
    'or': binary_arithmetic_operator('|'),
    'not': single_operator('!'),
}


fmt = string.Formatter()


class Arithmetic(Command):
    def __init__(self, command_str, domain):
        command = command_str[0]
        if command not in arithmetic_types:
            raise ValueError(
                'Unknown arithmetic operation: "{}"!'.format(command))
        self.arithmetic_type = command
        super().__init__(command_str, domain)

    def assembly_code(self):
        assemble = arithmetic_types[self.arithmetic_type]
        labels = {}
        for i, _ in enumerate((field for _, field, _, _ in fmt.parse(assemble)
                              if field and field.startswith('label')), start=1):
            labels['label'+str(i)] = Command.new_label()
        return assemble.format(**labels)+'//'+self.arithmetic_type


def push_local_etc(segment_name):
    return '\n'.join(['@{index}', 'D=A', '@'+segment_name, 'A=D+M', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1'])


def pop_local_etc(segment_name):
    return '\n'.join(['@{index}', 'D=A', '@'+segment_name, 'D=D+M', '@R5', 'M=D', '@SP', 'AM=M-1', 'D=M', '@R5', 'A=M', 'M=D'])


memory_access_combination = {
    'push': {
        'argument': push_local_etc('ARG'),
        'local': push_local_etc('LCL'),
        'static': '\n'.join(['@{domain}.{index}', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']),
        'constant': '\n'.join(['@{index}', 'D=A', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']),
        'this': push_local_etc('THIS'),
        'that': push_local_etc('THAT'),
        'pointer': '\n'.join(['@{this_or_that}', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']),
        'temp': '\n'.join(['@{index}', 'D=A', '@5', 'A=D+A', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1'])
    },
    'pop': {
        'argument': pop_local_etc('ARG'),
        'local': pop_local_etc('LCL'),
        'static': '\n'.join(['@SP', 'AM=M-1', 'D=M', '@{domain}.{index}', 'M=D']),
        'this': pop_local_etc('THIS'),
        'that': pop_local_etc('THAT'),
        'pointer': '\n'.join(['@SP', 'AM=M-1', 'D=M', '@{this_or_that}', 'M=D']),
        'temp': '\n'.join(['@{index}', 'D=A', '@5', 'D=D+A', '@R5', 'M=D', '@SP', 'AM=M-1', 'D=M', '@R5', 'A=M', 'M=D'])
    }
}


class MemoryAccess(Command):
    def __init__(self, command_str, domain):
        access_type, segment, index = command_str
        if access_type not in memory_access_combination or segment not in memory_access_combination[access_type]:
            raise ValueError(
                'Illegal syntax of memory access operation: "{} {} {}"!'.format(access_type, segment, index))
        self.access_type, self.segment, self.index = access_type, segment, index
        if segment == 'pointer':
            self.this_or_that ='THIS' if index == '0' else 'THAT'
        super().__init__(command_str, domain)

    def assembly_code(self):
        assemble = memory_access_combination[self.access_type][self.segment]
        return assemble.format(**{field: getattr(self, field)
                                  for _, field, _, _ in fmt.parse(assemble) if field})+'//'+' '.join([self.access_type, self.segment, str(self.index)])
