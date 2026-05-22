import tkinter as tk
from tkinter import ttk, messagebox

class VentanaLibros(tk.Toplevel):
    def __init__(self, parent, sistema, usuario):
        super().__init__(parent)
        self.parent = parent
        self.sistema = sistema
        self.usuario = usuario
        self.title("Gestión de Libros")
        self.geometry("750x520")
        self.configure(bg="#1a2744")

        self._crear_widgets()
        self._cargar_libros()

    def _crear_widgets(self):
        # header
        frame_top = tk.Frame(self, bg="#0f1a33", pady=10)
        frame_top.pack(fill="x")

        tk.Label(frame_top, text="📚  Biblioteca de Libros",
                 font=("Arial", 14, "bold"), bg="#0f1a33", fg="#c8a951").pack(side="left", padx=20)

        # busqueda
        frame_buscar = tk.Frame(frame_top, bg="#0f1a33")
        frame_buscar.pack(side="right", padx=20)

        self.entry_buscar = tk.Entry(frame_buscar, font=("Arial", 10),
                                      bg="#1a2744", fg="white",
                                      insertbackground="white",
                                      relief="flat", bd=3, width=25)
        self.entry_buscar.pack(side="left", ipady=4, padx=(0, 5))
        self.entry_buscar.insert(0, "Buscar libro o autor...")
        self.entry_buscar.bind("<FocusIn>", self._limpiar_placeholder)
        self.entry_buscar.bind("<Return>", lambda e: self._buscar())

        tk.Button(frame_buscar, text="🔍",
                  font=("Arial", 10), bg="#c8a951", fg="#1a2744",
                  relief="flat", cursor="hand2",
                  command=self._buscar).pack(side="left", ipady=4, padx=2)

        tk.Button(frame_buscar, text="Ver todos",
                  font=("Arial", 9), bg="#2d4070", fg="white",
                  relief="flat", cursor="hand2",
                  command=self._cargar_libros).pack(side="left", ipady=4, padx=2)

        # tabla de libros
        frame_tabla = tk.Frame(self, bg="#1a2744")
        frame_tabla.pack(fill="both", expand=True, padx=15, pady=10)

        columnas = ("ID", "Título", "Autor", "Categoría", "Disponibilidad")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas,
                                   show="headings", height=15)

        # estilo tabla
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                         background="#243156",
                         foreground="white",
                         fieldbackground="#243156",
                         rowheight=28)
        style.configure("Treeview.Heading",
                         background="#0f1a33",
                         foreground="#c8a951",
                         font=("Arial", 10, "bold"))
        style.map("Treeview", background=[("selected", "#3d5590")])

        for col in columnas:
            self.tabla.heading(col, text=col)

        self.tabla.column("ID", width=60, anchor="center")
        self.tabla.column("Título", width=220)
        self.tabla.column("Autor", width=160)
        self.tabla.column("Categoría", width=120)
        self.tabla.column("Disponibilidad", width=100, anchor="center")

        scroll = ttk.Scrollbar(frame_tabla, orient="vertical",
                                command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # botones de accion
        frame_botones = tk.Frame(self, bg="#1a2744")
        frame_botones.pack(fill="x", padx=15, pady=(0, 15))

        tk.Button(frame_botones, text="📖 Solicitar Préstamo",
                  font=("Arial", 10), bg="#c8a951", fg="#1a2744",
                  relief="flat", cursor="hand2", padx=15, pady=7,
                  command=self._solicitar_prestamo).pack(side="left", padx=5)

        tk.Button(frame_botones, text=" Devolver Libro",
                  font=("Arial", 10), bg="#2d4070", fg="white",
                  relief="flat", cursor="hand2", padx=15, pady=7,
                  command=self._devolver_libro).pack(side="left", padx=5)

        if self.usuario.get('tipo') == 'admin':
            tk.Button(frame_botones, text=" Agregar Libro",
                      font=("Arial", 10), bg="#2d6040", fg="white",
                      relief="flat", cursor="hand2", padx=15, pady=7,
                      command=self._agregar_libro).pack(side="left", padx=5)

        # label status
        self.lbl_status = tk.Label(self, text="",
                                    font=("Arial", 9), bg="#1a2744", fg="#80c080")
        self.lbl_status.pack()

    def _limpiar_placeholder(self, event):
        if self.entry_buscar.get() == "Buscar libro o autor...":
            self.entry_buscar.delete(0, tk.END)

    def _cargar_libros(self, libros=None):
        # limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        if libros is None:
            libros = self.sistema.libros

        for libro in libros:
            disponible = "✅ Disponible" if libro['disponibilidad'] else "❌ Prestado"
            self.tabla.insert("", "end", values=(
                libro['id_libro'],
                libro['titulo'],
                libro['autor'],
                libro['categoria'],
                disponible
            ))

        self.lbl_status.config(text=f"Mostrando {len(libros)} libro(s)")

    def _buscar(self):
        termino = self.entry_buscar.get().strip()
        if termino == "Buscar libro o autor..." or not termino:
            self._cargar_libros()
            return
        resultados = self.sistema.buscar_libros(termino)
        self._cargar_libros(resultados)
        if not resultados:
            messagebox.showinfo("Sin resultados",
                                f"No se encontraron libros con '{termino}'", parent=self)

    def _solicitar_prestamo(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Selecciona un libro",
                                   "Primero selecciona un libro de la lista", parent=self)
            return

        item = self.tabla.item(seleccion[0])
        id_libro = item['values'][0]
        titulo = item['values'][1]
        disponible = item['values'][4]

        if "Prestado" in disponible:
            messagebox.showerror("No disponible",
                                  f"El libro '{titulo}' no está disponible", parent=self)
            return

        confirm = messagebox.askyesno("Confirmar Préstamo",
                                       f"¿Deseas solicitar préstamo de:\n'{titulo}'?", parent=self)
        if confirm:
            ok, msg = self.sistema.prestar_libro(id_libro, self.usuario['matricula'])
            if ok:
                messagebox.showinfo("Préstamo exitoso", msg, parent=self)
                self._cargar_libros()
            else:
                messagebox.showerror("Error", msg, parent=self)

    def _devolver_libro(self):
        # abrir ventana de devolucion
        from interfaces.ventana_devolucion import VentanaDevolucion
        VentanaDevolucion(self, self.sistema, self.usuario)
        self._cargar_libros()  # esto tiene un bug: recarga antes de que devuelvan

    def _agregar_libro(self):
        from interfaces.ventana_agregar_libro import VentanaAgregarLibro
        VentanaAgregarLibro(self, self.sistema)
        self.after(500, self._cargar_libros)  # esperar un poco y recargar
