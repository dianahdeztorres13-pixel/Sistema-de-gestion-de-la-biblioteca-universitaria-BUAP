import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class VentanaEspacios(tk.Toplevel):
    def __init__(self, parent, sistema, usuario, tipo="cubiculo"):
        super().__init__(parent)
        self.sistema = sistema
        self.usuario = usuario
        self.tipo = tipo
        self.parent = parent

        titulos = {
            "cubiculo": "🏠 Reservación de Cubículos",
            "taller": "🎓 Reservación de Talleres",
            "videojuegos": "🎮 Salas de Videojuegos"
        }
        self.title(titulos.get(tipo, "Espacios"))
        self.geometry("680x530")
        self.configure(bg="#1a2744")

        self._crear_widgets()
        self._cargar_espacios()

    def _crear_widgets(self):
        # header
        frame_top = tk.Frame(self, bg="#0f1a33", pady=12)
        frame_top.pack(fill="x")

        titulos = {
            "cubiculo": "Cubículos de Estudio",
            "taller": "Espacios para Talleres",
            "videojuegos": "Salas de Videojuegos"
        }
        tk.Label(frame_top, text=titulos.get(self.tipo, "Espacios"),
                 font=("Arial", 14, "bold"), bg="#0f1a33", fg="#c8a951").pack(side="left", padx=20)

        # leyenda
        tk.Label(frame_top, text="🟢 Disponible   🔴 No disponible",
                 font=("Arial", 9), bg="#0f1a33", fg="#a0b0c0").pack(side="right", padx=20)

        # grid de espacios
        self.frame_grid = tk.Frame(self, bg="#1a2744")
        self.frame_grid.pack(fill="both", expand=True, padx=20, pady=15)

        # formulario de reserva
        frame_form = tk.Frame(self, bg="#243156", pady=12, padx=20)
        frame_form.pack(fill="x", padx=15, pady=(0, 10))

        tk.Label(frame_form, text="Reservar espacio seleccionado:",
                 font=("Arial", 10, "bold"), bg="#243156", fg="white").pack(anchor="w")

        frame_inputs = tk.Frame(frame_form, bg="#243156")
        frame_inputs.pack(fill="x", pady=8)

        tk.Label(frame_inputs, text="Fecha (DD/MM/AAAA):",
                 font=("Arial", 9), bg="#243156", fg="#c0d0e0").pack(side="left")
        self.entry_fecha = tk.Entry(frame_inputs, font=("Arial", 10),
                                     bg="#1a2744", fg="white",
                                     insertbackground="white",
                                     relief="flat", bd=3, width=14)
        self.entry_fecha.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.entry_fecha.pack(side="left", ipady=4, padx=(5, 20))

        tk.Label(frame_inputs, text="Hora:",
                 font=("Arial", 9), bg="#243156", fg="#c0d0e0").pack(side="left")
        self.combo_hora = ttk.Combobox(frame_inputs,
                                        values=["08:00", "09:00", "10:00", "11:00",
                                                "12:00", "13:00", "14:00", "15:00",
                                                "16:00", "17:00", "18:00"],
                                        state="readonly", width=8, font=("Arial", 10))
        self.combo_hora.set("09:00")
        self.combo_hora.pack(side="left", padx=(5, 20))

        tk.Button(frame_inputs, text="📅 RESERVAR",
                  font=("Arial", 10, "bold"), bg="#c8a951", fg="#1a2744",
                  relief="flat", cursor="hand2", padx=12, pady=5,
                  command=self._reservar).pack(side="left")

        self.espacio_seleccionado = None
        self.lbl_seleccion = tk.Label(frame_form, text="Ningún espacio seleccionado",
                                       font=("Arial", 9), bg="#243156", fg="#809aaa")
        self.lbl_seleccion.pack(anchor="w")

    def _cargar_espacios(self):
        for widget in self.frame_grid.winfo_children():
            widget.destroy()

        espacios = [e for e in self.sistema.espacios if e['tipo'] == self.tipo]

        if not espacios:
            tk.Label(self.frame_grid, text="No hay espacios de este tipo registrados",
                     font=("Arial", 11), bg="#1a2744", fg="#809aaa").pack(pady=40)
            return

        fila, col = 0, 0
        for espacio in espacios:
            disponible = espacio['disponibilidad']
            color_bg = "#1d4020" if disponible else "#401d1d"
            color_borde = "#3a8040" if disponible else "#803a3a"
            estado_texto = "✅ Disponible" if disponible else "❌ Ocupado"
            estado_color = "#60c060" if disponible else "#c06060"

            frame_espacio = tk.Frame(self.frame_grid, bg=color_bg,
                                      relief="flat", padx=15, pady=15,
                                      cursor="hand2" if disponible else "arrow")
            frame_espacio.grid(row=fila, column=col, padx=8, pady=8, sticky="nsew")

            tk.Label(frame_espacio,
                     text="🏠" if self.tipo == "cubiculo" else
                          "🎓" if self.tipo == "taller" else "🎮",
                     font=("Arial", 22), bg=color_bg).pack()

            tk.Label(frame_espacio, text=espacio['id_espacio'],
                     font=("Arial", 11, "bold"), bg=color_bg, fg="white").pack()

            tk.Label(frame_espacio, text=f"Cap: {espacio['capacidad']} personas",
                     font=("Arial", 8), bg=color_bg, fg="#a0b0c0").pack()

            tk.Label(frame_espacio, text=estado_texto,
                     font=("Arial", 9, "bold"), bg=color_bg, fg=estado_color).pack(pady=(5, 0))

            if disponible:
                frame_espacio.bind("<Button-1>", lambda e, esp=espacio: self._seleccionar(esp))
                for widget in frame_espacio.winfo_children():
                    widget.bind("<Button-1>", lambda e, esp=espacio: self._seleccionar(esp))

            col += 1
            if col >= 3:
                col = 0
                fila += 1

        # configurar pesos de columna para que se expandan bien
        for i in range(3):
            self.frame_grid.columnconfigure(i, weight=1)

    def _seleccionar(self, espacio):
        self.espacio_seleccionado = espacio
        self.lbl_seleccion.config(
            text=f"Seleccionado: {espacio['id_espacio']} (Cap. {espacio['capacidad']})",
            fg="#c8a951"
        )

    def _reservar(self):
        if not self.espacio_seleccionado:
            messagebox.showwarning("Sin selección",
                                   "Primero selecciona un espacio disponible", parent=self)
            return

        fecha = self.entry_fecha.get().strip()
        hora = self.combo_hora.get()

        if not fecha:
            messagebox.showwarning("Fecha requerida", "Ingresa la fecha de reserva", parent=self)
            return

        ok, msg = self.sistema.reservar_espacio(
            self.espacio_seleccionado['id_espacio'],
            self.usuario['matricula'],
            fecha, hora
        )

        if ok:
            messagebox.showinfo("Reserva confirmada",
                                f"✅ {msg}\nEspacio: {self.espacio_seleccionado['id_espacio']}\n"
                                f"Fecha: {fecha}  Hora: {hora}", parent=self)
            self.espacio_seleccionado = None
            self.lbl_seleccion.config(text="Ningún espacio seleccionado", fg="#809aaa")
            self._cargar_espacios()
        else:
            messagebox.showerror("Error", msg, parent=self)
