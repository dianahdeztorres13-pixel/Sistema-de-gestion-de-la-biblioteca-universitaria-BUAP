import tkinter as tk
from tkinter import ttk, messagebox

class VentanaReportes(tk.Toplevel):
    def __init__(self, parent, sistema):
        super().__init__(parent)
        self.sistema = sistema
        self.title("Reportes del Sistema")
        self.geometry("750x560")
        self.configure(bg="#1a2744")

        self._crear_widgets()

    def _crear_widgets(self):
        tk.Label(self, text=" Reportes y Estadísticas",
                 font=("Arial", 14, "bold"), bg="#1a2744", fg="#c8a951").pack(pady=15)

        # tabs para diferentes reportes
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Tab 1: Libros
        frame_libros = tk.Frame(notebook, bg="#1a2744")
        notebook.add(frame_libros, text=" Libros")
        self._tab_libros(frame_libros)

        # Tab 2: Espacios
        frame_espacios = tk.Frame(notebook, bg="#1a2744")
        notebook.add(frame_espacios, text=" Espacios")
        self._tab_espacios(frame_espacios)

        # Tab 3: Usuarios
        frame_usuarios = tk.Frame(notebook, bg="#1a2744")
        notebook.add(frame_usuarios, text=" Usuarios")
        self._tab_usuarios(frame_usuarios)

        # Tab 4: Grafica (solo si matplotlib esta disponible)
        frame_grafica = tk.Frame(notebook, bg="#1a2744")
        notebook.add(frame_grafica, text=" Gráfica")
        self._tab_grafica(frame_grafica)

    def _tab_libros(self, frame):
        reporte = self.sistema.generar_reporte_libros()

        tk.Label(frame, text="Estado de la Colección Bibliográfica",
                 font=("Arial", 12, "bold"), bg="#1a2744", fg="white").pack(pady=15)

        frame_cards = tk.Frame(frame, bg="#1a2744")
        frame_cards.pack()

        cards = [
            ("Total de Libros", reporte['total'], "#243156", "white"),
            ("Disponibles", reporte['disponibles'], "#1d4020", "#60c060"),
            ("Prestados", reporte['prestados'], "#401d1d", "#c06060"),
        ]

        for titulo, valor, bg, color in cards:
            card = tk.Frame(frame_cards, bg=bg, padx=25, pady=20)
            card.pack(side="left", padx=15)
            tk.Label(card, text=str(valor), font=("Arial", 28, "bold"),
                     bg=bg, fg=color).pack()
            tk.Label(card, text=titulo, font=("Arial", 9),
                     bg=bg, fg="#a0b0c0").pack()

        # tabla detallada
        tk.Label(frame, text="Lista completa:", font=("Arial", 10),
                 bg="#1a2744", fg="#c0d0e0").pack(anchor="w", padx=15, pady=(15, 5))

        frame_t = tk.Frame(frame, bg="#1a2744")
        frame_t.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        cols = ("ID", "Título", "Autor", "Estado")
        tabla = ttk.Treeview(frame_t, columns=cols, show="headings", height=8)
        for col in cols:
            tabla.heading(col, text=col)
        tabla.column("ID", width=60, anchor="center")
        tabla.column("Título", width=220)
        tabla.column("Autor", width=160)
        tabla.column("Estado", width=100, anchor="center")

        for libro in self.sistema.libros:
            tabla.insert("", "end", values=(
                libro['id_libro'], libro['titulo'], libro['autor'],
                "Si" if libro['disponibilidad'] else "No"
            ))

        scroll = ttk.Scrollbar(frame_t, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scroll.set)
        tabla.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    def _tab_espacios(self, frame):
        reporte = self.sistema.generar_reporte_espacios()

        tk.Label(frame, text="Disponibilidad de Espacios",
                 font=("Arial", 12, "bold"), bg="#1a2744", fg="white").pack(pady=15)

        frame_cards = tk.Frame(frame, bg="#1a2744")
        frame_cards.pack()

        tipos = [
            (" Cubículos", reporte['cubiculos']),
            (" Talleres", reporte['talleres']),
            (" Videojuegos", reporte['videojuegos']),
        ]

        for titulo, datos in tipos:
            card = tk.Frame(frame_cards, bg="#243156", padx=20, pady=15)
            card.pack(side="left", padx=10)
            tk.Label(card, text=titulo, font=("Arial", 11, "bold"),
                     bg="#243156", fg="#c8a951").pack()
            tk.Label(card, text=f"Total: {datos['total']}",
                     font=("Arial", 10), bg="#243156", fg="white").pack()
            tk.Label(card, text=f"Disponibles: {datos['disponibles']}",
                     font=("Arial", 10), bg="#243156", fg="#60c060").pack()
            tk.Label(card, text=f"Ocupados: {datos['total'] - datos['disponibles']}",
                     font=("Arial", 10), bg="#243156", fg="#c06060").pack()

        # reservas recientes
        tk.Label(frame, text="Reservas registradas:", font=("Arial", 10),
                 bg="#1a2744", fg="#c0d0e0").pack(anchor="w", padx=15, pady=(20, 5))

        frame_t = tk.Frame(frame, bg="#1a2744")
        frame_t.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        cols = ("ID", "Usuario", "Espacio", "Fecha", "Estado")
        tabla = ttk.Treeview(frame_t, columns=cols, show="headings", height=8)
        for col in cols:
            tabla.heading(col, text=col)

        for r in self.sistema.reservas[-20:]:  # ultimas 20
            tabla.insert("", "end", values=(
                r['id_reserva'], r['id_usuario'], r['id_espacio'],
                r['fecha'], r['estado']
            ))

        scroll = ttk.Scrollbar(frame_t, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scroll.set)
        tabla.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    def _tab_usuarios(self, frame):
        tk.Label(frame, text="Usuarios Registrados",
                 font=("Arial", 12, "bold"), bg="#1a2744", fg="white").pack(pady=15)

        total = len(self.sistema.usuarios)
        tipos = {}
        for u in self.sistema.usuarios:
            tipo = u.get('tipo', 'desconocido')
            tipos[tipo] = tipos.get(tipo, 0) + 1

        frame_cards = tk.Frame(frame, bg="#1a2744")
        frame_cards.pack()

        card_total = tk.Frame(frame_cards, bg="#243156", padx=25, pady=15)
        card_total.pack(side="left", padx=10)
        tk.Label(card_total, text=str(total), font=("Arial", 28, "bold"),
                 bg="#243156", fg="#c8a951").pack()
        tk.Label(card_total, text="Total Usuarios", font=("Arial", 9),
                 bg="#243156", fg="#a0b0c0").pack()

        for tipo, cantidad in tipos.items():
            card = tk.Frame(frame_cards, bg="#1d3050", padx=20, pady=15)
            card.pack(side="left", padx=8)
            tk.Label(card, text=str(cantidad), font=("Arial", 20, "bold"),
                     bg="#1d3050", fg="white").pack()
            tk.Label(card, text=tipo.capitalize(), font=("Arial", 9),
                     bg="#1d3050", fg="#a0b0c0").pack()

    def _tab_grafica(self, frame):
        try:
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

            reporte_libros = self.sistema.generar_reporte_libros()
            reporte_espacios = self.sistema.generar_reporte_espacios()

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 4))
            fig.patch.set_facecolor('#1a2744')

            # grafica de libros
            labels_l = ['Disponibles', 'Prestados']
            valores_l = [reporte_libros['disponibles'], reporte_libros['prestados']]
            colores_l = ['#3a8040', '#803a3a']
            ax1.pie(valores_l, labels=labels_l, colors=colores_l,
                    autopct='%1.1f%%', textprops={'color': 'white'})
            ax1.set_title('Estado de Libros', color='#c8a951')
            ax1.set_facecolor('#243156')

            # grafica de espacios
            categorias = ['Cubículos', 'Talleres', 'Videojuegos']
            disponibles = [
                reporte_espacios['cubiculos']['disponibles'],
                reporte_espacios['talleres']['disponibles'],
                reporte_espacios['videojuegos']['disponibles']
            ]
            ocupados = [
                reporte_espacios['cubiculos']['total'] - reporte_espacios['cubiculos']['disponibles'],
                reporte_espacios['talleres']['total'] - reporte_espacios['talleres']['disponibles'],
                reporte_espacios['videojuegos']['total'] - reporte_espacios['videojuegos']['disponibles'],
            ]
            x = range(len(categorias))
            ax2.bar(x, disponibles, label='Disponible', color='#3a8040')
            ax2.bar(x, ocupados, bottom=disponibles, label='Ocupado', color='#803a3a')
            ax2.set_xticks(x)
            ax2.set_xticklabels(categorias, color='white', fontsize=8)
            ax2.set_facecolor('#243156')
            ax2.set_title('Espacios', color='#c8a951')
            ax2.legend(labelcolor='white', facecolor='#1a2744')
            ax2.tick_params(colors='white')

            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        except ImportError:
            tk.Label(frame,
                     text=" Matplotlib no está instalado\n\npip install matplotlib",
                     font=("Arial", 12), bg="#1a2744", fg="#c8a951",
                     justify="center").pack(expand=True)
        except Exception as e:
            tk.Label(frame, text=f"Error al generar gráfica:\n{e}",
                     font=("Arial", 10), bg="#1a2744", fg="#e05050").pack(expand=True)
