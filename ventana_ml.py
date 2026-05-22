"""
Ventana de Machine Learning y Análisis de Datos.
Incluye 4 pestañas:
  1. Recomendador de Libros (KMeans)
  2. Predicción de Demanda de Espacios (Regresión Lineal)
  3. Análisis de Patrones de Uso (estadísticas descriptivas + gráficas)
  4. Predictor de Devolución Tardía (Árbol de Decisión)
"""

import tkinter as tk
from tkinter import ttk, messagebox


# paleta de colores compartida
BG        = "#1a2744"
BG2       = "#243156"
BG3       = "#0f1a33"
GOLD      = "#c8a951"
TEXT      = "#e0e8f0"
TEXT_DIM  = "#8090a8"
GREEN     = "#3a9e50"
RED       = "#c05050"
BLUE      = "#3d70c0"
ORANGE    = "#d08030"


def _estilo_tabla() -> None:
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background=BG2, foreground=TEXT,
                    fieldbackground=BG2, rowheight=26)
    style.configure("Treeview.Heading",
                    background=BG3, foreground=GOLD,
                    font=("Arial", 9, "bold"))
    style.map("Treeview", background=[("selected", "#3d5590")])


class VentanaML(tk.Toplevel):
    """Ventana principal del módulo de Machine Learning."""

    def __init__(self, parent, sistema, usuario):
        super().__init__(parent)
        self.sistema = sistema
        self.usuario = usuario

        # importar ML Manager
        from ML.ml_manager import ML_Manager
        self.ml = ML_Manager(sistema)

        self.title(" Machine Learning y Análisis de Datos — Biblioteca BUAP")
        self.geometry("900x640")
        self.configure(bg=BG)
        self.minsize(820, 580)

        _estilo_tabla()
        self._crear_widgets()

    # ─────────────────────────────────────────────── layout ──────────────────
    def _crear_widgets(self) -> None:
        # header
        hdr = tk.Frame(self, bg=BG3, pady=10)
        hdr.pack(fill="x")
        tk.Label(hdr, text=" Machine Learning & Análisis de Datos",
                 font=("Arial", 14, "bold"), bg=BG3, fg=GOLD).pack(side="left", padx=20)
        tk.Button(hdr, text="⚡ Entrenar todos los modelos",
                  font=("Arial", 9), bg=BLUE, fg="white",
                  relief="flat", cursor="hand2", padx=10, pady=4,
                  command=self._entrenar_todos).pack(side="right", padx=20)

        self.lbl_estado = tk.Label(self, text="Modelos listos para entrenar",
                                    font=("Arial", 8), bg=BG, fg=TEXT_DIM)
        self.lbl_estado.pack(anchor="e", padx=20)

        # notebook de pestañas
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=12, pady=6)

        self._tab_recomendador()
        self._tab_demanda()
        self._tab_patrones()
        self._tab_devolucion()

    # botón entrenar todos 
    def _entrenar_todos(self) -> None:
        self.lbl_estado.config(text="Entrenando… por favor espera", fg=GOLD)
        self.update()
        msgs = self.ml.entrenar_todos()
        resumen = "\n".join(msgs)
        self.lbl_estado.config(text="✅ Todos los modelos entrenados", fg=GREEN)
        messagebox.showinfo("Entrenamiento completo", resumen, parent=self)

    #  PESTAÑA 1 — Recomendador de Libros
     
    def _tab_recomendador(self) -> None:
        frame = tk.Frame(self.nb, bg=BG)
        self.nb.add(frame, text="📚 Recomendador")

        tk.Label(frame, text="Recomendador de Libros (KMeans Clustering)",
                 font=("Arial", 12, "bold"), bg=BG, fg=GOLD).pack(pady=12)
        tk.Label(frame,
                 text="Agrupa libros por categoría y popularidad. "
                      "Recomienda títulos similares a los que ya leíste.",
                 font=("Arial", 9), bg=BG, fg=TEXT_DIM).pack()

        # controles
        ctrl = tk.Frame(frame, bg=BG2, padx=20, pady=12)
        ctrl.pack(fill="x", padx=15, pady=10)

        tk.Label(ctrl, text="Matrícula del usuario:",
                 font=("Arial", 10), bg=BG2, fg=TEXT).grid(row=0, column=0, sticky="w")
        self.entry_rec_mat = tk.Entry(ctrl, font=("Arial", 11),
                                       bg=BG, fg="white",
                                       insertbackground="white",
                                       relief="flat", bd=4, width=20)
        self.entry_rec_mat.insert(0, self.usuario.get("matricula", ""))
        self.entry_rec_mat.grid(row=0, column=1, padx=10, ipady=4)

        tk.Label(ctrl, text="Top N:", font=("Arial", 10),
                 bg=BG2, fg=TEXT).grid(row=0, column=2)
        self.spin_top = tk.Spinbox(ctrl, from_=1, to=8, width=4,
                                    font=("Arial", 11), bg=BG, fg="white",
                                    buttonbackground=BG2, relief="flat")
        self.spin_top.delete(0, "end")
        self.spin_top.insert(0, "3")
        self.spin_top.grid(row=0, column=3, padx=6)

        tk.Button(ctrl, text="🔍 Recomendar",
                  font=("Arial", 10, "bold"), bg=GOLD, fg=BG3,
                  relief="flat", cursor="hand2", padx=12, pady=5,
                  command=self._ejecutar_recomendacion).grid(row=0, column=4, padx=10)

        # tabla de resultados
        cols = ("ID", "Título", "Categoría", "Veces Prestado")
        self.tabla_rec = ttk.Treeview(frame, columns=cols, show="headings", height=7)
        for col in cols:
            self.tabla_rec.heading(col, text=col)
        self.tabla_rec.column("ID", width=60, anchor="center")
        self.tabla_rec.column("Título", width=280)
        self.tabla_rec.column("Categoría", width=130)
        self.tabla_rec.column("Veces Prestado", width=110, anchor="center")

        sb = ttk.Scrollbar(frame, orient="vertical", command=self.tabla_rec.yview)
        self.tabla_rec.configure(yscrollcommand=sb.set)
        self.tabla_rec.pack(side="left", fill="both", expand=True, padx=(15, 0), pady=5)
        sb.pack(side="left", fill="y", pady=5)

        self.lbl_rec_info = tk.Label(frame, text="", font=("Arial", 9),
                                      bg=BG, fg=TEXT_DIM)
        self.lbl_rec_info.pack(pady=4)

    def _ejecutar_recomendacion(self) -> None:
        matricula = self.entry_rec_mat.get().strip()
        top_n = int(self.spin_top.get())
        if not matricula:
            messagebox.showwarning("Campo vacío", "Ingresa una matrícula", parent=self)
            return

        for item in self.tabla_rec.get_children():
            self.tabla_rec.delete(item)

        self.lbl_rec_info.config(text="Entrenando modelo…", fg=GOLD)
        self.update()
        recomendaciones = self.ml.recomendador.recomendar(matricula, top_n)

        if not recomendaciones:
            self.lbl_rec_info.config(
                text="No hay recomendaciones disponibles (sin historial suficiente).",
                fg=TEXT_DIM
            )
            return

        for r in recomendaciones:
            self.tabla_rec.insert("", "end", values=(
                r.get("id_libro", ""),
                r.get("titulo", ""),
                r.get("categoria", ""),
                r.get("frecuencia", 0),
            ))
        self.lbl_rec_info.config(
            text=f"✅ {len(recomendaciones)} libro(s) recomendado(s) para {matricula}",
            fg=GREEN
        )

    #  PESTAÑA 2 — Predicción de demanda
    
    def _tab_demanda(self) -> None:
        frame = tk.Frame(self.nb, bg=BG)
        self.nb.add(frame, text="📅 Demanda de Espacios")

        tk.Label(frame, text="Predicción de Demanda de Espacios (Regresión Lineal)",
                 font=("Arial", 12, "bold"), bg=BG, fg=GOLD).pack(pady=12)
        tk.Label(frame,
                 text="Estima cuántas reservas se esperan en un día y hora específicos.",
                 font=("Arial", 9), bg=BG, fg=TEXT_DIM).pack()

        # controles
        ctrl = tk.Frame(frame, bg=BG2, padx=20, pady=14)
        ctrl.pack(fill="x", padx=15, pady=10)

        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        tk.Label(ctrl, text="Día:", font=("Arial", 10), bg=BG2, fg=TEXT).grid(row=0, column=0)
        self.combo_dia = ttk.Combobox(ctrl, values=dias, state="readonly",
                                       font=("Arial", 10), width=12)
        self.combo_dia.set("Lunes")
        self.combo_dia.grid(row=0, column=1, padx=10)

        tk.Label(ctrl, text="Hora:", font=("Arial", 10), bg=BG2, fg=TEXT).grid(row=0, column=2)
        self.combo_hora_dem = ttk.Combobox(
            ctrl, values=[f"{h:02d}:00" for h in range(8, 21)],
            state="readonly", font=("Arial", 10), width=8
        )
        self.combo_hora_dem.set("10:00")
        self.combo_hora_dem.grid(row=0, column=3, padx=10)

        tk.Button(ctrl, text="📊 Predecir",
                  font=("Arial", 10, "bold"), bg=GOLD, fg=BG3,
                  relief="flat", cursor="hand2", padx=12, pady=5,
                  command=self._predecir_demanda).grid(row=0, column=4, padx=10)

        # resultado puntual
        self.lbl_pred_dem = tk.Label(frame, text="",
                                      font=("Arial", 16, "bold"), bg=BG, fg=GOLD)
        self.lbl_pred_dem.pack(pady=8)

        # tabla mapa de calor semanal
        tk.Label(frame, text="Mapa de calor semanal (predicción de reservas):",
                 font=("Arial", 10), bg=BG, fg=TEXT).pack(anchor="w", padx=15)

        cols_mc = ["Hora"] + dias
        self.tabla_mapa = ttk.Treeview(frame, columns=cols_mc,
                                        show="headings", height=8)
        for col in cols_mc:
            self.tabla_mapa.heading(col, text=col)
            ancho = 55 if col != "Hora" else 50
            self.tabla_mapa.column(col, width=ancho, anchor="center")

        sb2 = ttk.Scrollbar(frame, orient="vertical", command=self.tabla_mapa.yview)
        self.tabla_mapa.configure(yscrollcommand=sb2.set)
        self.tabla_mapa.pack(side="left", fill="both", expand=True,
                              padx=(15, 0), pady=5)
        sb2.pack(side="left", fill="y", pady=5)

        tk.Button(frame, text="🗓️ Generar mapa completo",
                  font=("Arial", 9), bg=BLUE, fg="white",
                  relief="flat", cursor="hand2", padx=10, pady=5,
                  command=self._mapa_calor).pack(pady=8)

    def _predecir_demanda(self) -> None:
        dias = ["Lunes", "Martes", "Miércoles", "Jueves",
                "Viernes", "Sábado", "Domingo"]
        dia_str = self.combo_dia.get()
        dia_num = dias.index(dia_str) if dia_str in dias else 0
        hora = int(self.combo_hora_dem.get().split(":")[0])

        self.lbl_pred_dem.config(text="Calculando…", fg=GOLD)
        self.update()
        valor = self.ml.predictor_espacios.predecir(dia_num, hora)
        self.lbl_pred_dem.config(
            text=f"Reservas esperadas el {dia_str} a las {hora:02d}:00 → {valor:.1f}",
            fg=GREEN
        )

    def _mapa_calor(self) -> None:
        for item in self.tabla_mapa.get_children():
            self.tabla_mapa.delete(item)
        self.lbl_pred_dem.config(text="Generando mapa…", fg=GOLD)
        self.update()

        mapa = self.ml.predictor_espacios.mapa_calor_semana()
        dias = ["Lunes", "Martes", "Miércoles", "Jueves",
                "Viernes", "Sábado", "Domingo"]
        horas = list(range(8, 21))

        for h in horas:
            fila = [f"{h:02d}:00"] + [f"{mapa[d][h]:.1f}" for d in dias]
            self.tabla_mapa.insert("", "end", values=fila)

        self.lbl_pred_dem.config(text="✅ Mapa de calor generado", fg=GREEN)

    #  PESTAÑA 3 — Análisis de Patrones
    
    def _tab_patrones(self) -> None:
        frame = tk.Frame(self.nb, bg=BG)
        self.nb.add(frame, text="📊 Análisis de Patrones")

        tk.Label(frame, text="Análisis de Patrones de Uso del Sistema",
                 font=("Arial", 12, "bold"), bg=BG, fg=GOLD).pack(pady=12)

        # sub-notebook dentro de la pestaña
        nb2 = ttk.Notebook(frame)
        nb2.pack(fill="both", expand=True, padx=10, pady=5)

        # — resumen general
        f_res = tk.Frame(nb2, bg=BG)
        nb2.add(f_res, text="Resumen")
        self._subtab_resumen(f_res)

        # — categorías populares
        f_cat = tk.Frame(nb2, bg=BG)
        nb2.add(f_cat, text="Categorías")
        self._subtab_categorias(f_cat)

        # — uso por día
        f_dia = tk.Frame(nb2, bg=BG)
        nb2.add(f_dia, text="Uso por día")
        self._subtab_uso_dia(f_dia)

        # — usuarios activos
        f_usr = tk.Frame(nb2, bg=BG)
        nb2.add(f_usr, text="Usuarios activos")
        self._subtab_usuarios(f_usr)

        # — tendencia mensual
        f_tend = tk.Frame(nb2, bg=BG)
        nb2.add(f_tend, text="Tendencia mensual")
        self._subtab_tendencia(f_tend)

    def _subtab_resumen(self, frame: tk.Frame) -> None:
        tk.Label(frame, text="Métricas clave del sistema",
                 font=("Arial", 11, "bold"), bg=BG, fg=TEXT).pack(pady=10)

        stats = self.ml.analizador.resumen_general()
        if "error" in stats:
            tk.Label(frame, text=stats["error"], bg=BG, fg=RED).pack()
            return

        fichas = [
            (" Total Libros",       stats["total_libros"],           "#243156"),
            (" Libros Disponibles", stats["libros_disponibles"],      "#1d4020"),
            (" Préstamos totales",  stats["total_prestamos"],         "#243156"),
            (" Préstamos activos",  stats["prestamos_activos"],       "#2d2d10"),
            (" Devueltos",          stats["prestamos_devueltos"],      "#1d4020"),
            (" Tasa devolución",    f"{stats['tasa_devolucion_pct']}%","#1d4020"),
            (" Reservas totales",   stats["total_reservas"],          "#243156"),
            (" Canceladas",         stats["reservas_canceladas"],      "#401d1d"),
            (" Usuarios",           stats["total_usuarios"],          "#243156"),
        ]

        fila, col = 0, 0
        grid = tk.Frame(frame, bg=BG)
        grid.pack(padx=20, pady=5)
        for titulo, valor, color in fichas:
            card = tk.Frame(grid, bg=color, padx=16, pady=12)
            card.grid(row=fila, column=col, padx=6, pady=6)
            tk.Label(card, text=str(valor), font=("Arial", 18, "bold"),
                     bg=color, fg=GOLD).pack()
            tk.Label(card, text=titulo, font=("Arial", 8),
                     bg=color, fg=TEXT_DIM).pack()
            col += 1
            if col >= 3:
                col = 0
                fila += 1

    def _subtab_categorias(self, frame: tk.Frame) -> None:
        tk.Label(frame, text="Categorías más populares (por préstamos)",
                 font=("Arial", 11, "bold"), bg=BG, fg=TEXT).pack(pady=10)

        cols = ("Posición", "Categoría", "Préstamos")
        tabla = ttk.Treeview(frame, columns=cols, show="headings", height=10)
        for col in cols:
            tabla.heading(col, text=col)
        tabla.column("Posición", width=70, anchor="center")
        tabla.column("Categoría", width=200)
        tabla.column("Préstamos", width=100, anchor="center")

        datos = self.ml.analizador.categorias_mas_populares()
        for i, d in enumerate(datos, 1):
            tabla.insert("", "end", values=(i, d["categoria"], d["prestamos"]))

        tabla.pack(fill="both", expand=True, padx=15, pady=5)
        self._boton_grafica(frame, self._grafica_categorias)

    def _subtab_uso_dia(self, frame: tk.Frame) -> None:
        tk.Label(frame, text="Actividad por día de la semana",
                 font=("Arial", 11, "bold"), bg=BG, fg=TEXT).pack(pady=10)

        datos = self.ml.analizador.uso_por_dia_semana()
        cols = ("Día", "Préstamos estimados")
        tabla = ttk.Treeview(frame, columns=cols, show="headings", height=8)
        for col in cols:
            tabla.heading(col, text=col)
        tabla.column("Día", width=200)
        tabla.column("Préstamos estimados", width=160, anchor="center")

        max_val = max(datos.values()) if datos else 1
        for dia, val in datos.items():
            barra = "█" * int(val / max_val * 20)
            tabla.insert("", "end", values=(dia, f"{val}  {barra}"))

        tabla.pack(fill="both", expand=True, padx=15, pady=5)
        self._boton_grafica(frame, self._grafica_dias)

    def _subtab_usuarios(self, frame: tk.Frame) -> None:
        tk.Label(frame, text="Usuarios con más préstamos",
                 font=("Arial", 11, "bold"), bg=BG, fg=TEXT).pack(pady=10)

        cols = ("Matrícula", "Nombre", "Préstamos")
        tabla = ttk.Treeview(frame, columns=cols, show="headings", height=8)
        for col in cols:
            tabla.heading(col, text=col)
        tabla.column("Matrícula", width=120, anchor="center")
        tabla.column("Nombre", width=230)
        tabla.column("Préstamos", width=90, anchor="center")

        datos = self.ml.analizador.usuarios_mas_activos(top_n=10)
        for d in datos:
            tabla.insert("", "end", values=(
                d["id_usuario"], d.get("nombre", d["id_usuario"]), d["prestamos"]
            ))

        tabla.pack(fill="both", expand=True, padx=15, pady=5)

    def _subtab_tendencia(self, frame: tk.Frame) -> None:
        tk.Label(frame, text="Tendencia mensual de préstamos",
                 font=("Arial", 11, "bold"), bg=BG, fg=TEXT).pack(pady=10)

        datos = self.ml.analizador.tendencia_mensual()
        cols = ("Mes", "Préstamos")
        tabla = ttk.Treeview(frame, columns=cols, show="headings", height=8)
        for col in cols:
            tabla.heading(col, text=col)
        tabla.column("Mes", width=160, anchor="center")
        tabla.column("Préstamos", width=130, anchor="center")

        for mes, val in sorted(datos.items()):
            tabla.insert("", "end", values=(mes, val))

        tabla.pack(fill="both", expand=True, padx=15, pady=5)
        self._boton_grafica(frame, self._grafica_tendencia)

    def _boton_grafica(self, frame: tk.Frame, comando) -> None:
        tk.Button(frame, text="📈 Ver gráfica",
                  font=("Arial", 9), bg=BLUE, fg="white",
                  relief="flat", cursor="hand2", padx=10, pady=5,
                  command=comando).pack(pady=6)

    # gráficas matplotlib 
    def _grafica_categorias(self) -> None:
        try:
            import matplotlib.pyplot as plt
            datos = self.ml.analizador.categorias_mas_populares()
            categorias = [d["categoria"] for d in datos]
            valores = [d["prestamos"] for d in datos]
            fig, ax = plt.subplots(figsize=(7, 4), facecolor="#1a2744")
            ax.set_facecolor("#243156")
            bars = ax.barh(categorias, valores, color=GOLD)
            ax.set_xlabel("Préstamos", color=TEXT)
            ax.set_title("Categorías más populares", color=GOLD, fontsize=13)
            ax.tick_params(colors=TEXT)
            for spine in ax.spines.values():
                spine.set_edgecolor("#3d5080")
            plt.tight_layout()
            plt.show()
        except ImportError:
            messagebox.showinfo("Info", "Instala matplotlib para ver gráficas", parent=self)

    def _grafica_dias(self) -> None:
        try:
            import matplotlib.pyplot as plt
            datos = self.ml.analizador.uso_por_dia_semana()
            dias = list(datos.keys())
            vals = list(datos.values())
            fig, ax = plt.subplots(figsize=(7, 4), facecolor="#1a2744")
            ax.set_facecolor("#243156")
            ax.bar(dias, vals, color=BLUE)
            ax.set_ylabel("Actividad estimada", color=TEXT)
            ax.set_title("Uso por día de la semana", color=GOLD, fontsize=13)
            ax.tick_params(colors=TEXT)
            plt.xticks(rotation=30)
            plt.tight_layout()
            plt.show()
        except ImportError:
            messagebox.showinfo("Info", "Instala matplotlib para ver gráficas", parent=self)

    def _grafica_tendencia(self) -> None:
        try:
            import matplotlib.pyplot as plt
            datos = self.ml.analizador.tendencia_mensual()
            meses = sorted(datos.keys())
            vals = [datos[m] for m in meses]
            fig, ax = plt.subplots(figsize=(8, 4), facecolor="#1a2744")
            ax.set_facecolor("#243156")
            ax.plot(meses, vals, marker="o", color=GREEN, linewidth=2)
            ax.fill_between(meses, vals, alpha=0.2, color=GREEN)
            ax.set_ylabel("Préstamos", color=TEXT)
            ax.set_title("Tendencia mensual de préstamos", color=GOLD, fontsize=13)
            ax.tick_params(colors=TEXT)
            plt.xticks(rotation=30)
            plt.tight_layout()
            plt.show()
        except ImportError:
            messagebox.showinfo("Info", "Instala matplotlib para ver gráficas", parent=self)

    #  PESTAÑA 4 — Predictor de Devolución Tardía
    
    def _tab_devolucion(self) -> None:
        frame = tk.Frame(self.nb, bg=BG)
        self.nb.add(frame, text="⏰ Devoluciones Tardías")

        tk.Label(frame, text="Predictor de Devolución Tardía (Árbol de Decisión)",
                 font=("Arial", 12, "bold"), bg=BG, fg=GOLD).pack(pady=12)
        tk.Label(frame,
                 text="Predice si un préstamo tiene riesgo de no ser devuelto a tiempo (>7 días).",
                 font=("Arial", 9), bg=BG, fg=TEXT_DIM).pack()

        # controles
        ctrl = tk.Frame(frame, bg=BG2, padx=20, pady=14)
        ctrl.pack(fill="x", padx=15, pady=10)

        categorias = ["Programacion", "Matematicas", "Ciencias",
                      "Algoritmos", "Redes", "IA", "Literatura", "Historia"]
        tk.Label(ctrl, text="Categoría:", font=("Arial", 10),
                 bg=BG2, fg=TEXT).grid(row=0, column=0, sticky="w")
        self.combo_cat_dev = ttk.Combobox(ctrl, values=categorias,
                                           state="readonly", font=("Arial", 10), width=14)
        self.combo_cat_dev.set("Programacion")
        self.combo_cat_dev.grid(row=0, column=1, padx=8)

        dias = ["Lunes", "Martes", "Miércoles", "Jueves",
                "Viernes", "Sábado", "Domingo"]
        tk.Label(ctrl, text="Día de préstamo:", font=("Arial", 10),
                 bg=BG2, fg=TEXT).grid(row=0, column=2, sticky="w")
        self.combo_dia_dev = ttk.Combobox(ctrl, values=dias,
                                           state="readonly", font=("Arial", 10), width=12)
        self.combo_dia_dev.set("Lunes")
        self.combo_dia_dev.grid(row=0, column=3, padx=8)

        tk.Label(ctrl, text="Hora:", font=("Arial", 10),
                 bg=BG2, fg=TEXT).grid(row=0, column=4)
        self.combo_hora_dev = ttk.Combobox(
            ctrl, values=[f"{h:02d}:00" for h in range(8, 21)],
            state="readonly", font=("Arial", 10), width=8
        )
        self.combo_hora_dev.set("10:00")
        self.combo_hora_dev.grid(row=0, column=5, padx=8)

        tk.Button(ctrl, text="🔮 Predecir",
                  font=("Arial", 10, "bold"), bg=GOLD, fg=BG3,
                  relief="flat", cursor="hand2", padx=12, pady=5,
                  command=self._predecir_devolucion).grid(row=0, column=6, padx=12)

        # resultado
        self.frame_resultado = tk.Frame(frame, bg=BG2, padx=20, pady=15)
        self.frame_resultado.pack(fill="x", padx=15, pady=5)

        self.lbl_riesgo = tk.Label(self.frame_resultado, text="",
                                    font=("Arial", 14, "bold"), bg=BG2, fg=GOLD)
        self.lbl_riesgo.pack()
        self.lbl_prob = tk.Label(self.frame_resultado, text="",
                                  font=("Arial", 11), bg=BG2, fg=TEXT)
        self.lbl_prob.pack(pady=4)
        self.lbl_rec_dev = tk.Label(self.frame_resultado, text="",
                                     font=("Arial", 10), bg=BG2, fg=TEXT_DIM,
                                     wraplength=700, justify="center")
        self.lbl_rec_dev.pack()

        # importancia de variables
        tk.Label(frame, text="Importancia de variables del modelo:",
                 font=("Arial", 10), bg=BG, fg=TEXT).pack(anchor="w", padx=15, pady=(12, 4))

        cols = ("Variable", "Importancia (%)")
        self.tabla_imp = ttk.Treeview(frame, columns=cols,
                                       show="headings", height=4)
        for col in cols:
            self.tabla_imp.heading(col, text=col)
        self.tabla_imp.column("Variable", width=260)
        self.tabla_imp.column("Importancia (%)", width=130, anchor="center")
        self.tabla_imp.pack(fill="x", padx=15, pady=4)

        tk.Button(frame, text="⚙️ Entrenar modelo y ver importancias",
                  font=("Arial", 9), bg=BLUE, fg="white",
                  relief="flat", cursor="hand2", padx=10, pady=5,
                  command=self._entrenar_devolucion).pack(pady=6)

    def _predecir_devolucion(self) -> None:
        dias = ["Lunes", "Martes", "Miércoles", "Jueves",
                "Viernes", "Sábado", "Domingo"]
        categoria = self.combo_cat_dev.get()
        dia_str = self.combo_dia_dev.get()
        dia_num = dias.index(dia_str) if dia_str in dias else 0
        hora = int(self.combo_hora_dev.get().split(":")[0])

        resultado = self.ml.predictor_devolucion.predecir(categoria, dia_num, hora)

        if resultado["tardia"]:
            self.lbl_riesgo.config(text=" RIESGO ALTO de devolución tardía", fg=RED)
        else:
            self.lbl_riesgo.config(text=" Devolución probable a tiempo", fg=GREEN)

        self.lbl_prob.config(
            text=f"Probabilidad de retraso: {resultado['probabilidad']}%"
        )
        self.lbl_rec_dev.config(text=resultado["recomendacion"])

    def _entrenar_devolucion(self) -> None:
        msg = self.ml.predictor_devolucion.entrenar()
        messagebox.showinfo("Entrenamiento", msg, parent=self)

        for item in self.tabla_imp.get_children():
            self.tabla_imp.delete(item)

        importancias = self.ml.predictor_devolucion.importancia_variables()
        for var, val in sorted(importancias.items(), key=lambda x: -x[1]):
            barra = "█" * int(val / 5)
            self.tabla_imp.insert("", "end", values=(var, f"{val}%  {barra}"))
