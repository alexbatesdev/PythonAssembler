from commands import (
    Comment,
    MOVW,
    MOVT,
    ADD,
    LDR,
    ORR,
    STR,
    SUB,
    B,
    BX,
    BlockDataTransfer,
)
from data_structures import CommandList
from helper import strip_commas, strip_parenthesis


def main():
    methods = {
        "^^": Comment,
        "MOVW": MOVW,
        "MOVT": MOVT,
        "LDR": LDR,
        "STR": STR,
        "LDM": BlockDataTransfer,
        "STM": BlockDataTransfer,
        "ORR": ORR,
        "ADD": ADD,
        "SUB": SUB,
        "BX": BX,
        "B": B,
    }

    instruction_set = CommandList()

    path = "test.txt"
    path_input = input(f"Enter the path of the input file (./{path}): ")
    if path_input != "":
        path = path_input

    with open(path, "r") as input_file:
        for line in input_file:
            if line == "\n":
                continue

            label = None
            if ":3" in line and ":3c" not in line:
                label = line.split(":3")[1].replace("\n", "").strip()
                line = line.split(":3")[0]

            split_line = strip_parenthesis(strip_commas(line)).split()

            # Iterate through the methods dictionary to find the correct command
            for command in methods.keys():
                if command in split_line[0]:
                    break

            args = split_line
            try:
                instruction_object = methods[command](args, label=label)
                if (
                    instruction_object is not None
                    and instruction_object.__class__.__name__ != "Comment"
                ):
                    instruction_set.append(instruction_object)
                    print(instruction_object)
                elif instruction_object.__class__.__name__ == "Comment":
                    instruction_object.toBinary()
                else:
                    print("Command not found")
                    continue
            except KeyError:
                print("Command not found")
                continue
            except Exception as e:
                print(e)
                continue

    path = "output.txt"
    path_output = input("Enter the output path of the file (./output.txt): ")
    if path_output != "":
        path = path_output

    with open(path, "wb") as output_file:
        input("Press Enter to continue to binary")
        binary_values = instruction_set.toBinary()
        print("Binary values: ")
        print(binary_values)
        input("Press Enter to continue...")
        byte_array = bytes([int(b, 2) for b in binary_values])
        output_file.write(byte_array)
        output_file.close()


if __name__ == "__main__":
    main()
