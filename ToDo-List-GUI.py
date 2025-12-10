import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
from datetime import date, datetime
from typing import Optional

class TodoListGUI:
    def __init__(self, master, file_path: str = "ToDoList.json"):
        self.master = master
        self.master.title("ToDo List Manager")
        self.master.geometry("1000x700")
        self.master.configure(bg="#f0f0f0")
        
        self.file_path = file_path
        self.tasks = []
        self.tasks_by_id = {}
        self._load()
        
        # configuration des couleurs
        self.colors = {
            "red": "#FF0000",
            "green": "#00FF00",
            "blue": "#0000FF",
            "yellow": "#FFFF00",
            "cyan": "#00FFFF",
            "magenta": "#FF00FF",
            "black": "#000000",
            "normal": "#000000"
        }
        
        self.setup_ui()
        self._check_deadlines()
        
    def _load(self):
        """charge les tâches depuis le fichier JSON"""
        if not os.path.exists(self.file_path):
            self.tasks = []
            self._reindex()
            return
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.tasks = data.get("tasks", []) if isinstance(data, dict) else []
            self._reindex()
        except (json.JSONDecodeError, OSError):
            self.tasks = []
            self.tasks_by_id = {}
    
    def _reindex(self):
        """reconstruit l'index des tâches par ID"""
        self.tasks_by_id = {t["id"]: t for t in self.tasks}
    
    def _save(self):
        """sauvegarde les tâches dans le fichier JSON"""
        data = {"tasks": self.tasks}
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    def setup_ui(self):
        """configure l'interface utilisateur principale"""
        # titre
        title_frame = tk.Frame(self.master, bg="#2c3e50", height=60)
        title_frame.pack(fill=tk.X, side=tk.TOP)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="📋 Gestionnaire de tâches", 
                              font=("Arial", 20, "bold"), 
                              bg="#2c3e50", fg="white")
        title_label.pack(pady=15)
        
        # fenetre principale avec deux colonnes
        main_frame = tk.Frame(self.master, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # colonne gauche - controle
        left_frame = tk.Frame(main_frame, bg="#f0f0f0", width=250)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_frame.pack_propagate(False)
        
        # section edition
        edit_label = tk.Label(left_frame, text="Édition", 
                             font=("Arial", 14, "bold"), 
                             bg="#f0f0f0")
        edit_label.pack(pady=(10, 5))
        
        btn_add = tk.Button(left_frame, text="➕ Ajouter une tâche", 
                           command=self.add_task_window,
                           bg="#27ae60", fg="white", 
                           font=("Arial", 10, "bold"),
                           relief=tk.FLAT, padx=10, pady=8)
        btn_add.pack(fill=tk.X, pady=5, padx=10)
        
        btn_edit = tk.Button(left_frame, text="✏️ Modifier une tâche", 
                            command=self.edit_task_window,
                            bg="#3498db", fg="white", 
                            font=("Arial", 10, "bold"),
                            relief=tk.FLAT, padx=10, pady=8)
        btn_edit.pack(fill=tk.X, pady=5, padx=10)
        
        btn_toggle = tk.Button(left_frame, text="✓ Changer le statut", 
                              command=self.toggle_task_status,
                              bg="#9b59b6", fg="white", 
                              font=("Arial", 10, "bold"),
                              relief=tk.FLAT, padx=10, pady=8)
        btn_toggle.pack(fill=tk.X, pady=5, padx=10)
        
        btn_delete = tk.Button(left_frame, text="🗑️ Supprimer une tâche", 
                              command=self.delete_task_window,
                              bg="#e74c3c", fg="white", 
                              font=("Arial", 10, "bold"),
                              relief=tk.FLAT, padx=10, pady=8)
        btn_delete.pack(fill=tk.X, pady=5, padx=10)
        
        # section affichage
        view_label = tk.Label(left_frame, text="Affichage", 
                             font=("Arial", 14, "bold"), 
                             bg="#f0f0f0")
        view_label.pack(pady=(20, 5))
        
        # filtres
        filter_frame = tk.LabelFrame(left_frame, text="Filtrer par", 
                                     bg="#f0f0f0", font=("Arial", 10, "bold"))
        filter_frame.pack(fill=tk.X, pady=5, padx=10)
        
        self.filter_var = tk.StringVar(value="all")
        self.active_filter_params = {}  # stocker les parametres de filtrage en cours
        
        filters = [
            ("Toutes", "all"),
            ("Non terminées", "not_done"),
            ("Terminées", "done"),
            ("Par catégorie", "category"),
            ("Par couleur", "color"),
            ("Par priorité", "priority")
        ]
        
        for text, value in filters:
            rb = tk.Radiobutton(filter_frame, text=text, 
                               variable=self.filter_var, value=value,
                               bg="#f0f0f0", font=("Arial", 9),
                               command=lambda v=value: self.on_filter_change(v))
            rb.pack(anchor=tk.W, padx=5, pady=2)
        
        # boutons de tri
        sort_frame = tk.LabelFrame(left_frame, text="Trier par", 
                                   bg="#f0f0f0", font=("Arial", 10, "bold"))
        sort_frame.pack(fill=tk.X, pady=5, padx=10)
        
        self.sort_var = tk.StringVar(value="none")
        sorts = [
            ("Aucun tri", "none"),
            ("Date d'ajout", "date_added"),
            ("Deadline", "deadline"),
            ("Alphabétique", "alphabetically"),
            ("Statut", "statut"),
            ("Priorité", "priority")
        ]
        
        for text, value in sorts:
            rb = tk.Radiobutton(sort_frame, text=text, 
                               variable=self.sort_var, value=value,
                               bg="#f0f0f0", font=("Arial", 9),
                               command=self.apply_filter_sort)
            rb.pack(anchor=tk.W, padx=5, pady=2)
        
        btn_refresh = tk.Button(left_frame, text="Rafraîchir", 
                               command=self.refresh_display,
                               bg="#34495e", fg="white", 
                               font=("Arial", 10, "bold"),
                               relief=tk.FLAT, padx=10, pady=8)
        btn_refresh.pack(fill=tk.X, pady=10, padx=10)
        
        # colonne droite - affichage des tâches
        right_frame = tk.Frame(main_frame, bg="white")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # barre de recherche
        search_frame = tk.Frame(right_frame, bg="white")
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(search_frame, text="🔍 Recherche:", 
                font=("Arial", 10), bg="white").pack(side=tk.LEFT, padx=5)
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.apply_filter_sort())
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, 
                               font=("Arial", 10), width=40)
        search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # zone de texte scrollable pour afficher les tâches
        self.task_display = scrolledtext.ScrolledText(right_frame, 
                                                       wrap=tk.WORD,
                                                       font=("Consolas", 10),
                                                       bg="white",
                                                       relief=tk.FLAT,
                                                       padx=10, pady=10)
        self.task_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # configuration des tags de couleur pour le texte
        for color_name, color_code in self.colors.items():
            self.task_display.tag_config(color_name, foreground=color_code)
        
        self.task_display.tag_config("title", font=("Arial", 11, "bold"))
        self.task_display.tag_config("urgent", background="#ffcccc")
        self.task_display.tag_config("done", foreground="#808080", overstrike=True)
        
        # affichage initial
        self.refresh_display()
    
    def _check_deadlines(self):
        """vérifie les deadlines et affiche les alertes"""
        task_list_today = []
        task_list_past = []
        today = date.today()
        
        for task in self.tasks:
            deadline = task.get("deadline", "")
            if not task.get("done", False) and deadline:
                try:
                    deadline_date = datetime.strptime(deadline, "%d-%m-%Y").date()
                    if deadline_date == today:
                        task_list_today.append(task)
                    elif deadline_date < today:
                        task_list_past.append(task)
                except:
                    pass
        
        if task_list_past or task_list_today:
            msg = ""
            if task_list_past:
                msg += f"⚠️ {len(task_list_past)} tâche(s) en retard:\n"
                for t in task_list_past:
                    msg += f"  - {t['text']}\n"
                msg += "\n"
            
            if task_list_today:
                msg += f"{len(task_list_today)} tâche(s) pour aujourd'hui:\n"
                for t in task_list_today:
                    msg += f"  - {t['text']}\n"
            
            messagebox.showwarning("Rappel de deadlines", msg)
    
    def display_tasks(self, tasks):
        """affiche les tâches dans la zone de texte"""
        self.task_display.config(state=tk.NORMAL)
        self.task_display.delete(1.0, tk.END)
        
        if not tasks:
            self.task_display.insert(tk.END, "Aucune tâche à afficher.\n", "title")
        else:
            for task in tasks:
                self._display_single_task(task)
                self.task_display.insert(tk.END, "\n" + "─"*80 + "\n\n")
        
        self.task_display.config(state=tk.DISABLED)
    
    def _display_single_task(self, task):
        """affiche une seule tâche avec formatage"""
        color = task.get("color", "normal")
        done = task.get("done", False)
        
        # ID et texte
        id_text = f"📌 ID: {task.get('id', 'N/A')} | "
        self.task_display.insert(tk.END, id_text, color)
        
        task_text = f"{task.get('text', '')}\n"
        if done:
            self.task_display.insert(tk.END, task_text, ("done", color))
        else:
            self.task_display.insert(tk.END, task_text, (color, "title"))
        
        # statut de la tache
        status = "✅ Terminée" if done else "⏳ En cours"
        self.task_display.insert(tk.END, f"Statut: {status}\n", color)
        
        # theme
        if task.get("theme", "") != "default":
            self.task_display.insert(tk.END, f"📁 Thème: {task.get('theme', '')}\n", color)
        
        # date de création
        self.task_display.insert(tk.END, f"📅 Créée le: {task.get('date', '')}\n", color)
        
        # deadline
        if task.get("deadline", ""):
            today = date.today()
            try:
                deadline_date = datetime.strptime(task.get("deadline"), "%d-%m-%Y").date()
                if deadline_date <= today and not done:
                    self.task_display.insert(tk.END, f"⚠️ DEADLINE: {task.get('deadline')}\n", 
                                           ("urgent", color))
                else:
                    self.task_display.insert(tk.END, f"⏰ Deadline: {task.get('deadline')}\n", color)
            except:
                self.task_display.insert(tk.END, f"⏰ Deadline: {task.get('deadline')}\n", color)
        
        # priorité
        if task.get("priority", 0) != 0:
            priority = task.get("priority", 0)
            self.task_display.insert(tk.END, f"Priorité: {priority}/5\n", color)
    
    def on_filter_change(self, filter_value):
        """gère le changement de filtre et ouvre les fenêtres de sélection si nécessaire"""
        if filter_value == "category":
            self.filter_by_category_window()
        elif filter_value == "color":
            self.filter_by_color_window()
        elif filter_value == "priority":
            self.filter_by_priority_window()
        else:
            # pour terminées/non terminées 
            self.apply_filter_sort()
    
    def apply_filter_sort(self):
        """applique les filtres + tris sélectionnés"""
        tasks = list(self.tasks)
        
        # recherche textuelle
        search_text = self.search_var.get().lower()
        if search_text:
            tasks = [t for t in tasks if search_text in t.get("text", "").lower()]
        
        # filtrage
        filter_mode = self.filter_var.get()
        tasks = self._apply_filter(tasks, filter_mode)
        
        # tri
        sort_mode = self.sort_var.get()
        if sort_mode != "none":
            tasks = self._sort_tasks(tasks, sort_mode)
        
        self.display_tasks(tasks)
    
    def _apply_filter(self, tasks, mode):
        """applique un filtre aux tâches"""
        if mode == "all":
            return tasks
        elif mode == "done":
            return [t for t in tasks if t.get("done", False)]
        elif mode == "not_done":
            return [t for t in tasks if not t.get("done", False)]
        elif mode == "category" and "category" in self.active_filter_params:
            return [t for t in tasks if t.get("theme") == self.active_filter_params["category"]]
        elif mode == "color" and "color" in self.active_filter_params:
            return [t for t in tasks if t.get("color") == self.active_filter_params["color"]]
        elif mode == "priority" and "priority" in self.active_filter_params:
            return [t for t in tasks if t.get("priority") == self.active_filter_params["priority"]]
        return tasks
    
    def filter_by_category_window(self):
        """ouvre une fenêtre pour filtrer par catégorie"""
        categories = list(set(t.get("theme", "") for t in self.tasks if t.get("theme")))
        if not categories:
            messagebox.showinfo("Info", "Aucune catégorie disponible")
            self.filter_var.set("all")  # si annulé, revenir au filtre "toutes"
            return
        
        category = self._select_from_list("Choisir une catégorie", categories)
        if category:
            self.active_filter_params["category"] = category
            self.apply_filter_sort()
        else:
            self.filter_var.set("all")  
    
    def filter_by_color_window(self):
        """ouvre une fenêtre pour filtrer par couleur"""
        colors = list(set(t.get("color", "") for t in self.tasks if t.get("color")))
        if not colors:
            messagebox.showinfo("Info", "Aucune couleur disponible")
            self.filter_var.set("all")
            return
        
        color = self._select_from_list("Choisir une couleur", colors)
        if color:
            self.active_filter_params["color"] = color
            self.apply_filter_sort()
        else:
            self.filter_var.set("all")
    
    def filter_by_priority_window(self):
        """ouvre une fenêtre pour filtrer par priorité"""
        priority = self._ask_priority("Choisir une priorité (0-5)")
        if priority is not None:
            self.active_filter_params["priority"] = priority
            self.apply_filter_sort()
        else:
            self.filter_var.set("all")
    
    def _sort_tasks(self, tasks, mode):
        """trie les tâches selon le mode spécifié"""
        if mode == "date_added":
            return sorted(tasks, key=lambda t: self._parse_date(t.get("date", "")))
        elif mode == "deadline":
            def key_deadline(t):
                s = (t.get("deadline", "") or "").strip()
                if not s:
                    return (0, datetime.min)
                try:
                    d = datetime.strptime(s, "%d-%m-%Y").date()
                    return (1, d)
                except:
                    return (0, datetime.min)
            return sorted(tasks, key=key_deadline)
        elif mode == "alphabetically":
            return sorted(tasks, key=lambda t: t.get("text", "").lower())
        elif mode == "statut":
            done = [t for t in tasks if t.get("done", False)]
            not_done = [t for t in tasks if not t.get("done", False)]
            return done + not_done
        elif mode == "priority":
            return sorted(tasks, key=lambda t: t.get("priority", 0), reverse=True)
        return tasks
    
    def _parse_date(self, date_str):
        """parse une date au format dd-mm-yyyy"""
        try:
            return datetime.strptime(date_str, "%d-%m-%Y")
        except:
            return datetime.max
    
    def refresh_display(self):
        """rafraîchit l'affichage"""
        self._load()
        self.apply_filter_sort()
    
    def add_task_window(self):
        """fenetre pour ajouter une tache"""
        window = tk.Toplevel(self.master)
        window.title("Ajouter une tâche")
        window.geometry("500x550")
        window.configure(bg="#f0f0f0")
        
        # champs du formulaire d'ajout de tache
        fields = {}
        
        row = 0
        # texte du todo (obligatoire)
        tk.Label(window, text="* Nom de la tâche:", bg="#f0f0f0", 
                font=("Arial", 10, "bold")).grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        fields['text'] = tk.Entry(window, width=40, font=("Arial", 10))
        fields['text'].grid(row=row, column=1, padx=10, pady=5)
        
        row += 1
        # theme
        tk.Label(window, text="Thème:", bg="#f0f0f0", 
                font=("Arial", 10)).grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        fields['theme'] = tk.Entry(window, width=40, font=("Arial", 10))
        fields['theme'].insert(0, "default")
        fields['theme'].grid(row=row, column=1, padx=10, pady=5)
        
        row += 1
        # deadline
        tk.Label(window, text="Deadline (jj-mm-aaaa):", bg="#f0f0f0", 
                font=("Arial", 10)).grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        fields['deadline'] = tk.Entry(window, width=40, font=("Arial", 10))
        fields['deadline'].grid(row=row, column=1, padx=10, pady=5)
        
        row += 1
        # priorité
        tk.Label(window, text="Priorité (0-5):", bg="#f0f0f0", 
                font=("Arial", 10)).grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        fields['priority'] = tk.Spinbox(window, from_=0, to=5, width=38, font=("Arial", 10))
        fields['priority'].grid(row=row, column=1, padx=10, pady=5)
        
        row += 1
        # couleur
        tk.Label(window, text="Couleur:", bg="#f0f0f0", 
                font=("Arial", 10)).grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        fields['color'] = ttk.Combobox(window, width=37, font=("Arial", 10),
                                       values=list(self.colors.keys()))
        fields['color'].set("normal")
        fields['color'].grid(row=row, column=1, padx=10, pady=5)
        
        row += 1
        # statut
        fields['done'] = tk.BooleanVar()
        tk.Checkbutton(window, text="Marquer comme terminée", variable=fields['done'],
                      bg="#f0f0f0", font=("Arial", 10)).grid(row=row, column=0, 
                                                             columnspan=2, pady=10)
        
        row += 1
        # boutons d'annulation/validation
        btn_frame = tk.Frame(window, bg="#f0f0f0")
        btn_frame.grid(row=row, column=0, columnspan=2, pady=20)
        
        def save_task():
            text = fields['text'].get().strip()
            if not text:
                messagebox.showerror("Erreur", "Le nom de la tâche est obligatoire!")
                return
            
            # Capitaliser la première lettre
            text = text[0].upper() + text[1:] if len(text) > 1 else text.upper()
            
            theme = fields['theme'].get().strip() or "default"
            deadline_str = fields['deadline'].get().strip()
            deadline = ""
            
            if deadline_str:
                try:
                    deadline_date = datetime.strptime(deadline_str, "%d-%m-%Y").date()
                    if deadline_date < date.today():
                        messagebox.showerror("Erreur", "La deadline ne peut pas être dans le passé!")
                        return
                    deadline = deadline_str
                except ValueError:
                    messagebox.showerror("Erreur", "Format de date invalide (jj-mm-aaaa)!")
                    return
            
            try:
                priority = int(fields['priority'].get())
            except:
                priority = 0
            
            color = fields['color'].get() or "normal"
            done = fields['done'].get()
            
            self._add_task(text=text, theme=theme, deadline=deadline, 
                          priority=priority, color=color, done=done)
            
            window.destroy()
            self.refresh_display()
            messagebox.showinfo("Succès", "Tâche ajoutée avec succès!")
        
        tk.Button(btn_frame, text="Ajouter", command=save_task,
                 bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                 padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Annuler", command=window.destroy,
                 bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                 padx=20, pady=5).pack(side=tk.LEFT, padx=5)
    
    def _add_task(self, text, theme, deadline, priority, color, done):
        """ajoute une tâche à la liste"""
        # trouver un ID unique
        id_count = 1
        for task in self.tasks:
            if task.get("id") == id_count:
                id_count += 1
        
        new_task = {
            "id": id_count,
            "done": done,
            "theme": theme,
            "text": text,
            "date": date.today().strftime("%d-%m-%Y"),
            "deadline": deadline,
            "priority": priority,
            "color": color,
        }
        
        # insérer la tache à la bonne position dans le json
        for idx, task in enumerate(self.tasks):
            if new_task["id"] < task["id"]:
                self.tasks.insert(idx, new_task)
                break
        else:
            self.tasks.append(new_task)
        
        self._reindex()
        self._save()
    
    def edit_task_window(self):
        """fenêtre pour modifier une tâche"""
        task_id = self._select_task_id("Modifier une tâche")
        if task_id is None:
            return
        
        task = self.tasks_by_id.get(task_id)
        if not task:
            messagebox.showerror("Erreur", "Tâche introuvable!")
            return
        
        window = tk.Toplevel(self.master)
        window.title(f"Modifier la tâche #{task_id}")
        window.geometry("500x550")
        window.configure(bg="#f0f0f0")
        
        fields = {}
        
        row = 0
        # texte
        tk.Label(window, text="Nom de la tâche:", bg="#f0f0f0", 
                font=("Arial", 10, "bold")).grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        fields['text'] = tk.Entry(window, width=40, font=("Arial", 10))
        fields['text'].insert(0, task.get("text", ""))
        fields['text'].grid(row=row, column=1, padx=10, pady=5)
        
        row += 1
        # theme
        tk.Label(window, text="Thème:", bg="#f0f0f0", 
                font=("Arial", 10)).grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        fields['theme'] = tk.Entry(window, width=40, font=("Arial", 10))
        fields['theme'].insert(0, task.get("theme", ""))
        fields['theme'].grid(row=row, column=1, padx=10, pady=5)
        
        row += 1
        # deadline
        tk.Label(window, text="Deadline (jj-mm-aaaa):", bg="#f0f0f0", 
                font=("Arial", 10)).grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        fields['deadline'] = tk.Entry(window, width=40, font=("Arial", 10))
        fields['deadline'].insert(0, task.get("deadline", ""))
        fields['deadline'].grid(row=row, column=1, padx=10, pady=5)
        
        row += 1
        # priorité
        tk.Label(window, text="Priorité (0-5):", bg="#f0f0f0", 
                font=("Arial", 10)).grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        fields['priority'] = tk.Spinbox(window, from_=0, to=5, width=38, font=("Arial", 10))
        fields['priority'].delete(0, tk.END)
        fields['priority'].insert(0, str(task.get("priority", 0)))
        fields['priority'].grid(row=row, column=1, padx=10, pady=5)
        
        row += 1
        # couleur
        tk.Label(window, text="Couleur:", bg="#f0f0f0", 
                font=("Arial", 10)).grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        fields['color'] = ttk.Combobox(window, width=37, font=("Arial", 10),
                                       values=list(self.colors.keys()))
        fields['color'].set(task.get("color", "normal"))
        fields['color'].grid(row=row, column=1, padx=10, pady=5)
        
        row += 1
        # statut
        fields['done'] = tk.BooleanVar(value=task.get("done", False))
        tk.Checkbutton(window, text="Marquer comme terminée", variable=fields['done'],
                      bg="#f0f0f0", font=("Arial", 10)).grid(row=row, column=0, 
                                                             columnspan=2, pady=10)
        
        row += 1
        # boutons validation/annulation
        btn_frame = tk.Frame(window, bg="#f0f0f0")
        btn_frame.grid(row=row, column=0, columnspan=2, pady=20)
        
        def save_changes():
            text = fields['text'].get().strip()
            if text:
                text = text[0].upper() + text[1:] if len(text) > 1 else text.upper()
                task["text"] = text
            
            theme = fields['theme'].get().strip()
            if theme:
                task["theme"] = theme
            
            # gestion de la deadline
            deadline_str = fields['deadline'].get().strip()
            original_deadline = task.get("deadline", "")
            
            # si la deadline a changé, on vérifie qu'elle n'est pas dans le passé
            if deadline_str != original_deadline:
                if deadline_str:
                    try:
                        deadline_date = datetime.strptime(deadline_str, "%d-%m-%Y").date()
                        if deadline_date < date.today():
                            messagebox.showerror("Erreur", "La nouvelle deadline ne peut pas être dans le passé")
                            return
                        task["deadline"] = deadline_str
                    except ValueError:
                        messagebox.showerror("Erreur", "Format de date invalide (jj-mm-aaaa)")
                        return
                else:
                    task["deadline"] = ""
            # si la deadline n'a pas changé, on la garde (meme si elle est dans le passé)
            
            try:
                task["priority"] = int(fields['priority'].get())
            except:
                pass
            
            color = fields['color'].get()
            if color:
                task["color"] = color
            
            task["done"] = fields['done'].get()
            
            self._reindex()
            self._save()
            window.destroy()
            self.refresh_display()
            messagebox.showinfo("Succès", "Tâche modifiée avec succès!")
        
        tk.Button(btn_frame, text="Enregistrer", command=save_changes,
                 bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                 padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Annuler", command=window.destroy,
                 bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                 padx=20, pady=5).pack(side=tk.LEFT, padx=5)
    
    def toggle_task_status(self):
        """change le statut d'une tâche (done/not done)"""
        task_id = self._select_task_id("Changer le statut d'une tâche")
        if task_id is None:
            return
        
        task = self.tasks_by_id.get(task_id)
        if not task:
            messagebox.showerror("Erreur", "Tâche introuvable!")
            return
        
        task["done"] = not task.get("done", False)
        self._reindex()
        self._save()
        self.refresh_display()
        
        status = "terminée" if task["done"] else "non terminée"
        messagebox.showinfo("Succès", f"Tâche marquée comme {status}!")
    
    def delete_task_window(self):
        """fenêtre pour supprimer une tâche"""
        task_id = self._select_task_id("Supprimer une tâche")
        if task_id is None:
            return
        
        task = self.tasks_by_id.get(task_id)
        if not task:
            messagebox.showerror("Erreur", "Tâche introuvable!")
            return
        
        confirm = messagebox.askyesno("Confirmation", 
                                      f"Êtes-vous sûr de vouloir supprimer la tâche:\n\n'{task.get('text', '')}'?")
        if confirm:
            self.tasks = [t for t in self.tasks if t["id"] != task_id]
            self._reindex()
            self._save()
            self.refresh_display()
            messagebox.showinfo("Succès", "Tâche supprimée avec succès!")
    
    def _select_task_id(self, title):
        """affiche une fenêtre pour sélectionner une tâche"""
        if not self.tasks:
            messagebox.showinfo("Info", "Aucune tâche disponible")
            return None
        
        window = tk.Toplevel(self.master)
        window.title(title)
        window.geometry("600x400")
        window.configure(bg="#f0f0f0")
        
        tk.Label(window, text="Sélectionnez une tâche:", 
                bg="#f0f0f0", font=("Arial", 12, "bold")).pack(pady=10)
        
        # liste des tâches
        frame = tk.Frame(window, bg="white")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, 
                            font=("Arial", 10), height=15)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        for task in self.tasks:
            status = "✅" if task.get("done", False) else "⏳"
            listbox.insert(tk.END, f"ID {task['id']}: {status} {task.get('text', '')}")
        
        selected_id = [None]
        
        def on_select():
            selection = listbox.curselection()
            if selection:
                selected_id[0] = self.tasks[selection[0]]["id"]
                window.destroy()
        
        btn_frame = tk.Frame(window, bg="#f0f0f0")
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Sélectionner", command=on_select,
                 bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                 padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Annuler", command=window.destroy,
                 bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                 padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        
        window.wait_window()
        return selected_id[0]
    
    def _select_from_list(self, title, items):
        """affiche une fenêtre pour sélectionner un élément dans une liste"""
        window = tk.Toplevel(self.master)
        window.title(title)
        window.geometry("400x300")
        window.configure(bg="#f0f0f0")
        
        tk.Label(window, text=title, 
                bg="#f0f0f0", font=("Arial", 12, "bold")).pack(pady=10)
        
        listbox = tk.Listbox(window, font=("Arial", 10), height=10)
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for item in items:
            listbox.insert(tk.END, item)
        
        selected = [None]
        
        def on_select():
            selection = listbox.curselection()
            if selection:
                selected[0] = items[selection[0]]
                window.destroy()
        
        btn_frame = tk.Frame(window, bg="#f0f0f0")
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Sélectionner", command=on_select,
                 bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                 padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Annuler", command=window.destroy,
                 bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                 padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        
        window.wait_window()
        return selected[0]
    
    def _ask_priority(self, title):
        """demande une priorité"""
        window = tk.Toplevel(self.master)
        window.title(title)
        window.geometry("300x150")
        window.configure(bg="#f0f0f0")
        
        tk.Label(window, text=title, 
                bg="#f0f0f0", font=("Arial", 12, "bold")).pack(pady=10)
        
        spinbox = tk.Spinbox(window, from_=0, to=5, font=("Arial", 14), width=10)
        spinbox.pack(pady=10)
        
        result: list[Optional[int]] = [None]
        
        def on_ok():
            try:
                result[0] = int(spinbox.get())
                window.destroy()
            except:
                messagebox.showerror("Erreur", "Valeur invalide!")
        
        btn_frame = tk.Frame(window, bg="#f0f0f0")
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="OK", command=on_ok,
                 bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                 padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Annuler", command=window.destroy,
                 bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                 padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        
        window.wait_window()
        return result[0]


def main():
    root = tk.Tk()
    app = TodoListGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()


