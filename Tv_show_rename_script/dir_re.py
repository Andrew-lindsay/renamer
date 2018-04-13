import os
import sys
import time
# variables
file_list  = []
count = 0
cwd = os.getcwd()
file_ending = ""
left_offset = 0
right_offset = 0

def rm_underscore(str1):
    str2 = str1[0:len(str1) -12]
    str_out = ""
    for ch in str2:
        if ch == '_':
            str_out = str_out + " "
        else:
            str_out = str_out + ch
    str_out = str_out + str1[len(str1) -12 : len(str1)]
    return str_out

# script starts here 
print("Welcome to the renamer")
print("Current working dir: " + cwd)

file_ending = raw_input("Please enter the type of file to use (e.g mkv, mp4):")

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
    yes_1 = ""
    yes_2 = "" 
    left_offset = raw_input("Enter number of characters from left to remove:")
    right_offset = raw_input("Enter number of characters from right to remove:")
    season = raw_input("Enter season number:")
    count = 0
    names = []

    for t in file_list:
        name = file_list[count]
        if (count + 1 > 9 ) :
            name = str(count + 1) + " - " + name[int(left_offset):(len(name)-int(right_offset))] + "_s0" + season + "e" + str(count + 1) + "." + file_ending
            
        else:
            name = str(count + 1) + " - " + name[int(left_offset):(len(name)-int(right_offset))] + "_s0" + season + "e0" + str(count + 1) + "." + file_ending
        print( t + " <-> " + name)
        names.append(name)  
        print("")
        count += 1

    print("Do you want to replace names")
    yes_1 = raw_input("Enter y/n: ")

    if yes_1 == "y":
        yes_2 = raw_input("Are you sure?,\nEnter y/n: ")

        if yes_2 == "y":
            for x in range(0,len(names)):
                print( file_list[x] + " <-> " + names[x])
                os.rename(cwd + "\\"+ file_list[x], cwd + "\\"+ names[x])
            sys.exit(0)
        else:
            continue
    else:
        _exit = raw_input("exit or continue: ")
        if _exit == "exit":
            sys.exit(0)
        else:
            continue
            
   
            

        
#for t in list1:
#    name = list1[count]
#    name = name[0:len(name)-7] + name[len(name)-6:len(name)]
#    print( t + " <-> " + name)
#    print()
##    os.rename(cwd + "\\"+ t,cwd + "\\"+ name  ) 
#    count += 1 
    
