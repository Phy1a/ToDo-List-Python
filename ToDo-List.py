#import csv
import json
import os

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

    def add_task(self, *, text: str, theme: str = "default", date: str = "",
                 deadline: str = "", time: int = 0, priority: int = 0,
                 color: str = "normal", done: bool = False):
        task = {
            "done": done,
            "theme": theme,
            "text": text,
            "date": date,
            "deadline": deadline,
            "time": time,
            "priority": priority,
            "color": color,
        }
        self.tasks.append(task)
        self._save()

    def list_tasks(self):
        return list(self.tasks)


#useless ?
def to_int(val, default=0):
    try:
        return int(val)
    except (TypeError, ValueError):
        return default

def securedInputInt(message="Please enter un number : ", min=None, max=None):
    validity = False
    while (validity == False):
        validity = True
        try:
            result = int(input(message))
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

def main():
    todo = TodoList("ToDoList.json")

    while True:
        # mode = input("Pour ouvrir la liste : \nEn mode lecture, tapez L \nEn mode ajout : tapez A\n").lower()
        mode = input("Pour ouvrir la liste : \nEn mode lecture, tapez L \nEn mode ajout : tapez A\n").strip().lower()
        if mode in ("a", "l"):
            break

    if mode == "a":
        print("Ajout d'une tache")
        text = input("Texte de la tache : ").strip()
        theme = (input("theme (default, school...) : ").strip() or "default")
        date = input("Date d'ajout : ").strip()
        deadline = input("Deadline : ").strip()
        priority_val = to_int(input("Priorité : ").strip(), default=0)
        color = (input("Couleur : ").strip() or "normal")
        done_in = input("fait ? (o/n) : ").strip().lower()
        done = done_in == "o"

        todo.add_task(
            text=text,
            theme=theme,
            date=date,
            deadline=deadline,
            time=time_val,
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
            print("done | theme | text | date | deadline | time | priority | color")
            for t in tasks:
                print(f'{t.get("done", False)} | {t.get("theme","")} | {t.get("text","")} | '
                      f'{t.get("date","")} | {t.get("deadline","")} | {t.get("time","")} | '
                      f'{t.get("priority","")} | {t.get("color","")}')


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