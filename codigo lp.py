import tkinter as tk
from tkinter import messagebox
import json

# Archivo donde se almacenarán las tareas
TASKS_FILE = "tareas.json"

# Cargar tareas desde JSON
def cargar_tareas():
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Guardar tareas en JSON
def guardar_tareas(tareas):
    with open(TASKS_FILE, "w") as f:
        json.dump(tareas, f, indent=4)

# Agregar nueva tarea
def agregar_tarea():
    tarea = entrada_tarea.get()
    if tarea:
        tareas.append({"tarea": tarea, "completada": False})
        guardar_tareas(tareas)
        actualizar_lista()
        entrada_tarea.delete(0, tk.END)
    else:
        messagebox.showwarning("Advertencia", "No puedes agregar una tarea vacía")

# Marcar tarea como completada
def completar_tarea():
    try:
        seleccion = lista_tareas.curselection()[0]
        tareas[seleccion]["completada"] = not tareas[seleccion]["completada"]
        guardar_tareas(tareas)
        actualizar_lista()
    except IndexError:
        messagebox.showwarning("Advertencia", "Selecciona una tarea para marcar")

# Eliminar tarea
def eliminar_tarea():
    try:
        seleccion = lista_tareas.curselection()[0]
        del tareas[seleccion]
        guardar_tareas(tareas)
        actualizar_lista()
    except IndexError:
        messagebox.showwarning("Advertencia", "Selecciona una tarea para eliminar")

# Actualizar la lista de tareas
def actualizar_lista():
    lista_tareas.delete(0, tk.END)
    for tarea in tareas:
        estado = "✔" if tarea["completada"] else "✖"
        lista_tareas.insert(tk.END, f"{estado} {tarea['tarea']}")

# Configuración de la interfaz
tareas = cargar_tareas()
root = tk.Tk()
root.title("Gestor de Tareas")

entrada_tarea = tk.Entry(root, width=40)
entrada_tarea.pack(pady=10)

btn_agregar = tk.Button(root, text="Agregar Tarea", command=agregar_tarea)
btn_agregar.pack()

lista_tareas = tk.Listbox(root, width=50, height=10)
lista_tareas.pack(pady=10)

btn_completar = tk.Button(root, text="Marcar Completada", command=completar_tarea)
btn_completar.pack()

btn_eliminar = tk.Button(root, text="Eliminar Tarea", command=eliminar_tarea)
btn_eliminar.pack()

actualizar_lista()
root.mainloop()
