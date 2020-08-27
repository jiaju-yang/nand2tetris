import sys
from translator.parser import Parser


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
    parser = Parser(source_code, filename.split('/')[-1])
    assemble_code = [command.assembly_code() for command in parser]
    write_to_file('\n'.join(assemble_code), f'{filename}.asm')
