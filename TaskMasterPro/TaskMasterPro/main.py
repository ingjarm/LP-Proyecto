import tkinter as tk
from tkinter import ttk
from interfaz import TaskManager

if __name__ == "__main__":
    root = tk.Tk()
    root.title("TaskMaster Pro+ - Organizador de Tareas")
    root.geometry("800x600")
    root.configure(bg="#f0f0f0")
    
    # Estilo mejorado
    style = ttk.Style()
    style.theme_use("clam")
    
    # Configurar colores
    style.configure("TNotebook", background="#f5f5f5")
    style.configure("TNotebook.Tab", padding=[10, 5], font=('Helvetica', 10, 'bold'))
    style.map("TNotebook.Tab", 
             background=[("selected", "#f5f5f5"), ("!selected", "#e0e0e0")],
             foreground=[("selected", "black"), ("!selected", "#555555")])
    
    app = TaskManager(root)
    
    # Centrar la ventana
    root.eval('tk::PlaceWindow . center')
    
    root.mainloop()