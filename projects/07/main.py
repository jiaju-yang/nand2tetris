import sys
import os
from translator.parser import Parser
from translator.command import bootstrap_code


def read_file_text(file):
    with open(file, 'r') as f:
        return f.read()


def write_to_file(text, file):
    with open(file, 'w') as f:
        f.write(text)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError('Argument error! e.g. "python main.py filename"')

    filepath = os.path.abspath(sys.argv[-1])
    if os.path.isfile(filepath) and filepath.endswith('.vm'):
        source_code_files = [filepath]
        target_path, filename = filepath.rsplit('.', 1)[0].rsplit('/', 1)
        target_file = os.path.join(target_path, filename+'.asm')
    elif os.path.isdir(filepath):
        source_code_files = []
        for file in os.listdir(filepath):
            file = os.path.join(filepath, file)
            if file.endswith('.vm'):
                if file.endswith('Sys.vm'):
                    source_code_files.insert(0, file)
                else:
                    source_code_files.append(file)
        filename = filepath.rsplit('/', 1)[1]
        target_file = os.path.join(filepath, filename+'.asm')
    else:
        raise ValueError('Unsupported file type: {}!'.format(filepath))
    
    assemble_code = []
    for source_code_file in source_code_files:
        source_code = read_file_text(source_code_file)
        parser = Parser(source_code, source_code_file.rsplit('/', 1)[1].rsplit('.', 1)[0])
        assemble_code.extend([command.assembly_code() for command in parser])
    extra_code = list(bootstrap_code)
    extra_code.extend(assemble_code)
    write_to_file('\n'.join(extra_code), target_file)
