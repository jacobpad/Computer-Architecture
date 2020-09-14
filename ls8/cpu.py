"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8  # Variables for cpu to use with instructions
        self.ram = [None] * 256  # Memory
        self.pc = 0  # Pointer to track operations in register
        self.running = True

    def ram_read(self, MAR):
        """
        MAR = Memory Address Register
        Value at ram address
        """
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        """
        MDR = Memory Data Register
        Write over a specified address in ram
        """
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] += -self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print(
            f"TRACE: %02X | %02X %02X %02X |"
            % (
                self.pc,
                # self.fl,
                # self.ie,
                self.ram_read(self.pc),
                self.ram_read(self.pc + 1),
                self.ram_read(self.pc + 2),
            ),
            end="",
        )

        for i in range(8):
            print(" %02X" % self.reg[i], end="")

        print()

    def run(self):
        """Run the CPU."""
        """
        10000010 # LDI R0,8
        00000000
        00001000
        01000111 # PRN R0
        00000000
        00000001 # HLT
        """
        # These are instructions we need to translate
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001

        while self.running:
            IR = self.ram[self.pc]  # Instruction Register
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if IR == HLT:
                self.running = False

            elif IR == LDI:  # Set the value of a register to an integer
                self.ram_write(self.pc + 1, operand_b)
                self.reg[self.pc] = operand_b
                self.pc += 3

            elif IR == PRN:  # Print value stored at register
                print(self.reg[operand_a])
                self.pc += 2

