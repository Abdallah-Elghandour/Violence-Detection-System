
file1 = open("dataset2\\64 frames data\\X_data.txt", "a")
file2 = open("dataset2\\64 frames data\\Y_data.txt", "a")
file3 = open("dataset2\\64 frames data\\X_Holding.txt", "r")
file4 = open("dataset2\\64 frames data\\Y_Holding.txt", "r")

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



# file1 = open("dataset\\64 frames data\\Y.txt", "r")
# file2 = open("dataset\\64 frames data\\Y_violence.txt", "w")

# lines = file1.readlines()
# for line in lines:
#     if line == "0\n":
#         file2.write("1\n")
#     else:
#         file2.write("1\n")


# file1.close()
# file2.close()


