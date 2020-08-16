import sys
from assembler.parser import Parser
from assembler.symbols import SymbolTable


def read_file_text(file):
    with open(file, 'r') as f:
        return f.read()


def write_to_file(text, file):
    with open(file, 'w') as f:
        f.write(text)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError('Argument error! e.g. "python main.py filename"')

    filename, _ = sys.argv[-1].rsplit('.', 1)

    source_code = read_file_text(sys.argv[-1])
    parser = Parser(source_code)
    binary_code = [command for command in parser]
    write_to_file('\n'.join(binary_code), f'{filename}.hack')
