from helper import (
    resolve_register,
    find_label,
    resolve_address_mode,
    resolve_register_list,
)
from data_structures import Command


class Comment(Command):
    def toBinary(self):
        print("Comment: " + " ".join(self.args))
        return []


class MOVW(Command):
    def toBinary(self):
        register = resolve_register(self.args[1])
        value = self.args[2]
        if value[0:2] == "0x":
            value = value[2:]
        binary_value = bin(int(value, 16)).replace("0b", "").zfill(16)
        imm4 = binary_value[0:4]
        imm12 = binary_value[4:]
        output = [
            self.condition + "0011",
            "0000" + imm4,
            register + imm12[0:4],
            imm12[4:12],
        ]
        return output

    def getEncoding(self):
        return "[condition][0011][0000][imm4][Rd][imm12]"


class MOVT(Command):
    def toBinary(self):
        register = resolve_register(self.args[1])
        value = self.args[2]
        if value[0:2] == "0x":
            value = value[2:]
        binary_value = bin(int(value, 16)).replace("0b", "").zfill(16)
        imm4 = binary_value[0:4]
        imm12 = binary_value[4:]
        output = [
            self.condition + "0011",
            "0100" + imm4,
            register + imm12[0:4],
            imm12[4:14],
        ]
        return output

    def getEncoding(self):
        return "[condition][0011][0100][imm4][Rd][imm12]"


class SingleDataProcess(Command):
    def toBinary(self, opCode):
        special = "0"
        if self.args[1] == "S":
            special = "1"
            register = resolve_register(self.args[2])
            register2 = resolve_register(self.args[3])
            value = self.args[4]
        else:
            register = resolve_register(self.args[1])
            register2 = resolve_register(self.args[2])
            value = self.args[3]

        immediate = "0"
        if value[0:2] == "0x":
            value = value[2:]
            immediate = "1"
        elif value[0] == "R":
            immediate = "0"
            value = value.replace("R", "")
        else:
            value = value
            immediate = "1"

        binary_value = bin(int(value, 16)).replace("0b", "").zfill(12)
        output = [
            (self.condition + "00" + immediate + opCode[0]),
            (opCode[1:] + special + register2),
            register + binary_value[0:4],
            binary_value[4:12],
        ]
        return output

    def getEncoding(self):
        return "[condition][00][I][opcode][S][Rn][Rd][Operand2]"


class ADD(SingleDataProcess):
    def toBinary(self):
        return super().toBinary("0100")


class SUB(SingleDataProcess):
    def toBinary(self):
        return super().toBinary("0010")


class ORR(SingleDataProcess):
    def toBinary(self):
        return super().toBinary("1100")


# Page 26 - ARM instruction set
class SingleDataTransfer(Command):
    def toBinary(self):
        b_bit = "0"
        load, pre_post, up_down = resolve_address_mode(self.args[0])
        destination_register = self.args[1]
        write_back = "0"
        if "!" in destination_register:
            write_back = "1"
            destination_register = destination_register.replace("!", "")
        destination_register = resolve_register(destination_register)
        base_register = self.args[2]
        if "!" in base_register:
            write_back = "1"
            base_register = base_register.replace("!", "")
        base_register = resolve_register(base_register)

        immediate = "0"

        if len(self.args) > 3:
            if self.args[3][0:2] == "0x":
                offset = self.args[3][2:]
            else:
                immediate = "1"
                offset = self.args[3].replace("R", "")
            offset = bin(int(self.args[3], 16)).replace("0b", "").zfill(12)
        else:
            offset = "0" * 12

        output = [
            (self.condition + "01" + immediate + pre_post),
            (up_down + b_bit + write_back + load + base_register),
            (destination_register + offset[0:4]),
            (offset[4:12]),
        ]
        return output

    def getEncoding(self):
        return "[condition][01][I][P][U][B][W][L][Rn][Rd][Offset12]"


# page 37 - ARM instruction set
class BlockDataTransfer(Command):
    def __init__(self, args, label=None):
        super().__init__(args, label)
        self.load = "0"

    def toBinary(self):
        s = "0"
        self.load, pre_post, up_down = resolve_address_mode(self.args[0])
        base_register = self.args[1]

        write_back = ""
        if "!" in base_register:
            write_back = "1"
            base_register = base_register.replace("!", "")
        else:
            write_back = "0"

        base_register = resolve_register(base_register)

        register_list = resolve_register_list(self.args[2:])
        output = [
            self.condition + "100" + pre_post,
            up_down + s + write_back + self.load + base_register,
            register_list[0:8],
            register_list[8:16],
        ]
        return output

    def getEncoding(self):
        return "[condition][100][P][U][S][W][L][Rn][RegisterList]"


class Branch(Command):
    def __init__(self, args, label=None):
        super().__init__(args, label)
        self.offset = None
        self.target_label = None
        self.link = "0"
        if args[0][:2] == "BL":
            self.link = "1"

        if "0x" in args[1]:
            self.offset = bin(int(args[1], 16)).replace("0b", "").zfill(24)
        elif args[1] != ":3c":
            raise SyntaxError(
                "Branch must have a label gremlin to measure the offset, or a pre measured hexadecimal offset."
            )
        else:
            self.target_label = args[2]

    def toBinary(self):
        if self.offset is None and self.target_label is not None:
            self.offset = find_label(self)
        output = [
            (self.condition + "101" + self.link),
            self.offset[0:8],
            self.offset[8:16],
            self.offset[16:24],
        ]
        return output

    def getEncoding(self):
        return "[condition][101][L][Offset24]"


class BX(Command):
    def toBinary(self):
        if len(self.args) > 1:
            register = resolve_register(self.args[1])
        else:
            register = resolve_register("R14")

        output = [
            self.condition + "0001",
            "0010" + "1111",
            "1111" + "1111",
            "0001" + register,
        ]
        return output

    def getEncoding(self):
        return "[condition][0001][0010][1111][1111][1111][0001][Rn]"
