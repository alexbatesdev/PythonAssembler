# Helper Functions
def resolve_condition(condition: str):
    match condition:
        case "AL":  # Always
            return "1110"
        case "EQ":
            return "0000"
        case "NE":
            return "0001"
        case "CS":
            return "0010"
        case "CC":
            return "0011"
        case "MI":
            return "0100"
        case "PL":  # Positive or zero
            return "0101"
        case "VS":
            return "0110"
        case "VC":
            return "0111"
        case "HI":
            return "1000"
        case "LS":
            return "1001"
        case "GE":
            return "1010"
        case "LT":
            return "1011"
        case "GT":
            return "1100"
        case "LE":
            return "1101"
        case _:
            return "1110"


def resolve_register(register: str):
    return (bin(int(register.replace("R", "")))).replace("0b", "").zfill(4)


def strip_parenthesis(string: str):
    return string.replace("(", "").replace(")", "")


def strip_commas(string: str):
    return string.replace(",", "")


def reverse_list(list: list):
    return list[::-1]


def parse_offset(offset):
    if offset[0] == "-":
        offset_positive = offset[1:]
        offset_binary = bin(int(offset_positive)).replace("0b", "").zfill(24)
        offset_inverse = "".join(["1" if x == "0" else "0" for x in offset_binary])
        offset = bin(int(offset_inverse, 2) + 1).replace("0b", "").zfill(24)
    else:
        offset = bin(int(offset)).replace("0b", "").zfill(24)
    return offset


def find_label(self):
    label_goblin = self
    label = None
    offset = -2
    while label_goblin.previous is not None:
        label_goblin = label_goblin.previous
        if label_goblin.__class__.__name__ == "Comment":
            continue
        offset -= 1
        if label_goblin.label == self.target_label:
            label = label_goblin.label
            break
    if label is None:
        label_goblin = self
        offset = -2
        while label_goblin.next is not None:
            label_goblin = label_goblin.next
            if label_goblin.__class__.__name__ == "Comment":
                continue
            offset += 1
            if label_goblin.label == self.target_label:
                label = label_goblin.label
                break
    if label is None:
        raise SyntaxError("Label not found.")
    return parse_offset(str(offset))
