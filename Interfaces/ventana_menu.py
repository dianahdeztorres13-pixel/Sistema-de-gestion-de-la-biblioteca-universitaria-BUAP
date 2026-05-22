import tkinter as tk
from tkinter import messagebox

class VentanaMenu(tk.Toplevel):
    def __init__(self, parent, sistema, usuario):
        super().__init__(parent)
        self.parent = parent
        self.sistema = sistema
        self.usuario = usuario
        self.title("Sistema Biblioteca BUAP - Menú Principal")
        self.geometry("800x560")
        self.configure(bg="#1a2744")
        self.resizable(True, True)
        self.minsize(700, 500)

        self._crear_widgets()

    def _crear_widgets(self):
        # sidebar
        self.sidebar = tk.Frame(self, bg="#0f1a33", width=200)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # nombre usuario en sidebar
        frame_user = tk.Frame(self.sidebar, bg="#192840", pady=15)
        frame_user.pack(fill="x")

        icono = "👨‍💼" if self.usuario.get('tipo') == 'admin' else "👤"
        tk.Label(frame_user, text=icono, font=("Arial", 24),
                 bg="#192840").pack()
        tk.Label(frame_user, text=self.usuario.get('nombre', 'Usuario'),
                 font=("Arial", 10, "bold"), bg="#192840", fg="white",
                 wraplength=180).pack()
        tk.Label(frame_user, text=self.usuario.get('tipo', '').capitalize(),
                 font=("Arial", 8), bg="#192840", fg="#c8a951").pack()

        # botones del menu
        opciones = [
            ("  Libros", self._abrir_libros),
            ("  Reservar Espacios", self._abrir_espacios),
            ("  Talleres", self._abrir_talleres),
            ("  Videojuegos", self._abrir_videojuegos),
            ("  Mis Préstamos", self._abrir_prestamos),
            ("  Mis Reservas", self._abrir_mis_reservas),
            ("  Reportes", self._abrir_reportes),
            ("  Machine Learning", self._abrir_ml),
            ("  Mi Perfil", self._abrir_perfil),
        ]

        # solo admin puede ver gestion
        if self.usuario.get('tipo') == 'admin':
            opciones.insert(0, ("🔧  Administración", self._abrir_admin))

        for texto, comando in opciones:
            btn = tk.Button(self.sidebar, text=texto,
                            font=("Arial", 10), bg="#0f1a33", fg="#c0d0e0",
                            relief="flat", anchor="w", padx=20, pady=10,
                            cursor="hand2", activebackground="#243156",
                            activeforeground="white", command=comando)
            btn.pack(fill="x")

        # boton cerrar sesion al fondo
        tk.Frame(self.sidebar, bg="#0f1a33").pack(fill="y", expand=True)
        tk.Button(self.sidebar, text="🚪  Cerrar Sesión",
                  font=("Arial", 10), bg="#0f1a33", fg="#e05050",
                  relief="flat", anchor="w", padx=20, pady=10,
                  cursor="hand2", command=self._cerrar_sesion).pack(fill="x", side="bottom")

        # area principal (contenido)
        self.area_contenido = tk.Frame(self, bg="#1a2744")
        self.area_contenido.pack(side="right", fill="both", expand=True)

        self._mostrar_bienvenida()

    def _mostrar_bienvenida(self):
        for widget in self.area_contenido.winfo_children():
            widget.destroy()

        tk.Label(self.area_contenido, text="Bienvenido al Sistema",
                 font=("Georgia", 20, "bold"), bg="#1a2744", fg="#c8a951").pack(pady=40)

        tk.Label(self.area_contenido,
                 text=f"Hola, {self.usuario.get('nombre', 'Usuario')}",
                 font=("Arial", 14), bg="#1a2744", fg="white").pack()

        tk.Label(self.area_contenido,
                 text="Selecciona una opción del menú lateral para comenzar",
                 font=("Arial", 10), bg="#1a2744", fg="#809aaa").pack(pady=10)

        # estadisticas rapidas
        frame_stats = tk.Frame(self.area_contenido, bg="#1a2744")
        frame_stats.pack(pady=30)

        reporte_libros = self.sistema.generar_reporte_libros()
        reporte_espacios = self.sistema.generar_reporte_espacios()

        stats = [
            ("", "Libros\nDisponibles", str(reporte_libros['disponibles'])),
            ("", "Cubículos\nLibres", str(reporte_espacios['cubiculos']['disponibles'])),
            ("", "Talleres\nDisponibles", str(reporte_espacios['talleres']['disponibles'])),
            ("", "Salas Juegos\nLibres", str(reporte_espacios['videojuegos']['disponibles'])),
        ]

        for icono, label, valor in stats:
            frame_card = tk.Frame(frame_stats, bg="#243156",
                                   padx=20, pady=15, relief="flat")
            frame_card.pack(side="left", padx=10)
            tk.Label(frame_card, text=icono, font=("Arial", 20),
                     bg="#243156").pack()
            tk.Label(frame_card, text=valor, font=("Arial", 18, "bold"),
                     bg="#243156", fg="#c8a951").pack()
            tk.Label(frame_card, text=label, font=("Arial", 8),
                     bg="#243156", fg="#a0b0c0", justify="center").pack()

    def _abrir_libros(self):
        from interfaces.ventana_libros import VentanaLibros
        VentanaLibros(self, self.sistema, self.usuario)

    def _abrir_espacios(self):
        from interfaces.ventana_espacios import VentanaEspacios
        VentanaEspacios(self, self.sistema, self.usuario, tipo="cubiculo")

    def _abrir_talleres(self):
        from interfaces.ventana_espacios import VentanaEspacios
        VentanaEspacios(self, self.sistema, self.usuario, tipo="taller")

    def _abrir_videojuegos(self):
        from interfaces.ventana_espacios import VentanaEspacios
        VentanaEspacios(self, self.sistema, self.usuario, tipo="videojuegos")

    def _abrir_prestamos(self):
        from interfaces.ventana_prestamos import VentanaPrestamos
        VentanaPrestamos(self, self.sistema, self.usuario)

    def _abrir_mis_reservas(self):
        from interfaces.ventana_mis_reservas import VentanaMisReservas
        VentanaMisReservas(self, self.sistema, self.usuario)

    def _abrir_reportes(self):
        from interfaces.ventana_reportes import VentanaReportes
        VentanaReportes(self, self.sistema)

    def _abrir_ml(self):
        from interfaces.ventana_ml import VentanaML
        VentanaML(self, self.sistema, self.usuario)

    def _abrir_perfil(self):
        from interfaces.ventana_perfil import VentanaPerfil
        VentanaPerfil(self, self.sistema, self.usuario)

    def _abrir_admin(self):
        from interfaces.ventana_admin import VentanaAdmin
        VentanaAdmin(self, self.sistema)

    def _cerrar_sesion(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Deseas cerrar sesión?"):
            self.sistema.usuario_activo = None
            self.destroy()
            self.parent.deiconify()
