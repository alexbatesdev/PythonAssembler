import argparse
from commands import Comment, MOVW, MOVT, ADD, LDR, ORR, STR, SUB, B, BL, BX
from data_structures import CommandList, Command
from helper import strip_commas, strip_parenthesis


def main():
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("--debug", action="store_true", help="Activate debug mode")
    script_arguments = parser.parse_args()

    if script_arguments.debug:
        print("Debug mode is on")
    else:
        print("Debug mode is off")

    # Return None, or a list of binary values in 2 byte chunks
    methods = {
        "^^": Comment,
        "MOVW": MOVW,
        "MOVT": MOVT,
        "ADD": ADD,
        "LDR": LDR,
        "ORR": ORR,
        "STR": STR,
        "SUB": SUB,
        "B": B,
        "BL": BL,
        "BX": BX,
    }

    instruction_set = CommandList()

    path = "input.txt"
    # path_input = input("Enter the path of the input file (./input.txt): ")
    # if path_input != "":
    #     path = path_input

    with open(path, "r") as input_file:
        for line in input_file:
            if line == "\n":
                continue

            label = None
            if ":3" in line and ":3c" not in line:
                label = line.split(":3")[1].replace("\n", "").strip()
                line = line.split(":3")[0]

            split_line = strip_parenthesis(strip_commas(line)).split()

            if "#" in split_line[0]:
                condition = split_line[0].split("#")[1]
                command = split_line[1]
                args = split_line[2:]
            else:
                condition = "AL"
                command = split_line[0]
                args = split_line[1:]

            try:
                instruction_object = methods[command](
                    args, condition=condition, label=label
                )
                if (
                    instruction_object is not None
                    and instruction_object.__class__.__name__ != "Comment"
                ):
                    instruction_set.append(instruction_object)
                    instruction_set.print()
                    input("Press Enter to continue...")
                else:
                    print("Command not found")
                    continue
                if script_arguments.debug:
                    # print(line.replace("\n", ""))
                    # print(split_line)
                    # print(condition)
                    # print(command)
                    # print(args)
                    if label is not None:
                        print(label)
                    # print(instruction_object)
                    # print(instruction_object.toBinary())
                    # print(instruction_set)
                    # input("Press Enter to continue...")
            except KeyError:
                print("Command not found")
                continue
            except Exception as e:
                print(e)
                continue

    path = "output.txt"
    # path_output = input("Enter the output path of the file (./output.txt): ")
    # if path_output != "":
    #     path = path_output

    with open(path, "wb") as output_file:
        input("Press Enter to continue to binary")
        binary_values = instruction_set.toBinary()
        print("Binary values: ")
        print(binary_values)
        input("Press Enter to continue...")
        byte_array = bytes([int(b, 2) for b in binary_values])
        output_file.write(byte_array)
        output_file.close()


def FindOffset():
    pass


if __name__ == "__main__":
    main()


# This bit swaps the bits for the raspberry pi
# if temp_data is not None:
#     if type(temp_data) == list:
#         for i in temp_data[::-1]:
#             output.append(i)
#         print(" ".join(temp_data))
#     else:
#         print(temp_data)