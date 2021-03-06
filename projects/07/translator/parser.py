from .command import Arithmetic, MemoryAccess, Branch, FunctionDeclare, FunctionReturn, FunctionCall


class Parser:
    def __init__(self, code_text, domain):
        commands_str = []
        for line in code_text.splitlines():
            formatted = line.strip()
            if not formatted or formatted.startswith('/'):
                continue
            formatted = formatted.split('//', 1)[0].strip() # Remove comments after code
            formatted = ' '.join(formatted.split()) # Remove multiple spaces
            commands_str.append(formatted)
        self.commands_str = commands_str
        self.domain = domain

    def parse_command(self, command_str, line):
        instructions = command_str.split(' ')
        if len(instructions) == 1:
            if instructions[0] == 'return':
                return FunctionReturn(instructions, self.domain)
            else:
                return Arithmetic(instructions, self.domain)
        elif len(instructions) == 3:
            if instructions[0] =='function':
                return FunctionDeclare(instructions, self.domain)
            elif instructions[0] =='call':
                return FunctionCall(instructions, self.domain)
            elif instructions[0] in {'push', 'pop'}:
                return MemoryAccess(instructions, self.domain)
        elif len(instructions) == 2:
            return Branch(instructions, self.domain)
        raise ValueError('None supported command: {}'.format(' '.join(instructions)))

    def __iter__(self):
        return ParserIterator(self)


class ParserIterator:
    def __init__(self, parser, start=0):
        self.parser = parser
        self.current = start

    def __next__(self):
        if self.current < len(self.parser.commands_str):
            next_line = self.parser.commands_str[self.current]
            command = self.parser.parse_command(next_line, self.current)
            self.current += 1
            return command
        raise StopIteration()
