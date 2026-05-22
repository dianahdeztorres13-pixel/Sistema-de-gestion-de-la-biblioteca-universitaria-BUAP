import tkinter as tk
from tkinter import ttk, messagebox
from interfaces.ventana_registro import VentanaRegistro
from interfaces.ventana_menu import VentanaMenu
from interfaces.ventana_visitante import VentanaVisitante

class VentanaLogin(tk.Tk):
    def __init__(self, sistema):
        super().__init__()
        self.sistema = sistema
        self.title("Sistema Biblioteca BUAP")
        self.geometry("500x550")
        self.configure(bg="#1a2744")
        self.resizable(False, False)

        # centrar ventana
        self.eval('tk::PlaceWindow . center')

        self._crear_widgets()

    def _crear_widgets(self):
        # logo/header
        frame_header = tk.Frame(self, bg="#1a2744")
        frame_header.pack(pady=30)

        tk.Label(frame_header, text="BUAP", font=("Georgia", 36, "bold"),
                 bg="#1a2744", fg="#c8a951").pack()
        tk.Label(frame_header, text="Sistema de Gestión Bibliotecaria",
                 font=("Arial", 11), bg="#1a2744", fg="#a0b4d0").pack()
        tk.Label(frame_header, text="Facultad de Ciencias de la Computación",
                 font=("Arial", 9), bg="#1a2744", fg="#7090a0").pack()

        # frame login
        frame_login = tk.Frame(self, bg="#243156", relief="flat", padx=30, pady=25)
        frame_login.pack(padx=40, fill="x")

        tk.Label(frame_login, text="Iniciar Sesión", font=("Arial", 14, "bold"),
                 bg="#243156", fg="white").pack(pady=(0, 15))

        # matricula
        tk.Label(frame_login, text="Matrícula / ID:", font=("Arial", 10),
                 bg="#243156", fg="#c0d0e0", anchor="w").pack(fill="x")
        self.entry_matricula = tk.Entry(frame_login, font=("Arial", 11),
                                        bg="#1a2744", fg="white",
                                        insertbackground="white",
                                        relief="flat", bd=5)
        self.entry_matricula.pack(fill="x", pady=(2, 10), ipady=5)

        # contraseña
        tk.Label(frame_login, text="Contraseña:", font=("Arial", 10),
                 bg="#243156", fg="#c0d0e0", anchor="w").pack(fill="x")
        self.entry_contra = tk.Entry(frame_login, font=("Arial", 11),
                                      bg="#1a2744", fg="white",
                                      insertbackground="white",
                                      show="*", relief="flat", bd=5)
        self.entry_contra.pack(fill="x", pady=(2, 15), ipady=5)

        # boton login
        btn_login = tk.Button(frame_login, text="ENTRAR",
                               font=("Arial", 11, "bold"),
                               bg="#c8a951", fg="#1a2744",
                               relief="flat", cursor="hand2",
                               command=self._login)
        btn_login.pack(fill="x", ipady=8)

        # separador
        tk.Label(self, text="─── o ───", font=("Arial", 9),
                 bg="#1a2744", fg="#506080").pack(pady=15)

        # opciones extra
        frame_opciones = tk.Frame(self, bg="#1a2744")
        frame_opciones.pack()

        btn_qr = tk.Button(frame_opciones, text="📷 Acceso con QR",
                            font=("Arial", 10), bg="#2d4070", fg="white",
                            relief="flat", cursor="hand2", padx=15, pady=8,
                            command=self._acceso_qr)
        btn_qr.grid(row=0, column=0, padx=5)

        btn_registro = tk.Button(frame_opciones, text="➕ Registrarse",
                                  font=("Arial", 10), bg="#2d4070", fg="white",
                                  relief="flat", cursor="hand2", padx=15, pady=8,
                                  command=self._abrir_registro)
        btn_registro.grid(row=0, column=1, padx=5)

        btn_visitante = tk.Button(frame_opciones, text="👤 Visitante",
                                   font=("Arial", 10), bg="#2d4070", fg="white",
                                   relief="flat", cursor="hand2", padx=15, pady=8,
                                   command=self._acceso_visitante)
        btn_visitante.grid(row=0, column=2, padx=5)

        # bind enter key
        self.entry_contra.bind("<Return>", lambda e: self._login())

        # creditos
        tk.Label(self, text="Diana Luz Hernández Torres | 202509874",
                 font=("Arial", 8), bg="#1a2744", fg="#404060").pack(side="bottom", pady=10)

    def _login(self):
        matricula = self.entry_matricula.get().strip()
        contrasena = self.entry_contra.get().strip()

        if not matricula or not contrasena:
            messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos")
            return

        usuario = self.sistema.validar_login(matricula, contrasena)
        if usuario:
            self.withdraw()
            menu = VentanaMenu(self, self.sistema, usuario)
            menu.protocol("WM_DELETE_WINDOW", lambda: self._cerrar_todo(menu))
        else:
            messagebox.showerror("Error", "Matrícula o contraseña incorrectos")
            self.entry_contra.delete(0, tk.END)

    def _acceso_qr(self):
        from interfaces.ventana_qr import VentanaQR
        VentanaQR(self, self.sistema)

    def _abrir_registro(self):
        VentanaRegistro(self, self.sistema)

    def _acceso_visitante(self):
        VentanaVisitante(self, self.sistema)

    def _cerrar_todo(self, ventana):
        ventana.destroy()
        self.deiconify()
