default_variable_table = {
    'SP': '0000000000000000',
    'LCL': '0000000000000001',
    'ARG': '0000000000000010',
    'THIS': '0000000000000011',
    'THAT': '0000000000000100',
    'R0': '0000000000000000',
    'R1': '0000000000000001',
    'R2': '0000000000000010',
    'R3': '0000000000000011',
    'R4': '0000000000000100',
    'R5': '0000000000000101',
    'R6': '0000000000000110',
    'R7': '0000000000000111',
    'R8': '0000000000001000',
    'R9': '0000000000001001',
    'R10': '0000000000001010',
    'R11': '0000000000001011',
    'R12': '0000000000001100',
    'R13': '0000000000001101',
    'R14': '0000000000001110',
    'R15': '0000000000001111',
    'SCREEN': '0100000000000000',
    'KBD': '0110000000000000'
}


class SymbolTable:
    def __init__(self, start_position=16):
        self.new_symbol_address = start_position
        self.symbols = dict(default_variable_table)

    def add_labels(self, labels):
        for label, address in labels.items():
            self.symbols[label] = format(address, '016b')

    def add_symbol(self, symbol):
        self.symbols[symbol] = format(self.new_symbol_address, '016b')
        self.new_symbol_address += 1

    def contains(self, symbol):
        return symbol in self.symbols

    def address(self, symbol):
        return self.symbols[symbol]
