import tkinter as tk
from tkinter import ttk, messagebox

class VentanaDevolucion(tk.Toplevel):
    def __init__(self, parent, sistema, usuario):
        super().__init__(parent)
        self.sistema = sistema
        self.usuario = usuario
        self.title("Devolver Libro")
        self.geometry("600x400")
        self.configure(bg="#1a2744")
        self.grab_set()

        self._crear_widgets()
        self._cargar_prestamos()

    def _crear_widgets(self):
        tk.Label(self, text="↩️ Devolución de Libros",
                 font=("Arial", 14, "bold"), bg="#1a2744", fg="#c8a951").pack(pady=15)

        tk.Label(self, text="Selecciona el préstamo a devolver:",
                 font=("Arial", 9), bg="#1a2744", fg="#a0b0c0").pack()

        frame_tabla = tk.Frame(self, bg="#1a2744")
        frame_tabla.pack(fill="both", expand=True, padx=15, pady=10)

        columnas = ("ID Préstamo", "Libro", "Fecha Préstamo", "Estado")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=10)

        for col in columnas:
            self.tabla.heading(col, text=col)

        self.tabla.column("ID Préstamo", width=100, anchor="center")
        self.tabla.column("Libro", width=220)
        self.tabla.column("Fecha Préstamo", width=120, anchor="center")
        self.tabla.column("Estado", width=100, anchor="center")

        scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        frame_btns = tk.Frame(self, bg="#1a2744")
        frame_btns.pack(pady=10)

        tk.Button(frame_btns, text="✅ Confirmar Devolución",
                  font=("Arial", 10, "bold"), bg="#c8a951", fg="#1a2744",
                  relief="flat", cursor="hand2", padx=15, pady=7,
                  command=self._devolver).pack(side="left", padx=5)

        tk.Button(frame_btns, text="❌ Cerrar",
                  font=("Arial", 10), bg="#2d4070", fg="white",
                  relief="flat", cursor="hand2", padx=15, pady=7,
                  command=self.destroy).pack(side="left", padx=5)

    def _cargar_prestamos(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        prestamos = self.sistema.get_prestamos_usuario(self.usuario['matricula'])
        # solo mostrar los activos
        prestamos_activos = [p for p in prestamos if p['estado'] == 'prestado']

        for p in prestamos_activos:
            # buscar titulo del libro
            titulo = p['id_libro']
            for libro in self.sistema.libros:
                if libro['id_libro'] == p['id_libro']:
                    titulo = libro['titulo']
                    break

            self.tabla.insert("", "end", values=(
                p['id_prestamo'], titulo, p['fecha_prestamo'], p['estado']
            ))

        if not prestamos_activos:
            tk.Label(self, text="No tienes préstamos activos",
                     font=("Arial", 10), bg="#1a2744", fg="#809aaa").pack()

    def _devolver(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Selecciona", "Selecciona un préstamo para devolver", parent=self)
            return

        item = self.tabla.item(seleccion[0])
        id_prestamo = item['values'][0]

        ok, msg = self.sistema.devolver_libro(id_prestamo)
        if ok:
            messagebox.showinfo("Devuelto", "¡Libro devuelto correctamente!", parent=self)
            self._cargar_prestamos()
        else:
            messagebox.showerror("Error", msg, parent=self)
