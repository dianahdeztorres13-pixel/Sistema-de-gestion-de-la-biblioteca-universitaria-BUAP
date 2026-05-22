import tkinter as tk
from tkinter import ttk, messagebox

class VentanaRegistro(tk.Toplevel):
    def __init__(self, parent, sistema):
        super().__init__(parent)
        self.sistema = sistema
        self.parent = parent
        self.title("Registro de Usuario")
        self.geometry("440x600")
        self.minsize(440, 600)
        self.configure(bg="#1a2744")
        self.resizable(True, True)
        self.transient(parent)

        self._crear_widgets()

        # hacer modal de forma segura (después de que la ventana sea visible)
        self.update_idletasks()
        try:
            self.wait_visibility()
            self.grab_set()
        except tk.TclError:
            pass

    def _crear_widgets(self):
        tk.Label(self, text="Nuevo Usuario", font=("Arial", 16, "bold"),
                 bg="#1a2744", fg="#c8a951").pack(pady=15)

        # botón REGISTRAR anclado al fondo (siempre visible aunque la ventana sea pequeña)
        frame_btn = tk.Frame(self, bg="#1a2744")
        frame_btn.pack(side="bottom", fill="x", padx=30, pady=15)

        btn_registrar = tk.Button(frame_btn, text="REGISTRAR",
                                   font=("Arial", 12, "bold"),
                                   bg="#c8a951", fg="#1a2744",
                                   relief="flat", cursor="hand2",
                                   command=self._registrar)
        btn_registrar.pack(fill="x", ipady=10)

        # frame con los campos
        frame = tk.Frame(self, bg="#243156", padx=25, pady=20)
        frame.pack(padx=30, pady=(0, 10), fill="both", expand=True)

        campos = [
            ("Matrícula / ID:", "matricula"),
            ("Nombre completo:", "nombre"),
            ("Correo institucional:", "correo"),
            ("Contraseña:", "contrasena"),
            ("Confirmar contraseña:", "confirmar"),
        ]

        self.entries = {}
        for label_text, key in campos:
            tk.Label(frame, text=label_text, font=("Arial", 9),
                     bg="#243156", fg="#c0d0e0", anchor="w").pack(fill="x")
            show = "*" if "contrasena" in key or "confirmar" in key else ""
            entry = tk.Entry(frame, font=("Arial", 10),
                             bg="#1a2744", fg="white",
                             insertbackground="white",
                             show=show, relief="flat", bd=4)
            entry.pack(fill="x", pady=(2, 8), ipady=4)
            self.entries[key] = entry

        # tipo de usuario
        tk.Label(frame, text="Tipo de usuario:", font=("Arial", 9),
                 bg="#243156", fg="#c0d0e0", anchor="w").pack(fill="x")
        self.combo_tipo = ttk.Combobox(frame,
                                        values=["estudiante", "docente", "visitante"],
                                        state="readonly", font=("Arial", 10))
        self.combo_tipo.set("estudiante")
        self.combo_tipo.pack(fill="x", pady=(2, 5))

        # permitir registrar con Enter
        self.entries["confirmar"].bind("<Return>", lambda e: self._registrar())

    def _registrar(self):
        matricula = self.entries["matricula"].get().strip()
        nombre = self.entries["nombre"].get().strip()
        correo = self.entries["correo"].get().strip()
        contrasena = self.entries["contrasena"].get().strip()
        confirmar = self.entries["confirmar"].get().strip()
        tipo = self.combo_tipo.get()

        # validaciones - un poco basicas como estudiante
        if not matricula or not nombre or not correo or not contrasena:
            messagebox.showwarning("Error", "Todos los campos son obligatorios", parent=self)
            return

        if contrasena != confirmar:
            messagebox.showerror("Error", "Las contraseñas no coinciden", parent=self)
            return

        if len(contrasena) < 6:
            messagebox.showwarning("Aviso", "La contraseña debe tener al menos 6 caracteres", parent=self)
            return

        # no valida formato de correo (error comun de estudiante)
        ok, msg = self.sistema.registrar_usuario(matricula, nombre, correo, contrasena, tipo)
        if ok:
            messagebox.showinfo("Éxito", f"Usuario registrado!\nYa puedes iniciar sesión.", parent=self)
            self.destroy()
        else:
            messagebox.showerror("Error", msg, parent=self)
