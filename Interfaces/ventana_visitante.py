import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class VentanaVisitante(tk.Toplevel):
    def __init__(self, parent, sistema):
        super().__init__(parent)
        self.sistema = sistema
        self.parent = parent
        self.title("Registro de Visitante")
        self.geometry("420x420")
        self.configure(bg="#1a2744")
        self.resizable(False, False)
        self.grab_set()

        self._crear_widgets()

    def _crear_widgets(self):
        tk.Label(self, text="👤 Acceso Visitante",
                 font=("Arial", 15, "bold"), bg="#1a2744", fg="#c8a951").pack(pady=20)
        tk.Label(self, text="Los visitantes deben registrarse manualmente",
                 font=("Arial", 9), bg="#1a2744", fg="#809aaa").pack()

        frame = tk.Frame(self, bg="#243156", padx=25, pady=20)
        frame.pack(padx=30, pady=15, fill="both", expand=True)

        campos = [
            ("Nombre completo:", "nombre"),
            ("Institución / Empresa:", "institucion"),
            ("Motivo de visita:", "motivo"),
        ]

        self.entries = {}
        for label_text, key in campos:
            tk.Label(frame, text=label_text, font=("Arial", 9),
                     bg="#243156", fg="#c0d0e0", anchor="w").pack(fill="x")
            entry = tk.Entry(frame, font=("Arial", 10),
                             bg="#1a2744", fg="white",
                             insertbackground="white",
                             relief="flat", bd=4)
            entry.pack(fill="x", pady=(2, 10), ipady=4)
            self.entries[key] = entry

        # fecha automatica
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        tk.Label(frame, text=f"Fecha de visita: {fecha_actual}",
                 font=("Arial", 9), bg="#243156", fg="#80a0c0").pack(anchor="w", pady=(0, 15))

        tk.Button(frame, text="REGISTRAR VISITA",
                  font=("Arial", 11, "bold"),
                  bg="#c8a951", fg="#1a2744",
                  relief="flat", cursor="hand2",
                  command=self._registrar_visita).pack(fill="x", ipady=7)

    def _registrar_visita(self):
        nombre = self.entries["nombre"].get().strip()
        institucion = self.entries["institucion"].get().strip()
        motivo = self.entries["motivo"].get().strip()

        if not nombre or not motivo:
            messagebox.showwarning("Campos requeridos",
                                   "El nombre y motivo son obligatorios", parent=self)
            return

        # registrar como visitante temporal
        from datetime import datetime
        id_visitante = f"V{datetime.now().strftime('%H%M%S')}"
        ok, msg = self.sistema.registrar_usuario(
            id_visitante, nombre, "", "visitante123", "visitante"
        )

        if ok:
            messagebox.showinfo("Bienvenido",
                                f"Bienvenido {nombre}!\nID temporal: {id_visitante}\n"
                                f"Tienes acceso básico al sistema.", parent=self)
            usuario = self.sistema.validar_login(id_visitante, "visitante123")
            self.destroy()
            from interfaces.ventana_menu import VentanaMenu
            self.parent.withdraw()
            menu = VentanaMenu(self.parent, self.sistema, usuario)
            menu.protocol("WM_DELETE_WINDOW", lambda: self._cerrar_todo(menu))
        else:
            # si falla el registro (matricula duplicada en el mismo segundo xd)
            messagebox.showerror("Error", "Error al registrar visita, intenta de nuevo", parent=self)

    def _cerrar_todo(self, ventana):
        ventana.destroy()
        self.parent.deiconify()
