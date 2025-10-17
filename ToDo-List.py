# Using open() function
file_path = "ToDoList.csv";

# Open the file in write mode
while (1):
    mode = input("Pour ouvrir la liste : \nEn mode lecture, tapez L \nEn mode ajout : tapez A\n").lower()
    if mode == 'a':
        mode = 'a'
        break
    elif mode == 'l':
        mode = 'r'
        break


with open(file_path, mode) as file:
    # Write content to the file
    if(mode == 'a'):
        text = input("Enter task : ")
        file.write(text)
        file.write("\n")
    else:
        for line in file:
            print(line, end="")  # end="" évite les doubles sauts de ligne


file.close()