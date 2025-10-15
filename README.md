# Guardian Security System

Sistema de ciberseguridad para monitoreo de red y detección de dispositivos.

## 🚀 Ejecución Rápida

### Requisitos Previos
```bash
# Instalar nmap (necesario para escaneos de red)
sudo apt install nmap  # Ubuntu/Debian
# sudo yum install nmap  # CentOS/RHEL
# brew install nmap     # macOS
```

### Paso 1: Preparar el entorno
```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Paso 2: Ejecutar Guardian
```bash
# OPCIÓN A: Script automático (recomendado)
./run_guardian.sh

# OPCIÓN B: Manual
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Paso 3: Acceder al sistema
- **URL:** http://localhost:8000
- **Usuario:** admin
- **Contraseña:** admin

## ⚡ Funcionalidades

- 🔐 **Autenticación JWT** - Login seguro
- 🌐 **Escaneo de Red** - Detección automática con nmap
- 📊 **Dashboard** - Monitoreo en tiempo real
- 🚨 **Alertas** - Notificaciones de seguridad
- 📄 **Reportes PDF** - Generación automática
- ⚙️ **Whitelist** - Gestión de dispositivos autorizados

## 🏗️ Arquitectura

- **Backend:** FastAPI + SQLite
- **Frontend:** Bootstrap 5 + JavaScript  
- **Seguridad:** JWT + bcrypt
- **Red:** nmap para escaneo
- **Reportes:** ReportLab para PDF

## � Estructura

```
Guardian/
├── main.py              # Aplicación principal
├── .env                 # Configuración
├── requirements.txt     # Dependencias
├── guardian.db          # Base de datos
├── db/                  # Modelos de datos
├── routers/             # API endpoints
├── utils/               # Scanner y autenticación
├── templates/           # Frontend HTML
└── static/              # Assets
```