import tkinter as tk
from tkinter import messagebox

class VentanaPerfil(tk.Toplevel):
    def __init__(self, parent, sistema, usuario):
        super().__init__(parent)
        self.sistema = sistema
        self.usuario = usuario
        self.title("Mi Perfil")
        self.geometry("420x460")
        self.configure(bg="#1a2744")
        self.resizable(False, False)

        self._crear_widgets()

    def _crear_widgets(self):
        # avatar
        tk.Label(self, text="👤", font=("Arial", 50),
                 bg="#1a2744").pack(pady=15)
        tk.Label(self, text=self.usuario.get('nombre', ''),
                 font=("Arial", 14, "bold"), bg="#1a2744", fg="white").pack()
        tk.Label(self, text=self.usuario.get('tipo', '').capitalize(),
                 font=("Arial", 10), bg="#1a2744", fg="#c8a951").pack(pady=(2, 15))

        frame = tk.Frame(self, bg="#243156", padx=25, pady=20)
        frame.pack(padx=25, fill="x")

        tk.Label(frame, text="Editar información:",
                 font=("Arial", 11, "bold"), bg="#243156", fg="white").pack(anchor="w", pady=(0, 10))

        campos = [
            ("Matrícula (no editable):", "matricula", True),
            ("Nombre:", "nombre", False),
            ("Correo:", "correo", False),
        ]

        self.entries = {}
        for label_text, key, readonly in campos:
            tk.Label(frame, text=label_text, font=("Arial", 9),
                     bg="#243156", fg="#c0d0e0", anchor="w").pack(fill="x")
            entry = tk.Entry(frame, font=("Arial", 10),
                             bg="#1a2744" if not readonly else "#0d1520",
                             fg="white" if not readonly else "#607080",
                             insertbackground="white",
                             relief="flat", bd=4,
                             state="normal" if not readonly else "disabled")
            entry.pack(fill="x", pady=(2, 8), ipady=4)
            if not readonly:
                entry.insert(0, self.usuario.get(key, ''))
            else:
                entry.config(state="normal")
                entry.insert(0, self.usuario.get(key, ''))
                entry.config(state="disabled")
            self.entries[key] = entry

        # cambiar contraseña
        tk.Label(frame, text="Nueva contraseña (dejar vacío para no cambiar):",
                 font=("Arial", 9), bg="#243156", fg="#c0d0e0", anchor="w").pack(fill="x")
        self.entry_nueva_contra = tk.Entry(frame, font=("Arial", 10),
                                            bg="#1a2744", fg="white",
                                            insertbackground="white",
                                            show="*", relief="flat", bd=4)
        self.entry_nueva_contra.pack(fill="x", pady=(2, 15), ipady=4)

        tk.Button(frame, text="GUARDAR CAMBIOS",
                  font=("Arial", 11, "bold"),
                  bg="#c8a951", fg="#1a2744",
                  relief="flat", cursor="hand2",
                  command=self._guardar).pack(fill="x", ipady=7)

        # boton generar QR
        tk.Button(self, text="📱 Generar mi Código QR",
                  font=("Arial", 10), bg="#2d4070", fg="white",
                  relief="flat", cursor="hand2", padx=15, pady=8,
                  command=self._generar_qr).pack(pady=15)

    def _guardar(self):
        nuevo_nombre = self.entries["nombre"].get().strip()
        nuevo_correo = self.entries["correo"].get().strip()
        nueva_contra = self.entry_nueva_contra.get().strip()

        if not nuevo_nombre:
            messagebox.showwarning("Error", "El nombre no puede estar vacío", parent=self)
            return

        # actualizar en la lista de usuarios del sistema
        matricula = self.usuario['matricula']
        for u in self.sistema.usuarios:
            if u['matricula'] == matricula:
                u['nombre'] = nuevo_nombre
                u['correo'] = nuevo_correo
                if nueva_contra:
                    if len(nueva_contra) < 6:
                        messagebox.showwarning("Contraseña corta",
                                               "La contraseña debe tener al menos 6 caracteres",
                                               parent=self)
                        return
                    u['contrasena'] = nueva_contra
                # actualizar tambien el usuario activo del sistema
                self.sistema.usuario_activo = u
                self.usuario.update(u)
                break

        self.sistema.guardar_datos()
        messagebox.showinfo("Guardado", "Perfil actualizado correctamente", parent=self)

    def _generar_qr(self):
        from interfaces.ventana_ver_qr import VentanaVerQR
        VentanaVerQR(self, self.sistema, self.usuario)
