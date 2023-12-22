def to_string(matrix: list[list[float]]):
    if len(matrix) == 0:
        return "[]"
    final = str(matrix[0])
    for i in range(1, len(matrix)):
        final += f'\n{matrix[i]}'
    return final


def side_by_side_string(matrix: list[list[float]],
                        other: list[list[float]],
                        middle="") -> str:
    final = ""
    i = 0
    mid = max(len(matrix), len(other)) // 2
    tabl = (len(middle) + 1) * "‎ " if len(middle) > 0 else ""
    while i < min(len(matrix), len(other)):
        for j in range(2):
            if j % 2 == 0:
                if i == mid:
                    final += str(matrix[i]) + middle + " "
                else:
                    final += str(matrix[i]) + tabl + " "
            else:
                if i == mid:
                    final += str(other[i]) + "\n"
                else:
                    final += str(other[i]) + "\n"
        i += 1
    if len(matrix) > len(other):
        for leftover in matrix[i:]:
            final += str(leftover) + "\n"
    elif len(other) > len(matrix):
        for leftover in other[i:]:
            tab = "‎ " * (len(matrix[0]) + 2 + (len(matrix[0]) - 1)*2 + len(matrix[0]) * 2)
            final += tab + tabl + str(leftover)
    return final


def list_from_string(list_str: str) -> list[float]:
    if "," in list_str:
        return [float(s_num) for s_num in list_str.split(", ")]
    else:
        return [float(s_num) for s_num in list_str.split()]


def cmd_help(menu2):
    print("=======================================")
    print("What do you want to do?")
    print("\tCreate matrix: 'create'\n\tDeterminant: 'det'\n\t"
          "Transpose: 'trans'\n\t"
          "Invert: 'invert'\n\tAdd other matrix: 'add'"
          "\n\tRestart: 'restart'\n\tHelp: 'help'"
          "\n\tClear screen: 'clear'"
          "\n\tShow matrices: 'show [FLAG]'\n\t\tMain: 'm' or '-m'"
          "\n\tExit: 'exit'") \
        if menu2 is None else print("\n\t"
                                    "Back to main matrix: 'back'\n\t"
                                    "Addition: 'madd'\n\t"
                                    "Subtraction: 'sub'\n\t"
                                    "Dot product: 'dot'\n\t"
                                    "Cross product: 'cross'\n\t"
                                    "Switch matrix order: 'switch'\n\t"
                                    "Clear screen: 'clear'\n\t"
                                    "Show matrices: 'show [FLAG]'\n\t\tMain: 'm' or '-m'\n\t\tOther: 'o' or '-o'\n\t\tBoth: 'b' or '-b'\n\t"
                                    "Exit: 'exit'\n\tHelp: 'help'\n\t"
                                    "Restart: 'restart'")
    print("=======================================")


def help_setup():
    print("\t==========================================================")
    print("\t\tPlease enter your matrix row by row.")
    print("\t\tMake sure each row has the same number of elements.")
    print("\t\tFollow the following formats:")
    print("\t\tFormat 1:\n\t\t\tEnter row: 1, 2, 3, 4\n\n\t\tFormat 2:\n"
          "\t\t\tEnter row: 1 2 3 4\n")
    print("\t\tWhen done, input 'done' or press Enter key. (Not case sensitive)")
    print("\t==========================================================")


if __name__ == "__main__":
    m = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
    o = [[7, 7], [8, 8], [9, 9]]
    print(side_by_side_string(m, o, " is"))

