import json
import os
from datetime import datetime
from clases.modelos import Usuario, Libro, Espacio, Reserva, Prestamo

class Sistema:
    def __init__(self):
        self.usuarios = []
        self.libros = []
        self.espacios = []
        self.reservas = []
        self.prestamos = []
        self.usuario_activo = None

        # crear carpeta datos si no existe
        if not os.path.exists("datos"):
            os.makedirs("datos")

        self.cargar_datos()

        # si no hay datos iniciales, cargar ejemplos
        if len(self.libros) == 0:
            self._cargar_datos_ejemplo()

    def _cargar_datos_ejemplo(self):
        libros_ejemplo = [
            {"id_libro": "L001", "titulo": "Introduccion a Python", "autor": "Mark Lutz", "categoria": "Programacion", "disponibilidad": True},
            {"id_libro": "L002", "titulo": "Estructuras de Datos", "autor": "Thomas Cormen", "categoria": "Algoritmos", "disponibilidad": True},
            {"id_libro": "L003", "titulo": "Calculo Diferencial", "autor": "James Stewart", "categoria": "Matematicas", "disponibilidad": False},
            {"id_libro": "L004", "titulo": "Fisica Universitaria", "autor": "Sears Zemansky", "categoria": "Ciencias", "disponibilidad": True},
            {"id_libro": "L005", "titulo": "Base de Datos", "autor": "Ramez Elmasri", "categoria": "Programacion", "disponibilidad": True},
            {"id_libro": "L006", "titulo": "Redes de Computadoras", "autor": "Andrew Tanenbaum", "categoria": "Redes", "disponibilidad": True},
        ]
        espacios_ejemplo = [
            {"id_espacio": "C001", "tipo": "cubiculo", "capacidad": 4, "disponibilidad": True},
            {"id_espacio": "C002", "tipo": "cubiculo", "capacidad": 4, "disponibilidad": True},
            {"id_espacio": "C003", "tipo": "cubiculo", "capacidad": 6, "disponibilidad": False},
            {"id_espacio": "T001", "tipo": "taller", "capacidad": 20, "disponibilidad": True},
            {"id_espacio": "T002", "tipo": "taller", "capacidad": 15, "disponibilidad": True},
            {"id_espacio": "V001", "tipo": "videojuegos", "capacidad": 8, "disponibilidad": True},
            {"id_espacio": "V002", "tipo": "videojuegos", "capacidad": 8, "disponibilidad": False},
        ]
        # usuario admin por defecto
        usuarios_ejemplo = [
            {"matricula": "admin", "nombre": "Administrador", "correo": "admin@buap.mx",
             "contrasena": "admin123", "tipo": "admin", "codigoQR": None},
        ]
        self.libros = libros_ejemplo
        self.espacios = espacios_ejemplo
        self.usuarios = usuarios_ejemplo
        self.guardar_datos()

    def cargar_datos(self):
        archivos = {
            "datos/usuarios.json": "usuarios",
            "datos/libros.json": "libros",
            "datos/espacios.json": "espacios",
            "datos/reservas.json": "reservas",
            "datos/prestamos.json": "prestamos"
        }
        for archivo, atributo in archivos.items():
            try:
                if os.path.exists(archivo):
                    with open(archivo, "r", encoding="utf-8") as f:
                        setattr(self, atributo, json.load(f))
            except:
                pass  # si falla simplemente deja la lista vacia

    def guardar_datos(self):
        datos = {
            "datos/usuarios.json": self.usuarios,
            "datos/libros.json": self.libros,
            "datos/espacios.json": self.espacios,
            "datos/reservas.json": self.reservas,
            "datos/prestamos.json": self.prestamos
        }
        for archivo, lista in datos.items():
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump(lista, f, ensure_ascii=False, indent=2)

    def validar_login(self, matricula, contrasena):
        for u in self.usuarios:
            if u['matricula'] == matricula and u['contrasena'] == contrasena:
                self.usuario_activo = u
                return u
        return None

    def validar_qr(self, matricula):
        for u in self.usuarios:
            if u['matricula'] == matricula:
                self.usuario_activo = u
                return u
        return None

    def registrar_usuario(self, matricula, nombre, correo, contrasena, tipo):
        # verificar si ya existe el usuario
        for u in self.usuarios:
            if u['matricula'] == matricula:
                return False, "La matricula ya esta registrada"
        nuevo = Usuario(matricula, nombre, correo, contrasena, tipo)
        self.usuarios.append(nuevo.to_dict())
        self.guardar_datos()
        return True, "Usuario registrado correctamente"

    def buscar_libros(self, termino):
        resultados = []
        termino = termino.lower()
        for libro in self.libros:
            if termino in libro['titulo'].lower() or termino in libro['autor'].lower():
                resultados.append(libro)
        return resultados

    def prestar_libro(self, id_libro, matricula_usuario):
        for libro in self.libros:
            if libro['id_libro'] == id_libro:
                if not libro['disponibilidad']:
                    return False, "El libro no esta disponible"
                libro['disponibilidad'] = False
                id_prestamo = f"P{len(self.prestamos)+1:03d}"
                prestamo = {
                    'id_prestamo': id_prestamo,
                    'id_usuario': matricula_usuario,
                    'id_libro': id_libro,
                    'fecha_prestamo': datetime.now().strftime("%d/%m/%Y"),
                    'estado': "prestado"
                }
                self.prestamos.append(prestamo)
                self.guardar_datos()
                return True, "Prestamo realizado correctamente"
        return False, "Libro no encontrado"

    def devolver_libro(self, id_prestamo):
        for p in self.prestamos:
            if p['id_prestamo'] == id_prestamo and p['estado'] == "prestado":
                p['estado'] = "devuelto"
                # actualizar disponibilidad del libro
                for libro in self.libros:
                    if libro['id_libro'] == p['id_libro']:
                        libro['disponibilidad'] = True
                self.guardar_datos()
                return True, "Devolucion registrada"
        return False, "Prestamo no encontrado"

    def reservar_espacio(self, id_espacio, matricula, fecha, hora):
        for espacio in self.espacios:
            if espacio['id_espacio'] == id_espacio:
                if not espacio['disponibilidad']:
                    return False, "El espacio no esta disponible"
                # verificar que no haya reserva en esa fecha/hora (esto tiene un bug: no verifica bien)
                for r in self.reservas:
                    if r['id_espacio'] == id_espacio and r['fecha'] == fecha:
                        if r['hora'] == hora and r['estado'] == "activa":
                            return False, "Ya existe una reserva en esa hora"
                espacio['disponibilidad'] = False
                id_reserva = f"R{len(self.reservas)+1:03d}"
                reserva = {
                    'id_reserva': id_reserva,
                    'id_usuario': matricula,
                    'id_espacio': id_espacio,
                    'fecha': fecha,
                    'hora': hora,
                    'estado': "activa"
                }
                self.reservas.append(reserva)
                self.guardar_datos()
                return True, f"Reserva {id_reserva} creada"
        return False, "Espacio no encontrado"

    def cancelar_reserva(self, id_reserva):
        for r in self.reservas:
            if r['id_reserva'] == id_reserva:
                r['estado'] = "cancelada"
                # liberar espacio
                for espacio in self.espacios:
                    if espacio['id_espacio'] == r['id_espacio']:
                        espacio['disponibilidad'] = True
                self.guardar_datos()
                return True, "Reserva cancelada"
        return False, "Reserva no encontrada"

    def generar_reporte_libros(self):
        total = len(self.libros)
        disponibles = sum(1 for l in self.libros if l['disponibilidad'])
        prestados = total - disponibles
        return {"total": total, "disponibles": disponibles, "prestados": prestados}

    def generar_reporte_espacios(self):
        cubiculos = [e for e in self.espacios if e['tipo'] == 'cubiculo']
        talleres = [e for e in self.espacios if e['tipo'] == 'taller']
        videojuegos = [e for e in self.espacios if e['tipo'] == 'videojuegos']
        return {
            "cubiculos": {"total": len(cubiculos), "disponibles": sum(1 for e in cubiculos if e['disponibilidad'])},
            "talleres": {"total": len(talleres), "disponibles": sum(1 for e in talleres if e['disponibilidad'])},
            "videojuegos": {"total": len(videojuegos), "disponibles": sum(1 for e in videojuegos if e['disponibilidad'])}
        }

    def get_prestamos_usuario(self, matricula):
        return [p for p in self.prestamos if p['id_usuario'] == matricula]

    def get_reservas_usuario(self, matricula):
        return [r for r in self.reservas if r['id_usuario'] == matricula]
