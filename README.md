# Sistema-de-gestion-de-la-biblioteca-universitaria-BUAP
##  Descripción
Sistema de escritorio desarrollado en Python con interfaz gráfica (Tkinter) para gestionar los servicios de la Biblioteca Universitaria de la BUAP. Permite administrar usuarios, libros, cubículos, talleres, salas de videojuegos y generar reportes del sistema.

## Tecnologías Utilizadas

- **Lenguaje:** Python 
- **GUI:** Tkinter (incluido en Python)
- **Base de datos:** JSON (archivos locales)
- **Gráficas:** Matplotlib
- **Códigos QR:** qrcode + Pillow
- **IDE:** Visual Studio Code

##  Estructura del Proyecto

```
biblioteca_buap/
│
├── main.py                    # Punto de entrada del programa
├── requirements.txt           # Dependencias
├── README.md
│
├── clases/
│   ├── __init__.py
│   ├── modelos.py             # Clases: Usuario, Libro, Espacio, Reserva, Prestamo
│   └── sistema.py             # Clase Sistema (lógica principal)
│
├── interfaces/
│   ├── __init__.py
│   ├── ventana_login.py       # Pantalla de inicio de sesión
│   ├── ventana_registro.py    # Registro de nuevos usuarios
│   ├── ventana_qr.py          # Acceso mediante QR
│   ├── ventana_visitante.py   # Registro manual de visitantes
│   ├── ventana_menu.py        # Menú principal con sidebar
│   ├── ventana_libros.py      # Consulta y búsqueda de libros
│   ├── ventana_agregar_libro.py # Agregar libros (admin)
│   ├── ventana_devolucion.py  # Devolución de libros
│   ├── ventana_espacios.py    # Reservar cubículos/talleres/videojuegos
│   ├── ventana_prestamos.py   # Historial de préstamos del usuario
│   ├── ventana_mis_reservas.py # Mis reservas activas
│   ├── ventana_reportes.py    # Reportes con gráficas
│   ├── ventana_perfil.py      # Editar perfil personal
│   ├── ventana_ver_qr.py      # Ver/generar código QR personal
│   └── ventana_admin.py       # Panel de administración
│
└── datos/                     # Carpeta generada automáticamente
    ├── usuarios.json
    ├── libros.json
    ├── espacios.json
    ├── reservas.json
    └── prestamos.json
```

##  Instalación y Ejecución

1. el repositorio:
```bash
https://github.com/dianahdeztorres13-pixel/Sistema-de-gestion-de-la-biblioteca-universitaria-BUAP/edit/main/README.md
```

2. Instala las dependencias:
```bash
pip install qrcode Pillow matplotlib pandas
```

3. Ejecuta el programa:
```bash
python main.py
```

## Credenciales de prueba (Admin)

- **Matrícula:** `admin`
- **Contraseña:** `admin123`

##  Funcionalidades

| Módulo | Descripción |
|--------|-------------|
|  Login | Inicio de sesión con matrícula/contraseña o QR |
|  QR | Acceso rápido escaneando código QR personal |
|  Registro | Alta de nuevos usuarios (estudiantes, docentes, visitantes) |
|  Libros | Búsqueda, préstamo y devolución de material bibliográfico |
|  Cubículos | Reservación de espacios de estudio |
|  Talleres | Gestión de espacios para actividades académicas |
|  Videojuegos | Reservación de salas recreativas |
|  Reportes | Estadísticas con gráficas de uso del sistema |
| Perfil | Edición de datos personales y generación de QR |
| Admin | Panel de administración completo |

##  Principios POO Aplicados

- **Encapsulación:** Atributos privados y métodos de acceso en cada clase
- **Herencia:** Las ventanas heredan de `tk.Toplevel` y `tk.Tk`
- **Polimorfismo:** Método `to_dict()` y `from_dict()` implementado en todas las clases del modelo
- **Abstracción:** La clase `Sistema` coordina todas las operaciones ocultando la complejidad

## Video de Exposición

[Enlace al video - pendiente de subir]

## Limitaciones conocidas

- El sistema funciona solo de forma local (sin acceso en red)
- La lectura de QR es simulada mediante entrada de texto
- No integrado con sistemas institucionales de la BUAP
