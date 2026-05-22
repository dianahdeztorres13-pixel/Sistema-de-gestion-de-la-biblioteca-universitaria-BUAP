"""
Módulo de Machine Learning y Análisis de Datos
Sistema Biblioteca BUAP

Modelos implementados:
  1. Recomendación de libros por categoría (KMeans clustering)
  2. Predicción de demanda de espacios (Regresión Lineal)
  3. Análisis de patrones de uso de préstamos (Pandas + Matplotlib)
  4. Predicción de devoluciones tardías (Árbol de Decisión)
"""

import os
import json
from datetime import datetime, timedelta


# Utilidad: generar dataset sintético si los datos reales son pocos

def _generar_dataset_prestamos(prestamos: list, libros: list) -> list[dict]:
    """
    Enriquece la lista de préstamos con campos numéricos útiles para ML.
    Si hay menos de 20 registros, genera datos sintéticos adicionales.
    """
    import random
    random.seed(42)

    categorias = ["Programacion", "Matematicas", "Ciencias",
                  "Algoritmos", "Redes", "IA", "Literatura", "Historia"]
    tipos_usuario = ["estudiante", "docente", "visitante"]

    # construir lookup de libro -> categoria
    cat_map = {l["id_libro"]: l.get("categoria", "Otro") for l in libros}

    dataset = []
    for p in prestamos:
        try:
            fecha = datetime.strptime(p["fecha_prestamo"], "%d/%m/%Y")
        except ValueError:
            fecha = datetime.now()
        dataset.append({
            "id_prestamo": p["id_prestamo"],
            "id_usuario": p["id_usuario"],
            "id_libro": p["id_libro"],
            "categoria": cat_map.get(p["id_libro"], "Otro"),
            "dia_semana": fecha.weekday(),          # 0=lunes, 6=domingo
            "hora_dia": random.randint(8, 20),      # simulado
            "devuelto": 1 if p["estado"] == "devuelto" else 0,
            "dias_prestamo": random.randint(1, 15),
        })

    # si hay pocos datos, generar sintéticos
    while len(dataset) < 60:
        categoria = random.choice(categorias)
        tipo = random.choice(tipos_usuario)
        dias = random.randint(1, 21)
        dataset.append({
            "id_prestamo": f"SYN{len(dataset):03d}",
            "id_usuario": f"USR{random.randint(1, 20):03d}",
            "id_libro": f"L{random.randint(1, 8):03d}",
            "categoria": categoria,
            "dia_semana": random.randint(0, 6),
            "hora_dia": random.randint(8, 20),
            "devuelto": random.choices([0, 1], weights=[0.3, 0.7])[0],
            "dias_prestamo": dias,
        })

    return dataset


def _generar_dataset_reservas(reservas: list, espacios: list) -> list[dict]:
    """Enriquece reservas con variables numéricas."""
    import random
    random.seed(7)

    tipo_map = {e["id_espacio"]: e["tipo"] for e in espacios}
    cap_map = {e["id_espacio"]: e["capacidad"] for e in espacios}

    dataset = []
    for r in reservas:
        try:
            fecha = datetime.strptime(r["fecha"], "%d/%m/%Y")
        except ValueError:
            fecha = datetime.now()
        hora_num = int(r.get("hora", "09:00").split(":")[0])
        dataset.append({
            "id_espacio": r["id_espacio"],
            "tipo": tipo_map.get(r["id_espacio"], "cubiculo"),
            "capacidad": cap_map.get(r["id_espacio"], 4),
            "dia_semana": fecha.weekday(),
            "hora_num": hora_num,
            "cancelada": 1 if r["estado"] == "cancelada" else 0,
        })

    tipos = ["cubiculo", "taller", "videojuegos"]
    while len(dataset) < 80:
        tipo = random.choice(tipos)
        dataset.append({
            "id_espacio": f"{tipo[0].upper()}{random.randint(1,3):03d}",
            "tipo": tipo,
            "capacidad": random.choice([4, 6, 8, 15, 20]),
            "dia_semana": random.randint(0, 6),
            "hora_num": random.randint(8, 18),
            "cancelada": random.choices([0, 1], weights=[0.8, 0.2])[0],
        })

    return dataset

