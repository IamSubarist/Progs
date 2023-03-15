import os



# file1 = open("a.txt",'r')        
# file2 = open("b.txt",'r')
NewFile = open("difference.txt",'r')

# for line1 in file1:
#     if line1 not in file2:
#         NewFile.write(line1)
        # os.remove(line1)

for line1 in NewFile:
    line = line1.replace('\n', '')
    # print(line)
    
    path_c = 'C:/Users/User/Desktop/Promezh'
    if line not in path_c:
        line.replace(line, '')
        # os.remove(line)
    os.remove(line)

# file1.close()
# file2.close()
NewFile.close()