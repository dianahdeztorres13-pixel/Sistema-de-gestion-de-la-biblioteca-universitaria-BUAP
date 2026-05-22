import tkinter as tk
from tkinter import ttk, messagebox

class VentanaAdmin(tk.Toplevel):
    def __init__(self, parent, sistema):
        super().__init__(parent)
        self.sistema = sistema
        self.title("Panel de Administración")
        self.geometry("750x520")
        self.configure(bg="#1a2744")

        self._crear_widgets()
        self._cargar_usuarios()

    def _crear_widgets(self):
        frame_top = tk.Frame(self, bg="#0f1a33", pady=10)
        frame_top.pack(fill="x")

        tk.Label(frame_top, text="🔧 Panel de Administración",
                 font=("Arial", 14, "bold"), bg="#0f1a33", fg="#c8a951").pack(side="left", padx=20)

        # tabs
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=15, pady=10)

        # Tab usuarios
        self.frame_usuarios = tk.Frame(notebook, bg="#1a2744")
        notebook.add(self.frame_usuarios, text="👥 Usuarios")
        self._tab_usuarios(self.frame_usuarios)

        # Tab libros admin
        frame_libros_admin = tk.Frame(notebook, bg="#1a2744")
        notebook.add(frame_libros_admin, text="📚 Gestión Libros")
        self._tab_libros_admin(frame_libros_admin)

        # Tab espacios admin
        frame_esp_admin = tk.Frame(notebook, bg="#1a2744")
        notebook.add(frame_esp_admin, text="🏠 Gestión Espacios")
        self._tab_espacios_admin(frame_esp_admin)

    def _tab_usuarios(self, frame):
        frame_tabla = tk.Frame(frame, bg="#1a2744")
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        cols = ("Matrícula", "Nombre", "Correo", "Tipo")
        self.tabla_usuarios = ttk.Treeview(frame_tabla, columns=cols,
                                            show="headings", height=12)
        for col in cols:
            self.tabla_usuarios.heading(col, text=col)

        self.tabla_usuarios.column("Matrícula", width=100, anchor="center")
        self.tabla_usuarios.column("Nombre", width=200)
        self.tabla_usuarios.column("Correo", width=200)
        self.tabla_usuarios.column("Tipo", width=100, anchor="center")

        scroll = ttk.Scrollbar(frame_tabla, orient="vertical",
                                command=self.tabla_usuarios.yview)
        self.tabla_usuarios.configure(yscrollcommand=scroll.set)
        self.tabla_usuarios.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        frame_btns = tk.Frame(frame, bg="#1a2744")
        frame_btns.pack(pady=8)

        tk.Button(frame_btns, text="🗑️ Eliminar Usuario",
                  font=("Arial", 10), bg="#803030", fg="white",
                  relief="flat", cursor="hand2", padx=12, pady=6,
                  command=self._eliminar_usuario).pack(side="left", padx=5)

        tk.Button(frame_btns, text="🔄 Actualizar",
                  font=("Arial", 10), bg="#2d4070", fg="white",
                  relief="flat", cursor="hand2", padx=12, pady=6,
                  command=self._cargar_usuarios).pack(side="left", padx=5)

    def _tab_libros_admin(self, frame):
        tk.Label(frame, text="Gestión completa de libros",
                 font=("Arial", 11), bg="#1a2744", fg="#c0d0e0").pack(pady=20)

        frame_btns = tk.Frame(frame, bg="#1a2744")
        frame_btns.pack()

        tk.Button(frame_btns, text="➕ Agregar Libro",
                  font=("Arial", 10), bg="#2d6040", fg="white",
                  relief="flat", cursor="hand2", padx=15, pady=8,
                  command=self._agregar_libro).pack(side="left", padx=10)

        tk.Button(frame_btns, text="🗑️ Eliminar Libro Seleccionado",
                  font=("Arial", 10), bg="#803030", fg="white",
                  relief="flat", cursor="hand2", padx=15, pady=8,
                  command=self._eliminar_libro).pack(side="left", padx=10)

        frame_t = tk.Frame(frame, bg="#1a2744")
        frame_t.pack(fill="both", expand=True, padx=10, pady=10)

        cols = ("ID", "Título", "Autor", "Categoría", "Disponible")
        self.tabla_libros_admin = ttk.Treeview(frame_t, columns=cols,
                                                show="headings", height=10)
        for col in cols:
            self.tabla_libros_admin.heading(col, text=col)

        for libro in self.sistema.libros:
            self.tabla_libros_admin.insert("", "end", values=(
                libro['id_libro'], libro['titulo'], libro['autor'],
                libro['categoria'], "✅" if libro['disponibilidad'] else "❌"
            ))

        scroll2 = ttk.Scrollbar(frame_t, orient="vertical",
                                  command=self.tabla_libros_admin.yview)
        self.tabla_libros_admin.configure(yscrollcommand=scroll2.set)
        self.tabla_libros_admin.pack(side="left", fill="both", expand=True)
        scroll2.pack(side="right", fill="y")

    def _tab_espacios_admin(self, frame):
        tk.Label(frame, text="Gestión de Espacios Físicos",
                 font=("Arial", 11), bg="#1a2744", fg="#c0d0e0").pack(pady=15)

        frame_t = tk.Frame(frame, bg="#1a2744")
        frame_t.pack(fill="both", expand=True, padx=10, pady=5)

        cols = ("ID", "Tipo", "Capacidad", "Disponible")
        tabla_esp = ttk.Treeview(frame_t, columns=cols, show="headings", height=10)
        for col in cols:
            tabla_esp.heading(col, text=col)

        for esp in self.sistema.espacios:
            tabla_esp.insert("", "end", values=(
                esp['id_espacio'], esp['tipo'].capitalize(), esp['capacidad'],
                "✅" if esp['disponibilidad'] else "❌"
            ))

        scroll3 = ttk.Scrollbar(frame_t, orient="vertical", command=tabla_esp.yview)
        tabla_esp.configure(yscrollcommand=scroll3.set)
        tabla_esp.pack(side="left", fill="both", expand=True)
        scroll3.pack(side="right", fill="y")

        # boton para resetear disponibilidad (util en admin)
        tk.Button(frame, text="🔄 Liberar todos los espacios",
                  font=("Arial", 10), bg="#1d4060", fg="white",
                  relief="flat", cursor="hand2", padx=15, pady=7,
                  command=self._liberar_espacios).pack(pady=10)

    def _cargar_usuarios(self):
        for item in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(item)
        for u in self.sistema.usuarios:
            self.tabla_usuarios.insert("", "end", values=(
                u['matricula'], u['nombre'], u.get('correo', ''), u.get('tipo', '')
            ))

    def _eliminar_usuario(self):
        seleccion = self.tabla_usuarios.selection()
        if not seleccion:
            messagebox.showwarning("Selecciona", "Selecciona un usuario", parent=self)
            return

        item = self.tabla_usuarios.item(seleccion[0])
        matricula = item['values'][0]

        if matricula == "admin":
            messagebox.showerror("Error", "No puedes eliminar al administrador", parent=self)
            return

        if messagebox.askyesno("Confirmar", f"¿Eliminar usuario {matricula}?", parent=self):
            self.sistema.usuarios = [u for u in self.sistema.usuarios if u['matricula'] != matricula]
            self.sistema.guardar_datos()
            self._cargar_usuarios()
            messagebox.showinfo("Eliminado", "Usuario eliminado", parent=self)

    def _agregar_libro(self):
        from interfaces.ventana_agregar_libro import VentanaAgregarLibro
        VentanaAgregarLibro(self, self.sistema)

    def _eliminar_libro(self):
        seleccion = self.tabla_libros_admin.selection()
        if not seleccion:
            messagebox.showwarning("Selecciona", "Selecciona un libro", parent=self)
            return
        item = self.tabla_libros_admin.item(seleccion[0])
        id_libro = item['values'][0]

        if messagebox.askyesno("Confirmar", f"¿Eliminar libro {id_libro}?", parent=self):
            self.sistema.libros = [l for l in self.sistema.libros if l['id_libro'] != id_libro]
            self.sistema.guardar_datos()
            # refrescar tabla - pero no refresca la de admin, bug de estudiante
            messagebox.showinfo("Eliminado", "Libro eliminado (reinicia la ventana para ver cambios)", parent=self)

    def _liberar_espacios(self):
        if messagebox.askyesno("Confirmar", "¿Liberar todos los espacios?", parent=self):
            for esp in self.sistema.espacios:
                esp['disponibilidad'] = True
            self.sistema.guardar_datos()
            messagebox.showinfo("Listo", "Todos los espacios están libres ahora", parent=self)
