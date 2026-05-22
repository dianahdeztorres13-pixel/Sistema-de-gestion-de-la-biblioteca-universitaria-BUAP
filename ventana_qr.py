import tkinter as tk
from tkinter import messagebox

class VentanaQR(tk.Toplevel):
    def __init__(self, parent, sistema):
        super().__init__(parent)
        self.sistema = sistema
        self.parent = parent
        self.title("Acceso con Código QR")
        self.geometry("380x320")
        self.configure(bg="#1a2744")
        self.resizable(False, False)
        self.grab_set()

        self._crear_widgets()

    def _crear_widgets(self):
        tk.Label(self, text="📷", font=("Arial", 48),
                 bg="#1a2744", fg="#c8a951").pack(pady=20)

        tk.Label(self, text="Escanear Código QR",
                 font=("Arial", 14, "bold"), bg="#1a2744", fg="white").pack()

        tk.Label(self, text="Coloca tu tarjeta QR frente al lector\no ingresa tu matrícula manualmente:",
                 font=("Arial", 9), bg="#1a2744", fg="#a0b0c0", justify="center").pack(pady=10)

        frame = tk.Frame(self, bg="#243156", padx=20, pady=15)
        frame.pack(padx=30, fill="x")

        tk.Label(frame, text="Matrícula:", font=("Arial", 10),
                 bg="#243156", fg="#c0d0e0").pack(anchor="w")
        self.entry_matricula = tk.Entry(frame, font=("Arial", 12),
                                         bg="#1a2744", fg="white",
                                         insertbackground="white",
                                         relief="flat", bd=4)
        self.entry_matricula.pack(fill="x", pady=(3, 10), ipady=5)

        tk.Button(frame, text="ACCEDER",
                  font=("Arial", 11, "bold"),
                  bg="#c8a951", fg="#1a2744",
                  relief="flat", cursor="hand2",
                  command=self._acceder).pack(fill="x", ipady=7)

        self.entry_matricula.bind("<Return>", lambda e: self._acceder())
        self.entry_matricula.focus()

    def _acceder(self):
        matricula = self.entry_matricula.get().strip()
        if not matricula:
            messagebox.showwarning("Error", "Ingresa tu matrícula", parent=self)
            return

        usuario = self.sistema.validar_qr(matricula)
        if usuario:
            self.destroy()
            from interfaces.ventana_menu import VentanaMenu
            self.parent.withdraw()
            menu = VentanaMenu(self.parent, self.sistema, usuario)
            menu.protocol("WM_DELETE_WINDOW", lambda: self._cerrar_todo(menu))
        else:
            messagebox.showerror("No encontrado",
                                 "No se encontró ningún usuario con esa matrícula", parent=self)

    def _cerrar_todo(self, ventana):
        ventana.destroy()
        self.parent.deiconify()
