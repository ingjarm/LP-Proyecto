import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

# Archivo de almacenamiento
db_file = "tasks.json"

class TaskManager:
    def _init_(self):
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if os.path.exists(db_file):
            with open(db_file, "r") as file:
                return json.load(file)
        return []

    def save_tasks(self):
        with open(db_file, "w") as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self, title, description, due_date, priority):
        task = {
            "title": title,
            "description": description,
            "due_date": due_date,
            "priority": priority,
            "completed": False
        }
        self.tasks.append(task)
        self.save_tasks()

    def delete_task(self, index):
        del self.tasks[index]
        self.save_tasks()

    def mark_completed(self, index):
        self.tasks[index]["completed"] = True
        self.save_tasks()

# Interfaz Gráfica
class TaskApp:
    def _init_(self, root):
        self.manager = TaskManager()
        self.root = root
        self.root.title("Gestor de Tareas")
        self.create_widgets()
        self.populate_tasks()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.root, columns=("#1", "#2", "#3", "#4"), show="headings")
        self.tree.heading("#1", text="Título")
        self.tree.heading("#2", text="Descripción")
        self.tree.heading("#3", text="Fecha Vencimiento")
        self.tree.heading("#4", text="Prioridad")
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        self.btn_add = tk.Button(self.root, text="Agregar Tarea", command=self.add_task)
        self.btn_add.pack()

        self.btn_delete = tk.Button(self.root, text="Eliminar Tarea", command=self.delete_task)
        self.btn_delete.pack()

        self.btn_complete = tk.Button(self.root, text="Marcar Completada", command=self.mark_completed)
        self.btn_complete.pack()

    def populate_tasks(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for idx, task in enumerate(self.manager.tasks):
            self.tree.insert("", "end", iid=idx, values=(task["title"], task["description"], task["due_date"], task["priority"]))

    def add_task(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Nueva Tarea")

        tk.Label(new_window, text="Título:").pack()
        title_entry = tk.Entry(new_window)
        title_entry.pack()
        
        tk.Label(new_window, text="Descripción:").pack()
        desc_entry = tk.Entry(new_window)
        desc_entry.pack()
        
        tk.Label(new_window, text="Fecha Vencimiento (YYYY-MM-DD):").pack()
        date_entry = tk.Entry(new_window)
        date_entry.pack()
        
        tk.Label(new_window, text="Prioridad:").pack()
        priority_entry = tk.Entry(new_window)
        priority_entry.pack()
        
        def save_new_task():
            title = title_entry.get()
            description = desc_entry.get()
            due_date = date_entry.get()
            priority = priority_entry.get()
            if title and due_date:
                self.manager.add_task(title, description, due_date, priority)
                self.populate_tasks()
                new_window.destroy()
            else:
                messagebox.showerror("Error", "Título y fecha de vencimiento son obligatorios")
        
        tk.Button(new_window, text="Guardar", command=save_new_task).pack()

    def delete_task(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione una tarea para eliminar")
            return
        index = int(selected_item[0])
        self.manager.delete_task(index)
        self.populate_tasks()

    def mark_completed(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione una tarea para marcar como completada")
            return
        index = int(selected_item[0])
        self.manager.mark_completed(index)
        self.populate_tasks()

if __name__ == "_main_":
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()