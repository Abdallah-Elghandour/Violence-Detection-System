# here we append the data from the class files to the data file
# so that all data will be in one file and we can use it for training

file1 = open("data\\dataset\\X_data.txt", "a")
file2 = open("data\\dataset\\Y_data.txt", "a")
file3 = open("data\\dataset\\X_Holding.txt", "r")
file4 = open("data\\dataset\\Y_Holding.txt", "r")

lines = file3.readlines()
lines2 = file4.readlines()
i = 0
j = 0

for line in lines:
    i += 1 
    file1.write(line)
    if i == 64:
        file2.write(lines2[j])
        j += 1
        i = 0

file1.close()
file2.close()
file3.close()
file4.close()