# 1. RECOMENDADOR DE LIBROS  (KMeans sobre categorías + frecuencia de préstamo)

class RecomendadorLibros:
    """
    Agrupa libros en clústeres según su categoría y popularidad,
    luego recomienda libros del mismo clúster que el usuario ha leído.
    """

    def __init__(self, sistema):
        self.sistema = sistema
        self.modelo = None
        self.df_libros = None
        self._entrenado = False

    def entrenar(self) -> str:
        """Entrena el modelo KMeans y retorna un resumen."""
        try:
            import pandas as pd
            import numpy as np
            from sklearn.cluster import KMeans
            from sklearn.preprocessing import LabelEncoder

            prestamos = self.sistema.prestamos
            libros = self.sistema.libros

            # contar cuántas veces se prestó cada libro
            frecuencia = {}
            for p in prestamos:
                frecuencia[p["id_libro"]] = frecuencia.get(p["id_libro"], 0) + 1

            # construir dataframe de libros
            rows = []
            for l in libros:
                rows.append({
                    "id_libro": l["id_libro"],
                    "titulo": l["titulo"],
                    "categoria": l["categoria"],
                    "disponibilidad": 1 if l["disponibilidad"] else 0,
                    "frecuencia": frecuencia.get(l["id_libro"], 0),
                })

            self.df_libros = pd.DataFrame(rows)

            # codificar categoría
            le = LabelEncoder()
            self.df_libros["cat_encoded"] = le.fit_transform(
                self.df_libros["categoria"]
            )
            self._label_encoder = le

            X = self.df_libros[["cat_encoded", "frecuencia", "disponibilidad"]].values

            n_clusters = min(4, len(X))
            self.modelo = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            self.modelo.fit(X)
            self.df_libros["cluster"] = self.modelo.labels_
            self._entrenado = True

            return f"Modelo entrenado: {n_clusters} clústeres sobre {len(libros)} libros"
        except ImportError:
            return "ERROR: Instala scikit-learn y pandas (pip install scikit-learn pandas)"
        except Exception as e:
            return f"Error entrenando modelo: {e}"

    def recomendar(self, matricula: str, top_n: int = 3) -> list[dict]:
        """Devuelve top_n libros recomendados para el usuario."""
        if not self._entrenado:
            self.entrenar()
        if self.df_libros is None:
            return []

        # libros ya leídos por el usuario
        leidos = {p["id_libro"] for p in self.sistema.prestamos
                  if p["id_usuario"] == matricula}

        if leidos:
            # encontrar el clúster más frecuente entre los libros leídos
            clusters_leidos = self.df_libros[
                self.df_libros["id_libro"].isin(leidos)
            ]["cluster"].tolist()
            cluster_objetivo = max(set(clusters_leidos), key=clusters_leidos.count)
        else:
            # sin historial: recomendar los más populares
            cluster_objetivo = self.df_libros.groupby("cluster")["frecuencia"].sum().idxmax()

        # filtrar: mismo clúster, disponible, no leído
        candidatos = self.df_libros[
            (self.df_libros["cluster"] == cluster_objetivo) &
            (self.df_libros["disponibilidad"] == 1) &
            (~self.df_libros["id_libro"].isin(leidos))
        ].sort_values("frecuencia", ascending=False).head(top_n)

        return candidatos[["id_libro", "titulo", "categoria", "frecuencia"]].to_dict("records")


# 2. PREDICTOR DE DEMANDA DE ESPACIOS  (Regresión Lineal)

