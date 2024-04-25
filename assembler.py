import argparse
from commands import Comment, MOVW, MOVT, ADD, LDR, ORR, STR, SUB, B, BL
from helper import strip_commas, strip_parenthesis


def main():
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("--debug", action="store_true", help="Activate debug mode")
    args = parser.parse_args()

    if args.debug:
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
    }

    output = []

    path = "input.txt"
    # path_input = input("Enter the path of the input file (./input.txt): ")
    # if path_input != "":
    #     path = path_input

    with open(path, "r") as input_file:
        for line in input_file:
            # print(line.replace("\n", ""))
            split_line = strip_parenthesis(strip_commas(line)).split()
            # print(split_line)
            command = split_line[0]
            # print(command)
            args = split_line[1:]
            # print(args)
            try:
                temp_data = methods[command](args)
                # print(command, args)
                if temp_data is not None:
                    if type(temp_data) == list:
                        for i in temp_data[::-1]:
                            output.append(i)
                        print(" ".join(temp_data))
                    else:
                        print(temp_data)
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
        binary_values = output
        byte_array = bytes([int(b, 2) for b in binary_values])
        output_file.write(byte_array)
        output_file.close()


if __name__ == "__main__":
    main()
