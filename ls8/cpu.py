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
        self.run_codes = {  # Branch table - long lost cusion of Webster
            0b10100000: self.ADD,
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b00000001: self.HLT,
            0b10100010: self.MUL,
            0b01000101: self.PUSH,
            0b01000110: self.POP,
            0b01010000: self.CALL,
            0b00010001: self.RET,
        }
        self.sp = self.reg[7] = 0xF4  # Stack Pointer
        # self.reg.append(0b11110100)  # F4 in binary, used for sp
        # self.sp = 0xF4

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

    def load(self, filename):
        """Load a program into memory."""
        if len(sys.argv) != 2:
            print("Sorry, please try again")
            sys.exit()

        filename = sys.argv[1]

        try:
            address = 0
            with open(filename, "r") as file:
                for line in file:
                    # Get rid of Commentary
                    split_line = line.split("#")[0]

                    # Strip spaces
                    command = split_line.strip()

                    # If everything works - continue on
                    if command == "":
                        continue

                    # Convert command from string to binary
                    instruction = int(command, 2)

                    # Import & load the commands into RAM?
                    self.ram[address] = instruction

                    # Incrament the address to avoide continually loading the program
                    address += 1

        except Exception:
            print(
                f"""\nAn Error Occoured:\n\
            The file was not found: {filename}
            Check the filepath and spelling.\n"""
            )
            sys.exit()

    def alu(self, op, reg_a, reg_b):
        """ALU operations. arithmetic logic unit"""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] += -self.reg[reg_b]
        elif op == "MUL":
            product = self.reg[reg_a] * self.reg[reg_b]
            self.reg[reg_a] = product
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

        while self.running:
            IR = self.ram_read(self.pc)  # Instruction Register
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR in self.run_codes:
                self.run_codes[IR](operand_a, operand_b)

            else:
                print("That command doesn't exist")
                self.running = False

    def HLT(self, operand_a, operand_b):
        self.running = False

    def PRN(self, operand_a, operand_b):
        # opA is the reg index to print
        print(self.reg[operand_a])
        self.pc += 2

    def LDI(self, operand_a, operand_b):
        # opA is the value, opB is the value to set
        self.reg[operand_a] = operand_b
        self.pc += 3

    def ADD(self, operand_a, operand_b):
        self.alu("ADD", operand_a, operand_b)
        self.pc += 3

    def SUB(self, operand_a, operand_b):
        self.alu("SUB", operand_a, operand_b)
        self.pc += 3

    def MUL(self, operand_a, operand_b):  # Multiply the next two
        self.alu("MUL", operand_a, operand_b)
        self.pc += 3

    def POP(self, operand_a, operand_b):
        value = self.ram[self.sp]  # What to store
        self.reg[operand_a] = value  # Where to store it
        self.sp += 1
        self.pc += 2

    def PUSH(self, operand_a, operand_b):
        """Push onto the stack"""
        self.sp += -1  # -=
        self.ram[self.sp] = self.reg[operand_a]
        self.pc += 2

    def CALL(self, operand_a, operand_b):
        next_funct_addr = self.pc + 2
        self.PUSH_ANY(next_funct_addr)
        self.pc = self.reg[operand_a]

    def PUSH_ANY(self, value):
        self.sp += -1
        self.ram[self.sp] = value

    def RET(self, operand_a, operand_b):
        """Pop val from stack to pc"""
        self.pc = self.ram[self.sp]
        self.sp += 1


###############################################
# Run with `python3 ls8.py examples/call.ls8` #
###############################################
