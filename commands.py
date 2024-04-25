from helper import resolve_condition, resolve_register, strip_parenthesis

# TODO: Decrement all the args indexes by 1 because of the condition
# being removed from the args list


class Command:
    def __init__(self, args, condition="AL"):
        self.condition = condition
        self.args = args

    def toBinary(self):
        raise NotImplementedError("Subclasses should implement this method.")


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
            (resolve_condition(self.condition) + "0011"),
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
            (resolve_condition(self.condition) + "0011"),
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


class SingleDataTransfer(Command):
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

        # Values for the future
        p = "0"
        u = "0"
        b = "0"
        w = "0"
        offset = "000000000000"

        output = [
            (self.condition + "01" + immediate + p),
            (u + b + w + load + value),
            (register + offset[0:4]),
            (offset[4:12]),
        ]
        return output


class LDR(SingleDataTransfer):
    def toBinary(self):
        return super().toBinary("1")


class STR(SingleDataTransfer):
    def toBinary(self):
        return super().toBinary("0")


class Branch(Command):
    def toBinary(self, link):
        offset = bin(int(self.args[1], 16)).replace("0b", "").zfill(24)
        output = [
            (self.condition + "101" + link),
            offset[0:8],
            offset[8:16],
            offset[16:24],
        ]
        return output


class B(Branch):
    def toBinary(self):
        return super().toBinary("0")


class BL(Branch):
    def toBinary(self):
        return super().toBinary("1")


class BX(Command):
    def toBinary(self):
        register = resolve_register(self.args[1])
        output = [
            (self.condition + "00010010"),
            "0000" + register,
            "000000000000",
        ]
        return output
