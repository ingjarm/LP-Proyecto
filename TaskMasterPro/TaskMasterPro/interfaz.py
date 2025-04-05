import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, timedelta
from datos import guardar_tareas, cargar_tareas

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.tareas = cargar_tareas()
        self.setup_ui()
        
    def setup_ui(self):
        # Configuración de estilo
        style = ttk.Style()
        style.configure("TFrame", background="#f5f5f5")
        style.configure("TLabel", background="#f5f5f5", font=('Helvetica', 10, 'bold'))
        style.configure("TButton", padding=5, font=('Helvetica', 9))
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame de entrada
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        self.entrada_tarea = ttk.Entry(input_frame, width=50, font=('Helvetica', 12))
        self.entrada_tarea.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        btn_agregar = ttk.Button(input_frame, text="➕ Agregar", command=self.agregar_tarea)
        btn_agregar.pack(side=tk.LEFT, padx=5)
        
        # Selector de estado
        self.estado_var = tk.StringVar(value="no_hecha")
        estados_frame = ttk.Frame(main_frame)
        estados_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(estados_frame, text="Estado:").pack(side=tk.LEFT)
        for texto, valor in [("❌ No hecha", "no_hecha"), ("⏳ Pendiente", "pendiente"), ("✅ Hecha", "hecha")]:
            rb = ttk.Radiobutton(estados_frame, text=texto, variable=self.estado_var, value=valor)
            rb.pack(side=tk.LEFT, padx=5)
        
        # Frames para las tareas
        tasks_frame = ttk.Frame(main_frame)
        tasks_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear tres secciones con Notebook (pestañas)
        notebook = ttk.Notebook(tasks_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña No hechas
        tab_no_hechas = ttk.Frame(notebook)
        notebook.add(tab_no_hechas, text="❌ No Hechas")
        self.lista_no_hechas = tk.Listbox(
            tab_no_hechas,
            width=60,
            height=10,
            font=('Helvetica', 11),
            selectbackground="#a6d8ff",
            bg="#ffe6e6"  # Rojo claro
        )
        self.lista_no_hechas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Pestaña Pendientes
        tab_pendientes = ttk.Frame(notebook)
        notebook.add(tab_pendientes, text="⏳ Pendientes")
        self.lista_pendientes = tk.Listbox(
            tab_pendientes,
            width=60,
            height=10,
            font=('Helvetica', 11),
            selectbackground="#a6d8ff",
            bg="#fffae6"  # Amarillo claro
        )
        self.lista_pendientes.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Pestaña Hechas
        tab_hechas = ttk.Frame(notebook)
        notebook.add(tab_hechas, text="✅ Hechas")
        self.lista_hechas = tk.Listbox(
            tab_hechas,
            width=60,
            height=10,
            font=('Helvetica', 11),
            selectbackground="#a6d8ff",
            bg="#e6ffe6"  # Verde claro
        )
        self.lista_hechas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame de botones
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="✏️ Editar", command=self.editar_tarea).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🗑️ Eliminar", command=self.eliminar_tarea).pack(side=tk.LEFT, padx=5)
        
        self.actualizar_lista()
        
        # Configurar eventos doble click para editar en todas las listas
        for lista in [self.lista_no_hechas, self.lista_pendientes, self.lista_hechas]:
            lista.bind("<Double-1>", self.editar_tarea)
    
    def agregar_tarea(self):
        texto = self.entrada_tarea.get().strip()
        if texto:
            nueva_tarea = {
                "texto": texto,
                "estado": self.estado_var.get(),
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "vencimiento": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
            }
            self.tareas.append(nueva_tarea)
            guardar_tareas(self.tareas)
            self.actualizar_lista()
            self.entrada_tarea.delete(0, tk.END)
    
    def actualizar_lista(self):
        # Limpiar todas las listas
        for lista in [self.lista_no_hechas, self.lista_pendientes, self.lista_hechas]:
            lista.delete(0, tk.END)
        
        # Organizar tareas por estado
        for tarea in self.tareas:
            texto = f"{tarea['texto']} (Vence: {tarea['vencimiento']})"
            
            if tarea["estado"] == "no_hecha":
                self.lista_no_hechas.insert(tk.END, texto)
            elif tarea["estado"] == "pendiente":
                self.lista_pendientes.insert(tk.END, texto)
            elif tarea["estado"] == "hecha":
                self.lista_hechas.insert(tk.END, texto)
    
    def obtener_tarea_seleccionada(self):
        # Determinar en qué lista está la selección
        for lista, estado in [
            (self.lista_no_hechas, "no_hecha"),
            (self.lista_pendientes, "pendiente"),
            (self.lista_hechas, "hecha")
        ]:
            seleccion = lista.curselection()
            if seleccion:
                # Encontrar la tarea correspondiente en self.tareas
                texto_lista = lista.get(seleccion[0])
                for i, tarea in enumerate(self.tareas):
                    if tarea["estado"] == estado and f"{tarea['texto']} (Vence: {tarea['vencimiento']})" == texto_lista:
                        return i, tarea
        return None, None
    
    def editar_tarea(self, event=None):
        indice, tarea = self.obtener_tarea_seleccionada()
        if tarea:
            ventana_editar = tk.Toplevel(self.root)
            ventana_editar.title("Editar Tarea")
            
            tk.Label(ventana_editar, text="Texto:").pack()
            entrada_edit = ttk.Entry(ventana_editar, width=40)
            entrada_edit.insert(0, tarea["texto"])
            entrada_edit.pack()
            
            tk.Label(ventana_editar, text="Estado:").pack()
            estado_edit = ttk.Combobox(ventana_editar, values=["hecha", "no_hecha", "pendiente"])
            estado_edit.set(tarea["estado"])
            estado_edit.pack()
            
            def guardar_cambios():
                tarea["texto"] = entrada_edit.get()
                tarea["estado"] = estado_edit.get()
                guardar_tareas(self.tareas)
                self.actualizar_lista()
                ventana_editar.destroy()
            
            ttk.Button(ventana_editar, text="Guardar", command=guardar_cambios).pack(pady=5)
    
    def eliminar_tarea(self):
        indice, _ = self.obtener_tarea_seleccionada()
        if indice is not None:
            self.tareas.pop(indice)
            guardar_tareas(self.tareas)
            self.actualizar_lista()