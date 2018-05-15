import os
import sys
import argparse

#  surprise Totoro
#    _____
#   /     \\
#   vvvvvvv  /|__/|
#      I   /O,O   |
#      I /_____   |      /|/|
#     J|/^ ^ ^ \  |    /00  |    _//|
#      |^ ^ ^ ^ |W|   |/^^\ |   /oo |
#       \m___m__|_|    \m_m_|   \mm_|


def parse_command_line():
    parser = argparse.ArgumentParser(prog='Re_namer', formatter_class=argparse.RawDescriptionHelpFormatter,
        description=
'''  _______    __   ____                                            
 /_  __/ |  / /  / __ \___        ____  ____ _____ ___  ___  _____
  / /  | | / /  / /_/ / _ \______/ __ \/ __ `/ __ `__ \/ _ \/ ___/
 / /   | |/ /  / _, _/  __/_____/ / / / /_/ / / / / / /  __/ /    
/_/    |___/  /_/ |_|\___/     /_/ /_/\__,_/_/ /_/ /_/\___/_/

Description:    
    This script is to be utilised to rename a season of a tv series so that it 
    can be detected and properly parsed by the kodi media manager.''')
    parser.add_argument('--season', '-s', action='store', help='Season of show', type=int, default=0)
    parser.add_argument('--left', '-l', action='store', help='Cut from left', type=int, default=0)
    parser.add_argument('--right', '-r', action='store', help='Cut from right', type=int, default=0)
    parser.add_argument('--ending', '-e', action='store', help='Type of files to select (e.g mkv, mp4)', type=str, required=True)
    args_parsed = parser.parse_args()
    return str(args_parsed.season), args_parsed.ending, args_parsed.left, args_parsed.right


def change_file_names(file_list, season, left_offset, right_offset, file_ending):
    """alters file names and prints old and new to screen"""
    names = []
    for count, old_name in enumerate(file_list, 1):

        # if count is greater than nine don't place 0 in front
        ep_str = "e" if count > 9 else "e0"

        new_name = str(count) + " - " + old_name[left_offset:(len(old_name) - right_offset)].replace('_', ' ') + "_s0" + season + ep_str \
               + str(count) + "." + file_ending

        print(old_name + " <-> " + new_name)
        names.append(new_name)

    return names


def commit_name_change(file_list, new_names, cwd):
    """ Takes old names of files sorted and mapping to new names of files"""
    for x in range(0, len(new_names)):
        print(file_list[x] + " <-> " + new_names[x])
        os.rename(cwd + "\\" + file_list[x], cwd + "\\" + new_names[x])


def yes_or_no(message='Enter y/n: '):
    while True:
        y_or_n = raw_input(message)
        if y_or_n is 'y':
            dire = True
            break
        elif y_or_n is 'n':
            dire = False
            break
        else:
            print('not a valid option')
    return dire


def main():
    try:
        # variables
        file_list = []
        cwd = os.getcwd()
        file_ending = ''
        left_offset = 0
        right_offset = 0
        season = 0

        args_passed = len(sys.argv) > 1

        print("Welcome to TV Re-namer")
        # TODO: be able to set current working directory, maybe by command line
        print("Current working dir: " + cwd)

        # if args npt passed get user input
        if not args_passed:
            file_ending = raw_input("Please enter the type of file to use (e.g mkv, mp4): ")
        else:
            season, file_ending, left_offset, right_offset = parse_command_line()

        # gets only those that have ending matching file_ending
        for _file in os.listdir(cwd):
            if _file.endswith(file_ending):
                file_list.append(_file)

        file_list.sort()

        # prints list of file that will be renamed
        if not args_passed:
            print("The files you have selected are:")
            for _file in file_list:
                print(_file)

        # get season from user if not passed
        if season is 0:
            while True and not args_passed:
                try:
                    season = str(int(raw_input("Enter season number: ")))
                    break
                except ValueError:
                    print("Please enter an integer")

        while True:

            while True and not args_passed:
                try:
                    left_offset = int(raw_input("characters to remove from left: "))
                    right_offset = int(raw_input("characters to remove from right: "))
                    break
                except ValueError:
                    print("please enter a numerical numbers only")

            # returns list of names after they have been renamed
            new_names = change_file_names(file_list, season, left_offset, right_offset, file_ending)

            print("Do you want to replace names")
            if yes_or_no():
                if yes_or_no("Are you sure?\nEnter y/n: "):
                    commit_name_change(file_list, new_names, cwd)
                    raw_input("Re-naming complete press any key to continue... ")
                    sys.exit(0)

            # on second pass when args have been past let them enter left right from command line
            args_passed = False
    except:
        pass


if __name__ == "__main__":
    main()
