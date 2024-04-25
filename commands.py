from helper import resolve_condition, resolve_register, strip_parenthesis


def Comment(args: list):
    print("Comment: " + " ".join(args))
    return


def MOVW(args: list):
    condition = args[0]
    register = resolve_register(args[1])
    value = args[2]
    if value[0:2] == "0x":
        value = value[2:]
    binary_value = bin(int(value, 16)).replace("0b", "").zfill(16)
    imm4 = binary_value[0:4]
    imm12 = binary_value[4:]
    output = [
        (resolve_condition(condition) + "0011"),
        "0000" + imm4,
        register + imm12[0:4],
        imm12[4:12],
    ]
    return output


def MOVT(args: list):
    condition = args[0]
    register = resolve_register(args[1])
    value = args[2]
    if value[0:2] == "0x":
        value = value[2:]
    binary_value = bin(int(value, 16)).replace("0b", "").zfill(16)
    imm4 = binary_value[0:4]
    imm12 = binary_value[4:]
    output = [
        (resolve_condition(condition) + "0011"),
        "0100" + imm4,
        register + imm12[0:4],
        imm12[4:14],
    ]
    return output


def SingleDataProcess(opCode: str, args: list):
    condition = resolve_condition(args[0])
    special = "0"
    if args[1] == "S":
        special = "1"
        register = resolve_register(args[2])
        register2 = resolve_register(args[3])
        value = args[4]
    else:
        register = resolve_register(args[1])
        register2 = resolve_register(args[2])
        value = args[3]

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
        (condition + "00" + immediate + opCode[0]),
        (opCode[1:] + special + register2),
        register + binary_value[0:4],
        binary_value[4:12],
    ]
    return output


def ADD(args: list):
    return SingleDataProcess("0100", args)


def SingleDataTransfer(l: str, args: list):
    condition = resolve_condition(args[0])
    register = resolve_register(args[1])
    value = resolve_register(args[2])
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
        (condition + "01" + immediate + p),
        (u + b + w + l + value),
        (register + offset[0:4]),
        (offset[4:12]),
    ]
    return output


def LDR(args: list):
    return SingleDataTransfer("1", args)


def ORR(args: list):
    return SingleDataProcess("1100", args)


def STR(args: list):
    return SingleDataTransfer("0", args)


def SUB(args: list):
    return SingleDataProcess("0010", args)


def Branch(link: str, args: list):
    condition = resolve_condition(args[0])
    offset = bin(int(args[1], 16)).replace("0b", "").zfill(24)
    output = [
        (condition + "101" + link),
        offset[0:8],
        offset[8:16],
        offset[16:24],
    ]
    return output


def B(args: list):
    return Branch("0", args)


def BL(args: list):
    return Branch("1", args)


def BX(args: list):
    condition = resolve_condition(args[0])
