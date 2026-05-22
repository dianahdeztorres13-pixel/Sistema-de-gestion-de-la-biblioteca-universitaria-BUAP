import tkinter as tk
from tkinter import messagebox

class VentanaVerQR(tk.Toplevel):
    def __init__(self, parent, sistema, usuario):
        super().__init__(parent)
        self.sistema = sistema
        self.usuario = usuario
        self.title("Mi Código QR")
        self.geometry("350x400")
        self.configure(bg="#1a2744")
        self.resizable(False, False)
        self.grab_set()

        self._crear_widgets()
        self._generar_mostrar_qr()

    def _crear_widgets(self):
        tk.Label(self, text=" Tu Código QR de Acceso",
                 font=("Arial", 12, "bold"), bg="#1a2744", fg="#c8a951").pack(pady=15)

        tk.Label(self, text=f"Usuario: {self.usuario.get('nombre', '')}",
                 font=("Arial", 10), bg="#1a2744", fg="white").pack()
        tk.Label(self, text=f"Matrícula: {self.usuario.get('matricula', '')}",
                 font=("Arial", 10), bg="#1a2744", fg="#a0b0c0").pack(pady=(2, 10))

        self.frame_qr = tk.Frame(self, bg="#ffffff", padx=10, pady=10)
        self.frame_qr.pack(padx=30)

        self.lbl_qr = tk.Label(self.frame_qr, bg="#ffffff")
        self.lbl_qr.pack()

        self.lbl_info = tk.Label(self, text="",
                                  font=("Arial", 9), bg="#1a2744", fg="#809aaa")
        self.lbl_info.pack(pady=5)

        tk.Button(self, text="Cerrar", font=("Arial", 10),
                  bg="#2d4070", fg="white", relief="flat",
                  cursor="hand2", padx=20, pady=7,
                  command=self.destroy).pack(pady=15)

    def _generar_mostrar_qr(self):
        try:
            import qrcode
            from PIL import Image, ImageTk

            matricula = self.usuario.get('matricula', '')
            qr = qrcode.QRCode(version=1, box_size=6, border=3)
            qr.add_data(matricula)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            # guardar y mostrar
            import os
            if not os.path.exists("datos"):
                os.makedirs("datos")
            ruta = f"datos/qr_{matricula}.png"
            img.save(ruta)

            img_tk = ImageTk.PhotoImage(img)
            self.lbl_qr.config(image=img_tk)
            self.lbl_qr.image = img_tk  # referencia para que no se borre del garbage collector

            self.lbl_info.config(text=f"QR guardado en: {ruta}")

            # actualizar en el sistema
            for u in self.sistema.usuarios:
                if u['matricula'] == matricula:
                    u['codigoQR'] = ruta
            self.sistema.guardar_datos()

        except ImportError as e:
            self.lbl_qr.config(text=" Instalar:\npip install qrcode pillow",
                                font=("Arial", 10), fg="red")
            self.lbl_info.config(text=str(e))
        except Exception as e:
            self.lbl_qr.config(text=f"Error:\n{str(e)}",
                                font=("Arial", 9), fg="red")
