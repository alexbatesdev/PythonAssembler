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
            raise Exception("Invalid condition")


def resolve_register(register: str):
    return (bin(int(register.replace("R", "")))).replace("0b", "").zfill(4)


def strip_parenthesis(string: str):
    return string.replace("(", "").replace(")", "")


def strip_commas(string: str):
    return string.replace(",", "")


def reverse_list(list: list):
    return list[::-1]