class PredictorDemandaEspacios:
    """
    Predice cuántas reservas habrá en un día y hora dados
    usando regresión lineal sobre el historial de reservas.
    """

    def __init__(self, sistema):
        self.sistema = sistema
        self.modelo = None
        self._entrenado = False

    def entrenar(self) -> str:
        try:
            import pandas as pd
            import numpy as np
            from sklearn.linear_model import LinearRegression
            from sklearn.model_selection import train_test_split
            from sklearn.metrics import mean_absolute_error

            dataset = _generar_dataset_reservas(
                self.sistema.reservas, self.sistema.espacios
            )
            df = pd.DataFrame(dataset)

            # agrupar por día + hora → contar reservas
            df_agg = (
                df.groupby(["dia_semana", "hora_num"])
                .size()
                .reset_index(name="num_reservas")
            )

            X = df_agg[["dia_semana", "hora_num"]].values
            y = df_agg["num_reservas"].values

            if len(X) < 4:
                return "Datos insuficientes para entrenamiento"

            if len(X) >= 8:
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.25, random_state=42
                )
            else:
                X_train, X_test, y_train, y_test = X, X, y, y

            self.modelo = LinearRegression()
            self.modelo.fit(X_train, y_train)

            y_pred = self.modelo.predict(X_test)
            mae = mean_absolute_error(y_test, y_pred)
            self._entrenado = True
            return f"Regresión entrenada — MAE: {mae:.2f} reservas"
        except ImportError:
            return "ERROR: Instala scikit-learn y pandas"
        except Exception as e:
            return f"Error: {e}"

    def predecir(self, dia_semana: int, hora: int) -> float:
        """
        Predice número esperado de reservas.
        dia_semana: 0=lunes, 6=domingo  |  hora: 8–20
        """
        if not self._entrenado:
            self.entrenar()
        if self.modelo is None:
            return 0.0
        import numpy as np
        pred = self.modelo.predict(np.array([[dia_semana, hora]]))[0]
        return max(0.0, round(float(pred), 2))

    def mapa_calor_semana(self) -> dict:
        """Devuelve predicciones para toda la semana, cada hora."""
        dias = ["Lunes", "Martes", "Miércoles", "Jueves",
                "Viernes", "Sábado", "Domingo"]
        horas = list(range(8, 21))
        mapa = {}
        for i, dia in enumerate(dias):
            mapa[dia] = {h: self.predecir(i, h) for h in horas}
        return mapa


# 3. ANÁLISIS DE PATRONES DE USO  (Pandas + estadísticas descriptivas)

