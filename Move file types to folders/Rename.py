import os
import shutil
import time

pwd = os.getcwd()

files_in_dir = []

file_type = raw_input('Enter file extension e.g .mkv: ')

lenf = len(file_type)

#for item in os.listdir(pwd):
#    # print(item)
#    # print(item[len(item)-4:])
#    # print(item[len(item)-4:] == ".png")
#    if item[len(item)-lenf:] == file_type:
#        # files_in_dir.append(item[:-4].capitalize())
#        folder = item[:-lenf].capitalize()
#        os.mkdir(folder)
#        shutil.move(os.path.join(pwd, item), os.path.join(pwd, folder))

files_in_dir = os.listdir(pwd)

files_in_dir = map(lambda x: x[:-lenf].capitalize(),
                   filter(lambda x: x[len(x)-lenf:] == file_type,
                          files_in_dir))

print'The following folders will be make in: ', pwd

if len(files_in_dir) == 0:
    print 'No files are present in: ' + pwd + ' with file type: ' + file_type
    
for item in files_in_dir:
    print(item)

str_x = ''
while 1:
    str_x = raw_input('to continue continue/exit enter [y/n]:')
    if str_x == 'y':
        map(lambda x: os.mkdir(x), files_in_dir)
        map(lambda x:  shutil.move(
            os.path.join(pwd, x + file_type),
            os.path.join(pwd, x)), files_in_dir)
        print 'Files have been moved to created folders'
        break
    elif str_x == 'n':
        break
    
time.sleep(4)
print 'Program terminated'
