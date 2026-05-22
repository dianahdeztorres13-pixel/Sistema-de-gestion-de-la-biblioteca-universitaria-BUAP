import json
import os
import qrcode
from datetime import datetime

# Clase base Usuario
class Usuario:
    def __init__(self, matricula, nombre, correo, contrasena, tipo):
        self.matricula = matricula
        self.nombre = nombre
        self.correo = correo
        self.contrasena = contrasena
        self.tipo = tipo  # estudiante, docente, visitante
        self.codigoQR = None

    def registrar(self, lista_usuarios):
        # verificar si ya existe
        for u in lista_usuarios:
            if u['matricula'] == self.matricula:
                return False
        lista_usuarios.append(self.to_dict())
        return True

    def generarQR(self):
        try:
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(self.matricula)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            path = f"datos/qr_{self.matricula}.png"
            img.save(path)
            self.codigoQR = path
            return path
        except Exception as e:
            print(f"Error generando QR: {e}")
            return None

    def iniciarSesionQR(self, matricula_escaneada):
        return self.matricula == matricula_escaneada

    def editarPerfil(self, nuevo_nombre=None, nuevo_correo=None):
        if nuevo_nombre:
            self.nombre = nuevo_nombre
        if nuevo_correo:
            self.correo = nuevo_correo

    def eliminarCuenta(self, lista_usuarios):
        for i, u in enumerate(lista_usuarios):
            if u['matricula'] == self.matricula:
                lista_usuarios.pop(i)
                return True
        return False

    def to_dict(self):
        return {
            'matricula': self.matricula,
            'nombre': self.nombre,
            'correo': self.correo,
            'contrasena': self.contrasena,
            'tipo': self.tipo,
            'codigoQR': self.codigoQR
        }

    @staticmethod
    def from_dict(d):
        u = Usuario(d['matricula'], d['nombre'], d['correo'], d['contrasena'], d['tipo'])
        u.codigoQR = d.get('codigoQR')
        return u


class Libro:
    def __init__(self, id_libro, titulo, autor, categoria, disponibilidad=True):
        self.id_libro = id_libro
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.disponibilidad = disponibilidad

    def registrar_libro(self, lista_libros):
        lista_libros.append(self.to_dict())

    def prestar_libro(self):
        if self.disponibilidad:
            self.disponibilidad = False
            return True
        return False  # ya prestado

    def devolver_libro(self):
        self.disponibilidad = True

    def to_dict(self):
        return {
            'id_libro': self.id_libro,
            'titulo': self.titulo,
            'autor': self.autor,
            'categoria': self.categoria,
            'disponibilidad': self.disponibilidad
        }

    @staticmethod
    def from_dict(d):
        return Libro(d['id_libro'], d['titulo'], d['autor'], d['categoria'], d['disponibilidad'])


class Espacio:
    def __init__(self, id_espacio, tipo, capacidad, disponibilidad=True):
        self.id_espacio = id_espacio
        self.tipo = tipo  # cubiculo, taller, videojuegos
        self.capacidad = capacidad
        self.disponibilidad = disponibilidad

    def reservar(self):
        if self.disponibilidad:
            self.disponibilidad = False
            return True
        return False

    def cancelar_reserva(self):
        self.disponibilidad = True

    def consultar_disponibilidad(self):
        return self.disponibilidad

    def to_dict(self):
        return {
            'id_espacio': self.id_espacio,
            'tipo': self.tipo,
            'capacidad': self.capacidad,
            'disponibilidad': self.disponibilidad
        }

    @staticmethod
    def from_dict(d):
        return Espacio(d['id_espacio'], d['tipo'], d['capacidad'], d['disponibilidad'])


class Reserva:
    def __init__(self, id_reserva, id_usuario, id_espacio, fecha, hora, estado="activa"):
        self.id_reserva = id_reserva
        self.id_usuario = id_usuario
        self.id_espacio = id_espacio
        self.fecha = fecha
        self.hora = hora
        self.estado = estado

    def crear_reserva(self, lista_reservas):
        lista_reservas.append(self.to_dict())

    def cancelar_reserva(self, lista_reservas):
        for r in lista_reservas:
            if r['id_reserva'] == self.id_reserva:
                r['estado'] = "cancelada"
                self.estado = "cancelada"
                return True
        return False

    def to_dict(self):
        return {
            'id_reserva': self.id_reserva,
            'id_usuario': self.id_usuario,
            'id_espacio': self.id_espacio,
            'fecha': self.fecha,
            'hora': self.hora,
            'estado': self.estado
        }

    @staticmethod
    def from_dict(d):
        return Reserva(d['id_reserva'], d['id_usuario'], d['id_espacio'],
                       d['fecha'], d['hora'], d['estado'])


class Prestamo:
    def __init__(self, id_prestamo, id_usuario, id_libro, fecha_prestamo, estado="prestado"):
        self.id_prestamo = id_prestamo
        self.id_usuario = id_usuario
        self.id_libro = id_libro
        self.fecha_prestamo = fecha_prestamo
        self.estado = estado

    def registrar_prestamo(self, lista_prestamos):
        lista_prestamos.append(self.to_dict())

    def devolver_libro(self, lista_prestamos):
        for p in lista_prestamos:
            if p['id_prestamo'] == self.id_prestamo:
                p['estado'] = "devuelto"
                self.estado = "devuelto"
                return True
        return False

    def to_dict(self):
        return {
            'id_prestamo': self.id_prestamo,
            'id_usuario': self.id_usuario,
            'id_libro': self.id_libro,
            'fecha_prestamo': self.fecha_prestamo,
            'estado': self.estado
        }

    @staticmethod
    def from_dict(d):
        return Prestamo(d['id_prestamo'], d['id_usuario'], d['id_libro'],
                        d['fecha_prestamo'], d['estado'])
