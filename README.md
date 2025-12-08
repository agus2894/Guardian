Guardian Security System

Sistema web de ciberseguridad para monitoreo de red, detección de dispositivos, generación de alertas y administración de una whitelist.
Diseñado para ofrecer visibilidad, control y protección en entornos domésticos o de pequeña empresa, con un enfoque en simplicidad, velocidad y análisis en tiempo real.

✨ Características Principales
🌐 Monitoreo y Escaneo de Red

Detección automática de dispositivos conectados
Obtención de IP, MAC y fabricante
Escaneos frecuentes mediante nmap
Registro completo del historial de actividad


🚨 Sistema de Alertas Inteligente

Notificación inmediata ante dispositivos no autorizados
Registro persistente en la base de datos
Regeneración automática para asegurar trazabilidad
Panel dedicado de alertas activas y resueltas

🔐 Autenticación y Seguridad

Login seguro con JWT
Hash de contraseñas mediante bcrypt
Sesiones protegidas
Rutas y funcionalidades restringidas por rol

📊 Dashboard Web en Tiempo Real

Vista general del estado de seguridad
Lista detallada de dispositivos conectados
Indicadores clave de actividad
Historial de escaneos
Estado de la whitelist

📄 Reportes Automáticos en PDF

Generación de reportes con los dispositivos detectados
Alertas generadas en el día
Actividad total de la red
Exportación lista para auditoría o respaldo

⚙️ Gestión de Whitelist

Registro de dispositivos autorizados
Control mediante dirección MAC
Comparación automática contra dispositivos detectados
Edición, agregado y eliminación desde el dashboard

🚀 Instalación
1. Instalar dependencias del sistema
sudo apt install nmap
# o equivalente según el sistema operativo

2. Preparar el entorno virtual
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3. Ejecutar la aplicación
# Opción recomendada
./run_guardian.sh

# O ejecución manual
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

4. Acceder al panel
URL: http://localhost:8000
Usuario: admin
Contraseña: admin

🏗️ Tecnologías Utilizadas

Backend: FastAPI
Frontend: HTML + Bootstrap 5
Base de datos: SQLite
Escaneo de red: nmap
Seguridad: JWT + bcrypt
Reportes: ReportLab (PDF)

📂 Estructura del Proyecto
Guardian/
├── main.py                 # Punto de entrada
├── db/                     # Modelos y base de datos
├── routers/                # Endpoints de la API
├── utils/                  # Scanner, auth y helpers
├── templates/              # HTML del dashboard
└── static/                 # CSS, JS y assets

🎯 Objetivo del Proyecto

Brindar una herramienta accesible y efectiva para mejorar la seguridad de redes locales mediante la detección temprana de dispositivos desconocidos, la centralización de alertas y la automatización de reportes.

🧑‍💻 Autor

Gonzalo Agustín Lamas
Técnico Universitario en Programación & Enfermero Profesional
