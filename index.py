while(1) :
    x = input("Enter > ")
    f = open("list.txt", "a")
    f.write(str(x)+"\n")
    f.close()


#open and read the file after the appending:
# f = open("list.txt", "r")
# print(f.read())