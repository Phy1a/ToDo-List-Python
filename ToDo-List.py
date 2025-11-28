#import csv
import json
import os
from datetime import date
from datetime import datetime

from colorama import Fore, Style, init

init(autoreset=True)
colors = {
    "red": Fore.RED,
    "green": Fore.GREEN,
    "blue": Fore.BLUE,
    "yellow": Fore.YELLOW,
    "cyan": Fore.CYAN,
    "magenta": Fore.MAGENTA
}

class TodoList:
    def __init__(self, file_path: str = "ToDoList.json"):
        self.file_path = file_path
        self.tasks = []
        self._load()

    def _load(self):
        if not os.path.exists(self.file_path):
            self.tasks = []
            return
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:      # can create many todoLists as we want
                data = json.load(f)     # dict

            # data = dict = {tasks: [{task1}, {task2}]}
            self.tasks = data.get("tasks", []) if isinstance(data, dict) else [] # if dict, get the value (the tasks with metadata) of "tasks" key 
            # self.tasks = lst = [{task1}, {task2}]
            self.tasks_by_id = {task["id"]: task for task in data["tasks"]}

        except (json.JSONDecodeError, OSError):         # decode or read error
            self.tasks = []


    
    def _save(self):
        """Save and close the todoList"""

        data = {"tasks": self.tasks}
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)    # false for emojis (maybe), 4 space for indentation

    def add_task(self, *, text: str, theme: str = "default", date= date.today(),
                 deadline, time: int = 0, priority: int = 0,
                 color: str = "normal", done: bool = False):
        if deadline != None:
            deadline = deadline.strftime("%d-%m-%Y")
        task = {
            "id" : len(self.tasks)+ 1, # unique id at a given time
            "done": done,
            "theme": theme,
            "text": text,
            "date": date.strftime("%d-%m-%Y"),
            "deadline": deadline,
            "time": time,
            "priority": priority,
            "color": color,
        }
        self.tasks.append(task)
        self._save()

        # Printing
        print("Task successfully added to the JSON file as:\n")
        printTask(task)

    def list_tasks(self):
        return list(self.tasks)

    def delete_task(self, task_id):
        # keep all the task exept the selected one
        self.tasks = [task for task in self.tasks if task["id"] != task_id]
        self._save()

    def _printSumUpTask(self):
        '''This function print the name and id of each task in the ToDoList'''
        task_id_list = []
        if not self.tasks:
            print("No task")
        else:
            print("----Tasks sum up----\n")
            for t in self.tasks:
                color_name = t.get("color", "").lower()
                color_code = colors.get(color_name, "")
                task_id_list.append(str(t.get("id", "")))
                print(color_code + f'Id : {t.get("id","Error")}\nTâche : {t.get("text","")}\n' + Style.RESET_ALL)
        return task_id_list


#useless ?
def check_priority(val, default=0):
    while True:
        if 0 <= int(val) <= 5:
            try:
                return int(val)
            except (TypeError, ValueError):
                print("ce n'est pas une priorité valide")
                continue

def check_time(val, default=0):
    pass

    while True:
        if 0 <= default <= 8:
            try:
                return int(val)
            except (TypeError, ValueError):
                print("ce n'est pas une priorité valide")
                continue

def securedInputInt(message="Please enter un number : ", min=None, max=None, can_be_empty=True):
    ''' This function returns the user selected integer and assure its validity
    Parameters : 
    char * message [In], the message to print to the user, has a default value
    int min [In], the minimum accepted value, optional
    int max [In], the maximum accepted value, optional
    bool can_be_empty [In], if the number is optional then the user can let it empty
    Return : int result, the number selected by the user'''
    validity = False
    result = 0
    while (validity == False):
        validity = True
        try:
            result_str = (input(message))

            # Empty priority
            if(result_str == ""):
                if (can_be_empty):
                    return ""
                else:
                    validity = False
            
            result = int(result_str)
            if (min != None and result < min):
                print("The minimum accepted value is ", min)
                validity = False
            if (max != None and result > max):
                print("The maximum accepted value is ", max)
                validity = False
        except:
            print("Please enter a number.")
            validity = False    
    return result

def securedInputString(message="Please enter a message: ", answers_list=None, can_be_empty=True):
    ''' This function returns the user selected option and assure its validity
    Parameters : 
    char * message [In] : the message to print to the user, has a default value
    char[] answers_list [In] : the list of possible answers
    bool can_be_empty [In], if the number is optional then the user can let it empty
    Return : char[], the selected answer by the user'''
    validity = False
    while (validity == False):
        validity = True

        result_str = (input(message)).strip()

        if(result_str == ""):
            if (can_be_empty):
                return ""
            else:
                print(f"\nThis answer isn't optional therefore it can't be empty\n")
                validity = False

        
        if (answers_list != None and result_str not in answers_list):
            print(f"\nThis answer is invalid, the possible answer are {answers_list}\n")
            validity = False
 
    return result_str


# Useless now
def voidstr(message):
    str = input(message)
    while True:
        if str=="":
            print("Veuillez rentrer une tache")
            str = input(message)
        else:
            return str

