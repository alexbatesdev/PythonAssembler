from helper import resolve_register, find_label
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
    def __init__(
        self,
        args,
        condition="AL",
        label=None,
        p_bit="0",
        u_bit="0",
        b_bit="0",
        w_bit="0",
        offset="000000000000",
    ):
        super().__init__(args, label)
        self.p_bit = p_bit
        self.u_bit = u_bit
        self.b_bit = b_bit
        self.w_bit = w_bit
        self.offset = offset

    def toBinary(self, load):
        register = resolve_register(self.args[1])
        value = resolve_register(self.args[2])
        immediate = "0"
        if value[0:2] == "0x":
            value = value[2:]
            immediate = "1"
        elif value[0] == "R":
            immediate = "0"
            value = value.replace("R", "")

        output = [
            (self.condition + "01" + immediate + self.p_bit),
            (self.u_bit + self.b_bit + self.w_bit + load + value),
            (register + self.offset[0:4]),
            (self.offset[4:12]),
        ]
        return output


class LDR(SingleDataTransfer):
    def toBinary(self):
        return super().toBinary("1")


class STR(SingleDataTransfer):
    def toBinary(self):
        return super().toBinary("0")


# page 37 - ARM instruction set
class BlockDataTransfer(Command):
    def __init__(self, args, condition="AL", label=None):
        super().__init__(args, label)
        raise NotImplementedError("BlockDataTransfer is not implemented yet.")

    def toBinary(self, load):
        raise NotImplementedError("BlockDataTransfer is not implemented yet.")


class STM(BlockDataTransfer):
    def toBinary(self):
        return super().toBinary("0")


class LDM(BlockDataTransfer):
    def toBinary(self):
        return super().toBinary("1")


class Branch(Command):
    def __init__(self, args, link, label=None):
        super().__init__(args, label)
        self.offset = None
        self.target_label = None
        self.link = link
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


class B(Branch):
    def __init__(self, args, label=None):
        if "L" in args[1]:
            link = "1"
        else:
            link = "0"
        super().__init__(args, link, label)

    def toBinary(self):
        return super().toBinary()


class BX(Command):
    def toBinary(self):
        print(self.args)
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
