# Guardian

**Guardián** es una aplicación de monitoreo de red local desarrollada en **Python** con **FastAPI**.  
Permite detectar dispositivos conectados a una red, generar alertas por intrusiones y gestionar una lista blanca (whitelist) de equipos autorizados.  
Incluye una interfaz web con inicio de sesión, panel de control y manejo visual de alertas.

---

Requisitos previos

Asegurate de tener instalado:

- **Python 3.10+**
- **pip** (instalador de paquetes)
- **nmap** (herramienta de escaneo de red)
- **Git** (opcional, para clonar el repositorio)

Instalar Nmap (si no lo tenés)

En Linux (Debian/Ubuntu):
```bash
sudo apt install nmap

En Windows:
Descargá desde https://nmap.org/download.html


y agregá la ruta de instalación de Nmap al PATH del sistema.
Instalación del entorno de desarrollo

    Clonar el proyecto o copiar la carpeta

git clone https://github.com/usuario/guardian.git
cd Guardian

Crear un entorno virtual

python3 -m venv venv

Activar el entorno virtual

    En Linux / Mac:

source venv/bin/activate

En Windows:

    venv\Scripts\activate

Instalar dependencias

    pip install -r requirements.txt

Archivo de configuración .env

En la raíz del proyecto, creá un archivo llamado .env con las siguientes variables:

# Credenciales de acceso al dashboard
(Personalizar usuario y contraseña a tu gusto.)

GUARDIAN_USER=admin
GUARDIAN_PASS=admin123


Estructura del proyecto

Guardian/
├── db/
│   ├── alerts.py
│   ├── devices.py
│   ├── whitelist.py
│   └── database.py
├── routers/
│   ├── scan.py
│   ├── alerts.py
│   └── whitelist.py
├── static/
│   ├── js/
│   │   └── dashboard.js
│   └── icons/
├── templates/
│   ├── index.html
│   └── login.html
├── main.py
├── .env
├── requirements.txt
└── README.md

Ejecución del sistema

    Asegurate de estar en el entorno virtual ((venv)).

    Ejecutá el servidor con:

uvicorn main:app --reload

O si tenés configurado el alias:

guardian_run

    Abrí el navegador y accedé a:

http://127.0.0.1:8000

    Iniciá sesión con las credenciales definidas en el .env.

Uso del sistema

Desde el Dashboard podrás:
Función	Descripción
🟢 Escanear Red	Detecta todos los dispositivos conectados en el rango ingresado.
🟠 Ver Alertas	Muestra los equipos no autorizados detectados.
🔴 Limpiar Alertas	Elimina todas las alertas registradas.
🔵 Ver Whitelist	Lista los dispositivos autorizados.
⚪ Agregar a Whitelist	Permite autorizar una IP específica.
🚪 Cerrar Sesión	Finaliza la sesión actual y vuelve al login.
💾 Base de datos

El sistema usa SQLite (guardian.db) que se genera automáticamente en la raíz del proyecto.
Contiene tres tablas:

    devices: dispositivos detectados

    alerts: alertas por intrusión

    whitelist: dispositivos autorizados

Podés eliminar el archivo guardian.db para resetear completamente los datos.
Tecnologías utilizadas

    Python 3.12

    FastAPI

    SQLite3

    Bootstrap 5

    Nmap

    HTML / JS / CSS

Notas finales
    El sistema fue probado en Linux (Ubuntu) y es compatible con Windows.
    Para un uso real, se recomienda ejecutar el programa con permisos de red suficientes para que Nmap pueda detectar todos los dispositivos.
    Ideal para proyectos académicos de seguridad, redes o programación web con Python.