def checkdate(message):
    while True:
        date_str = input(message)
        if date_str == "":
            break
        try:
            if datetime.strptime(date_str, "%d-%m-%Y") < datetime.today():
                print("La date est antérieure à aujourd'hui")
                continue
            date_obj = datetime.strptime(date_str, "%d-%m-%Y").date()
            return date_obj
        except ValueError:
            print("Date non valide (jj-mm-yyyy)")

#Useless
def getMode():
    ''' This function returns the user selected mode and assure its validity
    Parameters : None
    Return : char mode, the mode selected by the user'''
    while True:
        # mode = input("Pour ouvrir la liste : \nEn mode lecture, tapez L \nEn mode ajout : tapez A\n").lower()
        print("------------------------")
        mode = input("Pour ouvrir la liste : \nEn mode lecture, tapez L \nEn mode ajout : tapez A\nEn mode suppression: tapez S\nPour quitter: tapez Q\n>>> ").strip().lower()
        print("------------------------\n")
        if mode in ("a", "l", "s", 'q'):
            return mode

def printTask(task):
    color_name = task.get("color", "").lower()
    color_code = colors.get(color_name, "")
    print(color_code + f'Id : {task.get("id","Error")}\nDone : {task.get("done", False)}\nTheme : {task.get("theme","")}\nTask : {task.get("text","")}\n'
        f'Task created on {task.get("date","")}\nFor the : {task.get("deadline","")}\n'
        f'Priority level/5 : {task.get("priority","")}\nColor : {task.get("color","")}\n' + Style.RESET_ALL + "\n")


def main():
    todo = TodoList("ToDoList.json")
    while True:
        print("------------------------")
        mode = securedInputString("To open the list: \nIn read mode, type L \nIn edition mode: type E\nIn delete mode: type S\nTo exit: type Q\n>>> ",['e','l', 's', 'q', 'e', 'L', 'S', 'Q'],False)
        print("------------------------\n")
        match mode.lower():
            case 'e':
                print("------------------------")
                mode = securedInputString("Add a task : type A,\nEdit a task content : type E\nMark a tast done : type M \nGo back to thre vious menu : type Q\n>>> ",['a', 'e', 'm', 'q', 'A', 'E', 'M', 'Q'],False)
                print("------------------------\n")
                match mode.lower():
                    case 'a':
                        print("Task addition")
                        #text = voidstr("Texte de la tache : ").strip()      # input("Texte de la tache : ").strip()
                        text = securedInputString("Task name : ", can_be_empty=False)      # input("Texte de la tache : ").strip()
                        theme = (input("theme (default, school...) : ").strip() or "default")
                        #today = date.today().strftime("%d-%m-%Y")   # DD-MM-YYYY          #input("Date d'ajout : ").strip()
                        #deadlinetmp = input("Deadline : ").strip()
                        deadline = checkdate("Deadline : ")      #datetime.strptime(deadlinetmp, "%d-%m-%Y")
                        # time_val = check_time(input("Temps estimé : ").strip(), default=0)
                        priority_val = securedInputInt("Priorité : ", 0, 5)
                        color = (input("Color : ").strip() or "normal")
                        if color.lower() not in colors and color.lower() != "normal":
                            print(f"Color '{color}' unknown, use of 'normal' instead.")
                            color = "normal"
                        done_in = input("Done ? (y/n) : ").strip().lower()
                        done = done_in == "y"

                        if priority_val =="":
                            priority_val = 0
                        
                        todo.add_task(
                            text=text,
                            theme=theme,
                            deadline=deadline, # date
                            priority=priority_val,
                            color=color, # RGB WIP
                            done=done,
                        )
                        print("task added to the json")
                    case 'e':
                        todo._printSumUpTask

                        continue
                    case 'q':
                        continue
                    case default:
                        continue
            case 'l': #L
                # work in progress
                tasks = todo.list_tasks() #=lst
                if not tasks:
                    print("No task")
                else:
                    #print("id | done | theme | text | date | deadline | priority | color")
                    for t in tasks:
                        printTask(t)
            case 's': # mode == s
                task_id_list = todo._printSumUpTask()
                if (task_id_list != []):
                    selected_id = securedInputString("Please enter the id of the task you want to delete : ",task_id_list, True)
                    if selected_id != "":
                        todo.delete_task(int(selected_id))
                        print(Fore.GREEN + f"Task n°{selected_id} successfully deleted")
                    else:
                        print(Fore.RED + "Deletion aborted" )
            case 'q': # mode == q, to quit
                break
            case default:
                break


if __name__ == "__main__":
    main()



# else:
#         csv_reader = csv.reader(file, delimiter=',')
#         for line in csv_reader:
#             if line_count == 0:
#                 print(f'Column names are {", ".join(line)}')
#                 line_count += 1
#             else:
#                 print(f'{line[0]} |{line[1]} |{line[2]} |{line[3]} |{line[4]} |{line[5]} |{line[6]}')
#                 line_count += 1
            # print(line, end="")  # end="" évite les doubles sauts de ligne
#file.close