class AnalizadorPatrones:
    """
    Calcula estadísticas descriptivas y tendencias sobre el uso
    de la biblioteca: préstamos, reservas y usuarios.
    """

    def __init__(self, sistema):
        self.sistema = sistema

    def resumen_general(self) -> dict:
        """Retorna métricas clave del sistema."""
        try:
            import pandas as pd

            df_p = pd.DataFrame(self.sistema.prestamos) if self.sistema.prestamos else pd.DataFrame()
            df_r = pd.DataFrame(self.sistema.reservas) if self.sistema.reservas else pd.DataFrame()

            total_prestamos = len(df_p)
            total_devueltos = int((df_p["estado"] == "devuelto").sum()) if not df_p.empty else 0
            tasa_devolucion = (total_devueltos / total_prestamos * 100) if total_prestamos > 0 else 0

            total_reservas = len(df_r)
            total_canceladas = int((df_r["estado"] == "cancelada").sum()) if not df_r.empty else 0
            tasa_cancelacion = (total_canceladas / total_reservas * 100) if total_reservas > 0 else 0

            return {
                "total_prestamos": total_prestamos,
                "prestamos_activos": total_prestamos - total_devueltos,
                "prestamos_devueltos": total_devueltos,
                "tasa_devolucion_pct": round(tasa_devolucion, 1),
                "total_reservas": total_reservas,
                "reservas_activas": total_reservas - total_canceladas,
                "reservas_canceladas": total_canceladas,
                "tasa_cancelacion_pct": round(tasa_cancelacion, 1),
                "total_usuarios": len(self.sistema.usuarios),
                "total_libros": len(self.sistema.libros),
                "libros_disponibles": sum(1 for l in self.sistema.libros if l["disponibilidad"]),
            }
        except ImportError:
            return {"error": "Instala pandas"}

    def categorias_mas_populares(self) -> list[dict]:
        """Ranking de categorías por número de préstamos."""
        try:
            import pandas as pd
            dataset = _generar_dataset_prestamos(
                self.sistema.prestamos, self.sistema.libros
            )
            df = pd.DataFrame(dataset)
            ranking = (
                df.groupby("categoria")
                .size()
                .reset_index(name="prestamos")
                .sort_values("prestamos", ascending=False)
            )
            return ranking.to_dict("records")
        except ImportError:
            return []

    def uso_por_dia_semana(self) -> dict:
        """Cuenta préstamos y reservas por día de la semana."""
        try:
            import pandas as pd
            dias = ["Lunes", "Martes", "Miércoles", "Jueves",
                    "Viernes", "Sábado", "Domingo"]
            dataset = _generar_dataset_prestamos(
                self.sistema.prestamos, self.sistema.libros
            )
            df = pd.DataFrame(dataset)
            conteo = df.groupby("dia_semana").size()
            return {dias[i]: int(conteo.get(i, 0)) for i in range(7)}
        except ImportError:
            return {}

    def usuarios_mas_activos(self, top_n: int = 5) -> list[dict]:
        """Top usuarios con más préstamos."""
        try:
            import pandas as pd
            if not self.sistema.prestamos:
                return []
            df = pd.DataFrame(self.sistema.prestamos)
            ranking = (
                df.groupby("id_usuario")
                .size()
                .reset_index(name="prestamos")
                .sort_values("prestamos", ascending=False)
                .head(top_n)
            )
            # agregar nombre
            nombre_map = {u["matricula"]: u["nombre"] for u in self.sistema.usuarios}
            ranking["nombre"] = ranking["id_usuario"].map(
                lambda m: nombre_map.get(m, m)
            )
            return ranking.to_dict("records")
        except ImportError:
            return []

    def tendencia_mensual(self) -> dict:
        """Agrupa préstamos por mes (formato MM/YYYY)."""
        try:
            import pandas as pd
            import random
            random.seed(1)

            # generar fechas distribuidas en 6 meses para el demo
            base = datetime(2025, 12, 1)
            fechas = []
            for p in self.sistema.prestamos:
                try:
                    fechas.append(datetime.strptime(p["fecha_prestamo"], "%d/%m/%Y"))
                except ValueError:
                    fechas.append(base + timedelta(days=random.randint(0, 180)))

            # rellenar hasta 30 registros
            while len(fechas) < 30:
                fechas.append(base + timedelta(days=random.randint(0, 180)))

            df = pd.DataFrame({"fecha": fechas})
            df["mes"] = df["fecha"].dt.to_period("M").astype(str)
            conteo = df.groupby("mes").size().sort_index()
            return dict(conteo)
        except ImportError:
            return {}

# 4. PREDICTOR DE DEVOLUCIONES TARDÍAS  (Árbol de Decisión)

