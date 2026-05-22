import tkinter as tk
from tkinter import ttk, messagebox

class VentanaAgregarLibro(tk.Toplevel):
    def __init__(self, parent, sistema):
        super().__init__(parent)
        self.sistema = sistema
        self.title("Agregar Nuevo Libro")
        self.geometry("400x380")
        self.configure(bg="#1a2744")
        self.resizable(False, False)
        self.grab_set()

        self._crear_widgets()

    def _crear_widgets(self):
        tk.Label(self, text="➕ Nuevo Libro",
                 font=("Arial", 14, "bold"), bg="#1a2744", fg="#c8a951").pack(pady=20)

        frame = tk.Frame(self, bg="#243156", padx=25, pady=20)
        frame.pack(padx=25, fill="both", expand=True)

        campos = [("ID del Libro:", "id"), ("Título:", "titulo"),
                  ("Autor:", "autor")]

        self.entries = {}
        for label_text, key in campos:
            tk.Label(frame, text=label_text, font=("Arial", 9),
                     bg="#243156", fg="#c0d0e0", anchor="w").pack(fill="x")
            entry = tk.Entry(frame, font=("Arial", 10),
                             bg="#1a2744", fg="white",
                             insertbackground="white", relief="flat", bd=4)
            entry.pack(fill="x", pady=(2, 8), ipady=4)
            self.entries[key] = entry

        tk.Label(frame, text="Categoría:", font=("Arial", 9),
                 bg="#243156", fg="#c0d0e0", anchor="w").pack(fill="x")
        self.combo_categoria = ttk.Combobox(frame,
                                             values=["Programacion", "Matematicas", "Ciencias",
                                                     "Algoritmos", "Redes", "Literatura", "Historia"],
                                             state="readonly", font=("Arial", 10))
        self.combo_categoria.set("Programacion")
        self.combo_categoria.pack(fill="x", pady=(2, 15))

        tk.Button(frame, text="GUARDAR LIBRO",
                  font=("Arial", 11, "bold"),
                  bg="#c8a951", fg="#1a2744",
                  relief="flat", cursor="hand2",
                  command=self._guardar).pack(fill="x", ipady=7)

    def _guardar(self):
        id_libro = self.entries["id"].get().strip().upper()
        titulo = self.entries["titulo"].get().strip()
        autor = self.entries["autor"].get().strip()
        categoria = self.combo_categoria.get()

        if not id_libro or not titulo or not autor:
            messagebox.showwarning("Campos vacíos", "Todos los campos son requeridos", parent=self)
            return

        # verificar si el ID ya existe
        for libro in self.sistema.libros:
            if libro['id_libro'] == id_libro:
                messagebox.showerror("ID duplicado",
                                      f"Ya existe un libro con ID {id_libro}", parent=self)
                return

        nuevo_libro = {
            'id_libro': id_libro,
            'titulo': titulo,
            'autor': autor,
            'categoria': categoria,
            'disponibilidad': True
        }
        self.sistema.libros.append(nuevo_libro)
        self.sistema.guardar_datos()
        messagebox.showinfo("Guardado", f"Libro '{titulo}' agregado correctamente", parent=self)
        self.destroy()
