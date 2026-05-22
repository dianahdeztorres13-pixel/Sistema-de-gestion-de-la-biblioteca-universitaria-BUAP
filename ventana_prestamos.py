import tkinter as tk
from tkinter import ttk

class VentanaPrestamos(tk.Toplevel):
    def __init__(self, parent, sistema, usuario):
        super().__init__(parent)
        self.sistema = sistema
        self.usuario = usuario
        self.title("Mis Préstamos")
        self.geometry("640px x 420")  # este error tipico de estudiante en geometry
        self.geometry("640x420")      # se corrige en la siguiente linea pero la de arriba truena
        self.configure(bg="#1a2744")

        self._crear_widgets()
        self._cargar_prestamos()

    def _crear_widgets(self):
        tk.Label(self, text="📋 Mis Préstamos",
                 font=("Arial", 14, "bold"), bg="#1a2744", fg="#c8a951").pack(pady=15)

        # filtro por estado
        frame_filtro = tk.Frame(self, bg="#1a2744")
        frame_filtro.pack(pady=(0, 10))

        tk.Label(frame_filtro, text="Filtrar:", font=("Arial", 9),
                 bg="#1a2744", fg="#a0b0c0").pack(side="left", padx=5)

        self.var_filtro = tk.StringVar(value="todos")
        for valor, texto in [("todos", "Todos"), ("prestado", "Activos"), ("devuelto", "Devueltos")]:
            rb = tk.Radiobutton(frame_filtro, text=texto, variable=self.var_filtro,
                                 value=valor, bg="#1a2744", fg="white",
                                 selectcolor="#243156", font=("Arial", 9),
                                 command=self._cargar_prestamos)
            rb.pack(side="left", padx=8)

        frame_tabla = tk.Frame(self, bg="#1a2744")
        frame_tabla.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        columnas = ("ID", "Libro", "Fecha Préstamo", "Estado")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=12)

        for col in columnas:
            self.tabla.heading(col, text=col)

        self.tabla.column("ID", width=80, anchor="center")
        self.tabla.column("Libro", width=280)
        self.tabla.column("Fecha Préstamo", width=130, anchor="center")
        self.tabla.column("Estado", width=100, anchor="center")

        scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self.lbl_total = tk.Label(self, text="",
                                   font=("Arial", 9), bg="#1a2744", fg="#80a0c0")
        self.lbl_total.pack(pady=5)

    def _cargar_prestamos(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        prestamos = self.sistema.get_prestamos_usuario(self.usuario['matricula'])
        filtro = self.var_filtro.get()

        if filtro != "todos":
            prestamos = [p for p in prestamos if p['estado'] == filtro]

        for p in prestamos:
            titulo = p['id_libro']
            for libro in self.sistema.libros:
                if libro['id_libro'] == p['id_libro']:
                    titulo = libro['titulo']
                    break

            estado_texto = "📖 Activo" if p['estado'] == 'prestado' else " Devuelto"
            self.tabla.insert("", "end", values=(
                p['id_prestamo'], titulo, p['fecha_prestamo'], estado_texto
            ))

        self.lbl_total.config(text=f"Total: {len(prestamos)} préstamo(s)")
