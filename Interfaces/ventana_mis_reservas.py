import tkinter as tk
from tkinter import ttk, messagebox

class VentanaMisReservas(tk.Toplevel):
    def __init__(self, parent, sistema, usuario):
        super().__init__(parent)
        self.sistema = sistema
        self.usuario = usuario
        self.title("Mis Reservas")
        self.geometry("680x430")
        self.configure(bg="#1a2744")

        self._crear_widgets()
        self._cargar_reservas()

    def _crear_widgets(self):
        tk.Label(self, text=" Mis Reservas de Espacios",
                 font=("Arial", 14, "bold"), bg="#1a2744", fg="#c8a951").pack(pady=15)

        frame_tabla = tk.Frame(self, bg="#1a2744")
        frame_tabla.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        columnas = ("ID Reserva", "Espacio", "Tipo", "Fecha", "Hora", "Estado")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=12)

        for col in columnas:
            self.tabla.heading(col, text=col)

        self.tabla.column("ID Reserva", width=80, anchor="center")
        self.tabla.column("Espacio", width=80, anchor="center")
        self.tabla.column("Tipo", width=100, anchor="center")
        self.tabla.column("Fecha", width=100, anchor="center")
        self.tabla.column("Hora", width=70, anchor="center")
        self.tabla.column("Estado", width=100, anchor="center")

        scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        frame_btns = tk.Frame(self, bg="#1a2744")
        frame_btns.pack(pady=10)

        tk.Button(frame_btns, text=" Cancelar Reserva",
                  font=("Arial", 10), bg="#803030", fg="white",
                  relief="flat", cursor="hand2", padx=15, pady=7,
                  command=self._cancelar_reserva).pack(side="left", padx=5)

        tk.Button(frame_btns, text=" Actualizar",
                  font=("Arial", 10), bg="#2d4070", fg="white",
                  relief="flat", cursor="hand2", padx=15, pady=7,
                  command=self._cargar_reservas).pack(side="left", padx=5)

    def _cargar_reservas(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        reservas = self.sistema.get_reservas_usuario(self.usuario['matricula'])

        for r in reservas:
            # buscar tipo del espacio
            tipo = r['id_espacio']
            for espacio in self.sistema.espacios:
                if espacio['id_espacio'] == r['id_espacio']:
                    tipo = espacio['tipo'].capitalize()
                    break

            estado_icono = {
                "activa": " Activa",
                "cancelada": " Cancelada",
                "finalizada": " Finalizada"
            }.get(r['estado'], r['estado'])

            self.tabla.insert("", "end", values=(
                r['id_reserva'], r['id_espacio'], tipo,
                r['fecha'], r['hora'], estado_icono
            ))

        if not reservas:
            tk.Label(self, text="No tienes reservas registradas",
                     font=("Arial", 10), bg="#1a2744", fg="#809aaa").pack()

    def _cancelar_reserva(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Selecciona", "Selecciona una reserva para cancelar", parent=self)
            return

        item = self.tabla.item(seleccion[0])
        id_reserva = item['values'][0]
        estado = item['values'][5]

        if "Cancelada" in str(estado):
            messagebox.showinfo("Ya cancelada", "Esta reserva ya está cancelada", parent=self)
            return

        confirm = messagebox.askyesno("Confirmar", f"¿Cancelar la reserva {id_reserva}?", parent=self)
        if confirm:
            ok, msg = self.sistema.cancelar_reserva(id_reserva)
            if ok:
                messagebox.showinfo("Cancelada", "Reserva cancelada correctamente", parent=self)
                self._cargar_reservas()
            else:
                messagebox.showerror("Error", msg, parent=self)
