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
    "magenta": Fore.MAGENTA,
    "black": Fore.BLACK
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
        print(Fore.GREEN + "\nTask successfully added to the JSON file as:")
        printTask(task)

    def _edit_task(self, done, task, text ="", theme = "",
                 deadline= "", priority="",
                 color = ""):
        if (deadline != ""):
            deadline = deadline.strftime("%d-%m-%Y")
        if (done != ""):
            task.update({"done": done})
        if (theme != ""):
            task.update({"theme": theme})
        if (text != ""):
            task.update({"text": text})
        if (deadline != ""):
            task.update({"deadline": deadline})
        if (priority != ""):
            task.update({"priority": priority})
        if (color != ""):
            task.update({"color": color})
        
        self._save()

        # Printing
        print(Fore.GREEN + "Task successfully edited to the JSON file as:\n")
        printTask(task)

    def list_tasks(self):
        return list(self.tasks)

    def delete_task(self, task_id):
        # keep all the task exept the selected one
        self.tasks = [task for task in self.tasks if task["id"] != task_id]
        self._save()

    def _printSumUpTask(self, task_id: int =None):
        '''This function print the name and id of each task in the ToDoList'''
        task_id_list = []
        if not self.tasks:
            print("No task")
        else:
            if (task_id == None):
                print("----Tasks sum up----\n")
                for t in self.tasks:
                    color_name = t.get("color", "").lower()
                    color_code = colors.get(color_name, "")
                    task_id_list.append(str(t.get("id", "")))
                    print(color_code + f'Id : {t.get("id","Error")}\nTask : {t.get("text","")}\nDone : {t.get("done","")}\n' + Style.RESET_ALL)
            else:
                for t in self.tasks:
                    if(t.get("id", "error") == task_id):
                        color_name = t.get("color", "").lower()
                        color_code = colors.get(color_name, "")
                        task_id_list.append(str(t.get("id", "")))
                        print(color_code + f'Id : {t.get("id","Error")}\nTask : {t.get("text","")}\nDone : {t.get("done","")}\n' + Style.RESET_ALL)
                        break
                print("This task id does not figures in the ToDoList")


    def _checkDeadlines(self):
        task_list = []
        for task in self.tasks:
            today =  date.today().strftime("%d-%m-%Y")
            if (task.get("deadline", "") == today and task.get("done", "") == False):
                task_list.append(task)
        if (task_list != []):
            print(Fore.RED + f"You have {len(task_list)} undoned task(s) planned for today :" + Style.RESET_ALL)
            for task in task_list:
                self._printSumUpTask(task["id"])
                print()
        


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

def securedInputInt(message="Please enter un number : ", min: int =None, max: int =None, can_be_empty=True):
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
    '''This fonction checks that the input message matchs the date format dd-mm-yyyy or None if nothing is entered
    Parameter : str[] message
    return : str[] like dd-mm-yyyy or None '''
    while True:
        date_str = input(message)
        if date_str == "":
            return ""
        try:
            #print(date_str, "%d-%m-%Y"), date.today()
            date_obj = datetime.strptime(date_str, "%d-%m-%Y").date()
            if date_obj < date.today():
                print("La date est antérieure à aujourd'hui")
                continue
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
    print()
    print(color_code + f'Id : {task.get("id","Error")}\nTask : {task.get("text","")}\nDone : {task.get("done", False)}'+ Style.RESET_ALL)
    if (task.get("theme","") != "default"):
        print(color_code + f'Theme : {task.get("theme","")}' + Style.RESET_ALL)
    print(color_code + f'Task created on {task.get("date","")}'  + Style.RESET_ALL)
    if (task.get("deadline","") != None):
        print(color_code + f'For the : {task.get("deadline","")}' + Style.RESET_ALL)
    if (task.get("priority","") != 0):
        print(color_code + f'Priority level/5 : {task.get("priority","")}' + Style.RESET_ALL)
    print()


def sortTask(task, mode):
    """
    par date (ajout/deadline) (les plus récents en bas/deadline la plus proche en bas)
    par statut
    par ordre alphabétique
    priorité
    """
    if not isinstance(task, list):
        return []
    if mode == "date_added":
        # Expects `task` to be a list of task dicts; returns sorted list
        def parse_date(t):
            d = t.get("date", "")
            try:
                return datetime.strptime(d, "%d-%m-%Y")
            except Exception:
                # Put invalid/missing dates at the end
                return datetime.max
        return sorted(task, key=parse_date)
    elif mode == "priority":
        def parse_priority(t):
            p = t.get("priority", "")
            return p
        return sorted(task, key=parse_priority)
    elif mode == "alphabetically":
        # all tasks should start with uppercases for this to work
        def parse_tasks(t):
            t = t.get("text", "")
            return t
        return sorted(task, key=parse_tasks)
    elif mode == "deadline":
        def key_deadline(t):
            today = datetime.today().date()
            s = t.get("deadline", "") or ""
            try:
                d = datetime.strptime(s, "%d-%m-%Y").date()
            except Exception:
                return (0, 0)
            distance = abs((d - today).days)
            return (1, -distance, d.toordinal())
        return sorted(task, key=key_deadline)
    elif mode == "statut":
        done_tasks = []
        not_done_tasks = []
        for t in task:
            if t.get("done", False):
                done_tasks.append(t)
            else:
                not_done_tasks.append(t)
        return done_tasks + not_done_tasks
    return []





