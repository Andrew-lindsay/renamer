import os
import sys


def change_file_names(file_list, season, left_offset, right_offset, file_ending):
    """alters file names and prints old and new to screen"""
    names = []
    for count, old_name in enumerate(file_list, 1):

        # if count is
        ep_str = "e" if count > 9 else "e0"

        new_name = str(count) + " - " + old_name[int(left_offset):(len(old_name) - int(right_offset))] + "_s0" + season + ep_str \
               + str(count) + "." + file_ending

        print(old_name + " <-> " + new_name)
        names.append(new_name)
        print("")

    return names


def main():
    # variables
    file_list = []
    cwd = os.getcwd()
    file_ending = ""
    left_offset = 0
    right_offset = 0

    # script starts here
    print("Welcome to the re-namer")
    print("Current working dir: " + cwd)

    file_ending = raw_input("Please enter the type of file to use (e.g mkv, mp4): ")

    # gets only those that have ending of file
    for _file in os.listdir(cwd):
        if _file.endswith(file_ending):
            file_list.append(_file)

    # sort into order
    file_list.sort()

    # prints list of file that will be renamed
    print("The files you have selected are:")
    for _file in file_list:
        print(_file)

    while True:
        # TODO: add command line arg code

        yes_1 = ""
        yes_2 = ""
        left_offset = raw_input("Enter number of characters from left to remove:")
        right_offset = raw_input("Enter number of characters from right to remove:")
        season = raw_input("Enter season number:")
        count = 0
        names = []

        # returns list of names after they have been renamed
        new_names = change_file_names(file_list, season, left_offset, right_offset, file_ending)

        print("Do you want to replace names")
        yes_1 = raw_input("Enter y/n: ")

        if yes_1 == "y":
            yes_2 = raw_input("Are you sure?,\nEnter y/n: ")

            if yes_2 == "y":
                for x in range(0, len(new_names)):
                    print(file_list[x] + " <-> " + new_names[x])
                    os.rename(cwd + "\\" + file_list[x], cwd + "\\" + new_names[x])
                sys.exit(0)
            else:
                continue
        else:
            _exit = raw_input("exit or continue: ")
            if _exit == "exit":
                sys.exit(0)
            else:
                continue


if __name__ == "__main__":
    main()