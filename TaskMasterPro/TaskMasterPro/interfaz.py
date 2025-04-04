import tkinter as tk
from tkinter import ttk, messagebox
from datos import cargar_tareas, guardar_tareas, crear_backup
from datetime import datetime

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("TaskMaster Pro")
        self.root.geometry("500x400")
        
        self.tasks = cargar_tareas()
        self.setup_ui()
        self.update_task_list()

    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Entrada de tarea
        self.task_entry = ttk.Entry(main_frame, width=40)
        self.task_entry.grid(row=0, column=0, padx=5, pady=5, sticky=tk.EW)
        
        # Botón agregar
        add_btn = ttk.Button(main_frame, text="➕ Agregar", command=self.add_task)
        add_btn.grid(row=0, column=1, padx=5, pady=5)
        
        # Lista de tareas
        self.task_listbox = tk.Listbox(
            main_frame, 
            width=50, 
            height=15,
            selectbackground="#a6a6a6",
            selectmode=tk.SINGLE
        )
        self.task_listbox.grid(row=1, column=0, columnspan=2, pady=10, sticky=tk.EW)
        
        # Frame de botones
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=5)
        
        complete_btn = ttk.Button(btn_frame, text="✅ Completar", command=self.toggle_task)
        complete_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = ttk.Button(btn_frame, text="🗑️ Eliminar", command=self.delete_task)
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        edit_btn = ttk.Button(btn_frame, text="✏️ Editar", command=self.edit_task)
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        # Configurar evento doble clic
        self.task_listbox.bind("<Double-1>", self.edit_task)

    def add_task(self):
        task_text = self.task_entry.get().strip()
        if not task_text:
            messagebox.showwarning("Advertencia", "La tarea no puede estar vacía")
            return
            
        new_task = {
            "id": len(self.tasks) + 1,
            "text": task_text,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "priority": "normal"
        }
        
        self.tasks.append(new_task)
        guardar_tareas(self.tasks)
        self.update_task_list()
        self.task_entry.delete(0, tk.END)

    def toggle_task(self):
        try:
            selection = self.task_listbox.curselection()[0]
            self.tasks[selection]["completed"] = not self.tasks[selection]["completed"]
            guardar_tareas(self.tasks)
            self.update_task_list()
        except IndexError:
            messagebox.showwarning("Advertencia", "Selecciona una tarea primero")

    def delete_task(self):
        try:
            selection = self.task_listbox.curselection()[0]
            del self.tasks[selection]
            guardar_tareas(self.tasks)
            self.update_task_list()
        except IndexError:
            messagebox.showwarning("Advertencia", "Selecciona una tarea primero")

    def edit_task(self, event=None):
        try:
            selection = self.task_listbox.curselection()[0]
            old_text = self.tasks[selection]["text"]
            
            # Ventana emergente para editar
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Editar Tarea")
            
            edit_entry = ttk.Entry(edit_window, width=40)
            edit_entry.pack(padx=10, pady=10)
            edit_entry.insert(0, old_text)
            edit_entry.focus()
            
            def save_edit():
                new_text = edit_entry.get().strip()
                if new_text:
                    self.tasks[selection]["text"] = new_text
                    guardar_tareas(self.tasks)
                    self.update_task_list()
                    edit_window.destroy()
            
            save_btn = ttk.Button(edit_window, text="Guardar", command=save_edit)
            save_btn.pack(pady=5)
            
        except IndexError:
            messagebox.showwarning("Advertencia", "Selecciona una tarea primero")

    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "✓" if task["completed"] else "✗"
            priority = f"[{task['priority'][0].upper()}] " if task["priority"] != "normal" else ""
            task_text = f"{status} {priority}{task['text']} ({task['created_at']})"
            self.task_listbox.insert(tk.END, task_text)
            
            if task["completed"]:
                self.task_listbox.itemconfig(tk.END, {'fg': 'green'})