class PredictorDevolucionTardia:
    """
    Predice si un usuario devolverá un libro tarde (>7 días)
    basándose en: categoría, día de la semana, tipo de usuario.
    """

    def __init__(self, sistema):
        self.sistema = sistema
        self.modelo = None
        self._entrenado = False
        self._label_encoders = {}

    def entrenar(self) -> str:
        try:
            import pandas as pd
            import numpy as np
            from sklearn.tree import DecisionTreeClassifier
            from sklearn.preprocessing import LabelEncoder
            from sklearn.model_selection import train_test_split
            from sklearn.metrics import accuracy_score, classification_report

            dataset = _generar_dataset_prestamos(
                self.sistema.prestamos, self.sistema.libros
            )
            df = pd.DataFrame(dataset)

            # variable objetivo: tardía si dias_prestamo > 7
            df["tardia"] = (df["dias_prestamo"] > 7).astype(int)

            # codificar categoría
            le = LabelEncoder()
            df["cat_enc"] = le.fit_transform(df["categoria"])
            self._label_encoders["categoria"] = le

            X = df[["cat_enc", "dia_semana", "hora_dia"]].values
            y = df["tardia"].values

            # si solo hay una clase, no podemos estratificar ni clasificar bien
            clases_unicas = set(y.tolist())
            if len(clases_unicas) < 2:
                # forzar variedad mínima sintética
                import numpy as np
                if 1 not in clases_unicas:
                    y[-1] = 1
                else:
                    y[-1] = 0

            try:
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.25, random_state=42, stratify=y
                )
            except ValueError:
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.25, random_state=42
                )

            self.modelo = DecisionTreeClassifier(max_depth=4, random_state=42)
            self.modelo.fit(X_train, y_train)

            y_pred = self.modelo.predict(X_test)
            acc = accuracy_score(y_test, y_pred)
            self._entrenado = True
            return f"Árbol de decisión entrenado — Accuracy: {acc:.1%}"
        except ImportError:
            return "ERROR: Instala scikit-learn y pandas"
        except Exception as e:
            return f"Error: {e}"

    def predecir(self, categoria: str, dia_semana: int, hora: int) -> dict:
        """
        Retorna {'tardia': bool, 'probabilidad': float, 'recomendacion': str}
        """
        if not self._entrenado:
            self.entrenar()
        if self.modelo is None:
            return {"tardia": False, "probabilidad": 0.0, "recomendacion": "Sin modelo"}

        try:
            le = self._label_encoders["categoria"]
            categorias_conocidas = list(le.classes_)
            if categoria not in categorias_conocidas:
                cat_enc = 0
            else:
                cat_enc = le.transform([categoria])[0]

            import numpy as np
            X = np.array([[cat_enc, dia_semana, hora]])
            proba = self.modelo.predict_proba(X)[0]
            pred = self.modelo.predict(X)[0]
            prob_tardia = float(proba[1]) if len(proba) > 1 else 0.0

            if prob_tardia > 0.65:
                rec = "⚠️ Alto riesgo de devolución tardía. Considera fecha límite más corta."
            elif prob_tardia > 0.35:
                rec = "🟡 Riesgo moderado. Enviar recordatorio a los 5 días."
            else:
                rec = "✅ Baja probabilidad de retraso."

            return {
                "tardia": bool(pred),
                "probabilidad": round(prob_tardia * 100, 1),
                "recomendacion": rec,
            }
        except Exception as e:
            return {"tardia": False, "probabilidad": 0.0, "recomendacion": str(e)}

    def importancia_variables(self) -> dict:
        """Retorna la importancia de cada variable del árbol."""
        if not self._entrenado or self.modelo is None:
            return {}
        nombres = ["Categoría del Libro", "Día de la Semana", "Hora del Día"]
        importancias = self.modelo.feature_importances_
        return {n: round(float(v) * 100, 1) for n, v in zip(nombres, importancias)}

# Fachada: ML_Manager  — punto de acceso único desde la GUI

class ML_Manager:
    """
    Clase fachada que agrupa todos los modelos de ML.
    La ventana de ML solo necesita instanciar esta clase.
    """

    def __init__(self, sistema):
        self.sistema = sistema
        self.recomendador = RecomendadorLibros(sistema)
        self.predictor_espacios = PredictorDemandaEspacios(sistema)
        self.analizador = AnalizadorPatrones(sistema)
        self.predictor_devolucion = PredictorDevolucionTardia(sistema)

    def entrenar_todos(self) -> list[str]:
        """Entrena todos los modelos y devuelve los mensajes."""
        return [
            f"Recomendador: {self.recomendador.entrenar()}",
            f"Demanda:       {self.predictor_espacios.entrenar()}",
            f"Devoluciones:  {self.predictor_devolucion.entrenar()}",
        ]
