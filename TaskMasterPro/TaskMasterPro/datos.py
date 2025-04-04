import json
import os
from datetime import datetime

def cargar_tareas():
    try:
        if not os.path.exists("tasks.json"):
            return []
            
        with open("tasks.json", "r") as f:
            tasks = json.load(f)
            if not all(isinstance(task, dict) for task in tasks):
                raise ValueError("Formato de archivo inválido")
            return tasks
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        messagebox.showwarning("Error", f"No se pudieron cargar las tareas: {str(e)}")
        return []

def guardar_tareas(tasks):
    try:
        crear_backup()
        with open("tasks.json", "w") as f:
            json.dump(tasks, f, indent=4, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron guardar las tareas: {str(e)}")

def crear_backup():
    backup_dir = "backups"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_dir, f"tasks_backup_{timestamp}.json")
    
    try:
        with open(backup_file, "w") as f:
            json.dump(cargar_tareas(), f, indent=4)
    except Exception as e:
        messagebox.showwarning("Backup", f"No se pudo crear el backup: {str(e)}")