def main():
    todo = TodoList("ToDoList.json")
    todo._checkDeadlines()
    while True:
        print("------------------------")
        mode = securedInputString("To open the list: \nIn read mode, type L \nIn edition mode: type E\nIn delete mode: type S\nTo exit: type Q\n>>> ",['e','l', 's', 'q', 'E', 'L', 'S', 'Q'],False)
        print("------------------------\n")
        match mode.lower():
            case 'e': #edit mode
                print("------------------------")
                mode = securedInputString("Add a task : type A\nEdit a task content : type E\nMark a tast done : type M \nGo back to thre vious menu : type Q\n>>> ",['a', 'e', 'm', 'q', 'A', 'E', 'M', 'Q'],False)
                print("------------------------\n")
                match mode.lower():
                    case 'a':
                        print("Task addition")
                        #text = voidstr("Texte de la tache : ").strip()      # input("Texte de la tache : ").strip()
                        text = securedInputString("Task name : ", can_be_empty=False)      # input("Texte de la tache : ").strip()
                        text = text[0].upper() + text[1:]   # uppercase for first letter
                        theme = (input("theme (default, school...) : ").strip() or "default")
                        #today = date.today().strftime("%d-%m-%Y")   # DD-MM-YYYY          #input("Date d'ajout : ").strip()
                        #deadlinetmp = input("Deadline : ").strip()
                        deadline = checkdate("Deadline : ")      # %d-%m-%Y or None
                        # time_val = check_time(input("Temps estimé : ").strip(), default=0)
                        priority_val = securedInputInt("Priorité : ", 0, 5)
                        color = (input("Color : ").strip() or "normal")
                        if color.lower() not in colors and color.lower() != "normal":
                            print(f"Color '{color}' unknown, use of 'normal' instead.")
                            color = "normal"
                        while True:
                            done_in = input("Done ? (y/n) : ").strip().lower()
                            if done_in == "y" or done_in == "n" or done_in == "": # "" => false (by default)
                                break
                        done = done_in == "y"

                        if priority_val =="":
                            priority_val = 0
                        
                        todo.add_task(
                            text=text,
                            theme=theme,
                            deadline=deadline, # date or None
                            priority=priority_val,
                            color=color,
                            done=done
                        )
                        print("task added to the json")
                    case 'e': # full edit case
                        task_id_list = todo._printSumUpTask()
                        if (task_id_list != []):
                            selected_id = securedInputString("Please enter the id of the task you want to edit : ",task_id_list, True)
                            if selected_id != "":
                                for t in todo.tasks:
                                    if (str(t.get("id", "")) == selected_id):
                                        printTask(t)
                                        print("\nTo not modify the champ, just press enter\n")
                                        text = securedInputString("Task name : ", can_be_empty=True)      # input("Texte de la tache : ").strip()
                                        if(text != ""):
                                            text = text[0].upper() + text[1:]   # uppercase for first letter
                                        theme = input("theme (default, school...) : ").strip()
                                        deadline = checkdate("Deadline : ")    #datetime.strptime(deadlinetmp, "%d-%m-%Y")
                                        priority_val = securedInputInt("Priorité : ", 0, 5)
                                        if priority_val =="":
                                            priority_val = t.get("priority", "")
                                        color = (input("Color : ").strip() or "")
                                        if color.lower() not in colors and color.lower() != "":
                                            print(f"Color '{color}' unknown, use of 'normal' instead.")
                                            color = ""
                                        while True:
                                            done_in = input("Done ? (y/n) : ").strip().lower()
                                            if done_in == "y" or done_in == "n" or done_in == "":
                                                break
                                        done = done_in == "y"
                                        todo._edit_task(task=t,
                                                        text=text,
                                                        theme=theme,
                                                        deadline=deadline, # date
                                                        priority = priority_val,
                                                        color=color,
                                                        done=done)
                            else:
                                print(Fore.RED + "Edition aborted" )
                        else:
                            print("Edition aborted")
                    case 'm': # mark task done case
                        task_id_list = todo._printSumUpTask()
                        if (task_id_list != []):
                            selected_id = securedInputString("Please enter the id of the task you want to toggle mark as done : ",task_id_list, True)
                            if selected_id != "":
                                for t in todo.tasks:
                                    if (str(t.get("id", "")) == selected_id):
                                        if(t.get("done", "")==True):
                                            todo._edit_task(task=t,done=False)
                                        else:
                                            todo._edit_task(task=t,done=True)
                            else:
                                print(Fore.RED + "Operation aborted" )
                        else:
                            print("Operation aborted")
                    case 'q':
                        continue
                    case default:
                        continue
            case 'l': #L
                # work in progress
                tasks = todo.list_tasks() #=lst
                sort = securedInputString("Choose a sort (optional):\nWithout sort: type L\nSort by task added date: type T\nSort by deadline: type DL\nSort alphabetically: type A\nSort by Done status: type D\nSort by priority: type P\n>>> ", 
                                          ["l", "L", "t", "T", "dl", "DL", "a", "A", "d", "D", "p", "P", ""], 
                                          True)
                print("------------------------\n")
                if not tasks or tasks == []:
                    print("No task")
                elif sort != "" or sort.lower() !="l":
                    match sort.lower():
                        case "t":
                            tasks = sortTask(tasks, "date_added")
                        case "dl":
                            tasks = sortTask(tasks, "deadline")
                        case "a":
                            tasks = sortTask(tasks, "alphabetically")
                        case "d":
                            tasks = sortTask(tasks, "statut")
                        case "p":
                            tasks = sortTask(tasks, "priority")
                    for t in tasks:
                        printTask(t)
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