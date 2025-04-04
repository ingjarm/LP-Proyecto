import tkinter as tk
from interfaz import TaskManager

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()