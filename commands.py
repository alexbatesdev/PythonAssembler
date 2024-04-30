from helper import resolve_register
from data_structures import Command


class Comment(Command):
    def toBinary(self):
        print("Comment: " + " ".join(self.args))
        return []


class MOVW(Command):
    def toBinary(self):
        register = resolve_register(self.args[0])
        value = self.args[1]
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
        register = resolve_register(self.args[0])
        value = self.args[1]
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
        if self.args[0] == "S":
            special = "1"
            register = resolve_register(self.args[1])
            register2 = resolve_register(self.args[2])
            value = self.args[3]
        else:
            register = resolve_register(self.args[0])
            register2 = resolve_register(self.args[1])
            value = self.args[2]

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
        register = resolve_register(self.args[0])
        value = resolve_register(self.args[1])
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


# TODO: Fix the label goblin
# He can't properly count offsets


class Branch(Command):
    def __init__(self, args, condition="AL", label=None):
        super().__init__(args, condition, label)
        self.offset = None
        if "0x" in args[0]:
            self.offset = bin(int(args[0], 16)).replace("0b", "").zfill(24)
        elif args[0] != ":3c":
            raise SyntaxError(
                "Branch must have a label gremlin to measure the offset, or a pre measured hexadecimal offset."
            )
        print(self.offset)

    def __find_label__(self):
        label_goblin = self
        label = None
        offset = -2
        print(label_goblin)
        while label_goblin.previous is not None:
            label_goblin = label_goblin.previous
            if label_goblin.__class__.__name__ == "Comment":
                continue
            offset -= 1
            if label_goblin.label == self.offset:
                label = label_goblin.label
                break
            print(label_goblin)
            input("pause")
        if label is None:
            label_goblin = self
            offset = -2
            while label_goblin.next is not None:
                label_goblin = label_goblin.next
                if label_goblin.__class__.__name__ == "Comment":
                    continue
                offset += 1
                if label_goblin.label == self.offset:
                    label = label_goblin.label
                    break
                print(label_goblin)
                input("pause")

        print(offset)
        print(self.__parse_offset__(str(offset)))
        input("HALT")

        if label_goblin.label != self.offset:
            raise SyntaxError("Label not found.")
        return self.__parse_offset__(str(offset))

    def toBinary(self, link):
        if self.offset is None:
            self.offset = self.__find_label__()
        output = [
            (self.condition + "101" + link),
            self.offset[0:8],
            self.offset[8:16],
            self.offset[16:24],
        ]
        print("toBinary")
        return output

    def __parse_offset__(self, offset):
        if offset[0] == "-":
            offset_positive = offset[1:]
            offset_binary = bin(int(offset_positive)).replace("0b", "").zfill(24)
            offset_inverse = "".join(["1" if x == "0" else "0" for x in offset_binary])
            offset = bin(int(offset_inverse, 2) + 1).replace("0b", "").zfill(24)
        else:
            offset = bin(int(offset)).replace("0b", "").zfill(24)
        return offset


class B(Branch):
    def toBinary(self):
        return super().toBinary("0")


class BL(Branch):
    def toBinary(self):
        return super().toBinary("1")


class BX(Command):
    def toBinary(self):
        if len(self.args) > 0:
            register = resolve_register(self.args[0])
        else:
            register = resolve_register("R14")

        output = [
            self.condition + "0001",
            "0010" + "1111",
            "1111" + "1111",
            "0001" + register,
        ]
        return output


if __name__ == "__main__":
    node = Comment(["This is a comment"])
    node.setNext(Comment(["This is another comment"]))
