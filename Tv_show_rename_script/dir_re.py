import os
import sys
import argparse


def change_file_names(file_list, season, left_offset, right_offset, file_ending):
    """alters file names and prints old and new to screen"""
    names = []
    for count, old_name in enumerate(file_list, 1):

        # if count is greater than nine don't place 0 in front
        ep_str = "e" if count > 9 else "e0"

        new_name = str(count) + " - " + old_name[left_offset:(len(old_name) - right_offset)] + "_s0" + season + ep_str \
               + str(count) + "." + file_ending

        print(old_name + " <-> " + new_name)
        names.append(new_name)

    return names


def commit_name_change(file_list, new_names, cwd):
    """ Takes old names of files sorted and mapping to new names of files"""
    for x in range(0, len(new_names)):
        print(file_list[x] + " <-> " + new_names[x])
        os.rename(cwd + "\\" + file_list[x], cwd + "\\" + new_names[x])


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

    # TODO: fix
    # if not len(sys.argv) is 0:
    #     for arg in sys.argv:
    #         pass

    while True:
        yes_1 = ""
        yes_2 = ""

        while True:
            try:
                left_offset = int(raw_input("Enter number of characters from left to remove:"))
                right_offset = int(raw_input("Enter number of characters from right to remove:"))
                season = str(int(raw_input("Enter season number:")))
                break
            except ValueError:
                print("please enter a numerical numbers only")

        # returns list of names after they have been renamed
        new_names = change_file_names(file_list, season, left_offset, right_offset, file_ending)

        print("Do you want to replace names")
        yes_1 = raw_input("Enter y/n: ")

        if yes_1 == "y":
            yes_2 = raw_input("Are you sure?,\nEnter y/n: ")
            if yes_2 == "y":
                commit_name_change(file_list, new_names, cwd)
                raw_input("Re-naming complete press any key to continue... ")
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
