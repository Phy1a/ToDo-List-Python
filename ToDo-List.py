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
                #print(data)    # data = dict = {tasks: [{task1}, {task2}]}
                self.tasks = data.get("tasks", []) if isinstance(data, dict) else [] # if dict, get the value (the tasks with metadata) of "tasks" key 
                #print(self.tasks)              # self.tasks = lst = [{task1}, {task2}]
        except (json.JSONDecodeError, OSError):         # decode or read error
            self.tasks = []

    def _save(self):
        """Save and close the todoList"""
        data = {"tasks": self.tasks}
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)    # false for emojis (maybe), 4 space for indentation

    def add_task(self, *, text: str, theme: str = "default", date= date.today(),
                 deadline= date.today(), time: int = 0, priority: int = 0,
                 color: str = "normal", done: bool = False):
        task = {
            "done": done,
            "theme": theme,
            "text": text,
            "date": date.strftime("%d-%m-%Y"),
            "deadline": deadline.strftime("%d-%m-%Y"),
            "time": time,
            "priority": priority,
            "color": color,
        }
        self.tasks.append(task)
        self._save()

    def list_tasks(self):
        return list(self.tasks)


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

def securedInputInt(message="Please enter un number : ", min=None, max=None):
    validity = False
    result = 0
    while (validity == False):
        validity = True
        try:
            result_str = (input(message))

            # Empty priority
            if (result_str == ""):
                return ""
            
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



def main():
    todo = TodoList("ToDoList.json")

    while True:
        # mode = input("Pour ouvrir la liste : \nEn mode lecture, tapez L \nEn mode ajout : tapez A\n").lower()
        mode = input("Pour ouvrir la liste : \nEn mode lecture, tapez L \nEn mode ajout : tapez A\n").strip().lower()
        if mode in ("a", "l"):
            break

    if mode == "a":
        print("Ajout d'une tache")
        text = voidstr("Texte de la tache : ").strip()      # input("Texte de la tache : ").strip()
        theme = (input("theme (default, school...) : ").strip() or "default")
        #today = date.today().strftime("%d-%m-%Y")   # DD-MM-YYYY          #input("Date d'ajout : ").strip()
        #deadlinetmp = input("Deadline : ").strip()
        deadline = checkdate("Deadline : ")      #datetime.strptime(deadlinetmp, "%d-%m-%Y")
        # time_val = check_time(input("Temps estimé : ").strip(), default=0)
        priority_val = securedInputInt("Priorité : ", 0, 5)
        color = (input("Couleur : ").strip() or "normal")
        if color.lower() not in colors and color.lower() != "normal":
            print(f"Couleur '{color}' non reconnue, utilisation de 'normal'.")
            color = "normal"
        done_in = input("fait ? (o/n) : ").strip().lower()
        done = done_in == "o"

        if deadline==None:
            deadline=""
        
        todo.add_task(
            text=text,
            theme=theme,
            #date=today, # datenow()
            deadline=deadline, # date
            #time=time_val,
            priority=priority_val,
            color=color, # RGB WIP
            done=done,
        )
        print("tache ajoutée au json")
    else: #L
        # work in progress
        tasks = todo.list_tasks() #=lst
        if not tasks:
            print("pas de tache")
        else:
            print("done | theme | text | date | deadline | priority | color")
            for t in tasks:
                color_name = t.get("color", "").lower()
                color_code = colors.get(color_name, "")
                print(color_code + f'Réalisé : {t.get("done", False)}\nThème : {t.get("theme","")}\nTâche : {t.get("text","")}\n'
                      f'Tâche créé le {t.get("date","")}\nPour le : {t.get("deadline","")}\n'
                      f'Niveau de priorité/5 : {t.get("priority","")}\nCouleur : {t.get("color","")}\n' + Style.RESET_ALL + "\n")


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