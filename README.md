# 🛡️ Guardian - Sistema de Monitoreo de Red y Ciberseguridad

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Security](https://img.shields.io/badge/Security-Network%20Monitoring-red.svg)](#)

> **Guardian** es un sistema profesional de monitoreo de red y detección de intrusiones diseñado para proporcionar visibilidad en tiempo real y alertas proactivas de seguridad en entornos de red corporativos y domésticos.

## 🎯 **Objetivo del Proyecto**

Guardian surge de la necesidad de tener una solución **simple, efectiva y autónoma** para:

- **Monitorear automáticamente** dispositivos en la red
- **Detectar intrusiones** y dispositivos no autorizados
- **Generar alertas** en tiempo real ante amenazas
- **Documentar incidentes** con reportes profesionales
- **Proporcionar visibilidad** completa del estado de la red

## 🏗️ **Arquitectura del Sistema**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   Bootstrap 5   │◄──►│   FastAPI       │◄──►│   SQLite        │
│   + JavaScript  │    │   + Python      │    │   + Context Mgr │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Notificaciones│    │   Scheduler     │    │   Logs          │
│   Push Browser  │    │   APScheduler   │    │   JSON Struct   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔄 **Flujo de Trabajo**

### **1. Inicialización del Sistema**
```
┌─ Inicio Guardian ─┐
├─ Inicializar BD ──┤
├─ Cargar Config ───┤
├─ Iniciar Scheduler┤
└─ Sistema Listo ───┘
```

### **2. Proceso de Monitoreo**
```
Escaneo Automático → Detectar Dispositivos → ¿Autorizado?
                                               │
                                 ┌─── Sí ────┴─── Registrar
                                 │
                                 └─── No ─── Generar Alerta
                                             │
                                             ├─ Notificación Push
                                             ├─ Log de Seguridad
                                             └─ Actualizar Dashboard
```

### **3. Gestión de Incidentes**
```
Alerta → Clasificación → Notificación → Logs → Análisis → Reporte PDF
```

## ⚡ **Características Principales**

### 🔒 **Seguridad y Monitoreo**
- **Detección de intrusiones** en tiempo real
- **Escaneo automático** de red programable
- **Whitelist inteligente** de dispositivos autorizados
- **Alertas proactivas** ante dispositivos no autorizados
- **Correlación de eventos** de seguridad

### 📊 **Dashboard y Reportes**
- **Interfaz intuitiva** con modo oscuro/claro
- **Métricas en tiempo real** de la red
- **Visualización de dispositivos** con detalles MAC
- **Exportación PDF** profesional de reportes
- **Historial completo** de eventos

### 🔔 **Notificaciones Inteligentes**
- **Push notifications** del navegador
- **Alertas por email** (configurable)
- **Clasificación automática** por severidad
- **Persistencia de configuración** por usuario

### 🛠️ **Administración**
- **Autenticación segura** con JWT
- **Gestión de whitelist** desde interfaz web
- **Programación flexible** de escaneos
- **Logs estructurados** en JSON para análisis

## 🚀 **Instalación y Configuración**

### **Prerrequisitos**
```bash
- Python 3.12+
- pip (gestor de paquetes)
- Red accesible para escaneo
```

### **1. Clonar el Repositorio**
```bash
git clone https://github.com/tu-usuario/guardian.git
cd guardian
```

### **2. Crear Entorno Virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### **3. Instalar Dependencias**
```bash
pip install -r requirements.txt
```

### **4. Configurar Variables de Entorno**
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

**Configuración mínima en `.env`:**
```env
# Autenticación
GUARDIAN_USER=admin
GUARDIAN_PASS=tu_password_segura
SECRET_KEY=tu_clave_secreta_jwt

# Red
DEFAULT_NETWORK_RANGE=192.168.0.0/24

# Email (opcional)
EMAIL_NOTIFICATIONS=false
SMTP_SERVER=smtp.gmail.com
SMTP_USERNAME=tu_email@gmail.com
SMTP_PASSWORD=tu_app_password
```

### **5. Iniciar Guardian**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### **6. Acceder al Dashboard**
```
http://localhost:8000
```

## 📋 **Uso del Sistema**

### **Dashboard Principal**
1. **Login** con credenciales configuradas
2. **Configurar escaneos** automáticos
3. **Monitorear dispositivos** en tiempo real
4. **Gestionar whitelist** de dispositivos autorizados
5. **Revisar alertas** y eventos de seguridad

### **Escaneos de Red**
- **Automático:** Configurable cada X minutos
- **Manual:** Botón "Escanear Ahora"
- **Programado:** Scheduler con intervalos personalizables

### **Gestión de Alertas**
- **Visualización** en tiempo real
- **Filtrado** por tipo y severidad
- **Exportación** a PDF para auditorías
- **Limpieza** manual del historial

## 🛡️ **Casos de Uso en Ciberseguridad**

### **1. Monitoreo de Red Corporativa**
- Detectar dispositivos no autorizados (BYOD no aprobados)
- Identificar posibles intrusiones
- Mantener inventario actualizado de activos de red

### **2. Seguridad Doméstica**
- Monitorear dispositivos IoT
- Detectar accesos no autorizados a WiFi
- Alertas ante nuevos dispositivos

### **3. Cumplimiento y Auditorías**
- Documentación automática de eventos
- Reportes profesionales para compliance
- Logs estructurados para análisis forense

### **4. Incident Response**
- Detección temprana de amenazas
- Correlación de eventos de red
- Base de datos histórica para investigaciones

## 📁 **Estructura del Proyecto**

```
guardian/
├── 📁 db/                 # Gestión de base de datos
│   ├── alerts.py          # Manejo de alertas
│   ├── database.py        # Configuración y conexiones
│   ├── devices.py         # Gestión de dispositivos
│   └── whitelist.py       # Lista de dispositivos autorizados
├── 📁 routers/            # Endpoints de la API
│   ├── alerts.py          # API de alertas
│   ├── auth.py           # Autenticación
│   ├── devices.py        # API de dispositivos
│   ├── reports.py        # Generación de PDFs
│   ├── scan.py           # Escaneos de red
│   ├── scheduler.py      # Programación automática
│   └── whitelist.py      # Gestión de whitelist
├── 📁 static/            # Archivos estáticos
│   ├── js/dashboard.js   # Lógica del frontend
│   └── icons/           # Iconos y favicon
├── 📁 templates/         # Plantillas HTML
│   ├── index.html       # Dashboard principal
│   └── login.html       # Página de login
├── 📁 utils/            # Utilidades del sistema
│   ├── auth.py          # Autenticación JWT
│   ├── scanner.py       # Escaneo de red
│   ├── simple_logger.py # Sistema de logs
│   ├── simple_scheduler.py # Scheduler optimizado
│   └── mailer.py        # Notificaciones email
├── 📄 main.py           # Aplicación principal
├── 📄 requirements.txt  # Dependencias
└── 📄 README.md         # Esta documentación
```

## 🔧 **Tecnologías Utilizadas**

### **Backend**
- **FastAPI** - Framework web moderno y rápido
- **SQLite** - Base de datos ligera y confiable
- **APScheduler** - Programación de tareas
- **python-nmap** - Escaneo de red
- **ReportLab** - Generación de PDFs
- **JWT** - Autenticación segura

### **Frontend**
- **Bootstrap 5** - Framework CSS responsivo
- **JavaScript** - Interactividad y notificaciones
- **Jinja2** - Motor de plantillas
- **Font Awesome** - Iconos

### **Seguridad**
- **bcrypt** - Hash de contraseñas
- **CSRF Protection** - Protección contra ataques
- **Logs estructurados** - Trazabilidad completa

## 📊 **Métricas de Performance**

- **Tiempo de escaneo:** ~30-60 segundos (red estándar /24)
- **Uso de memoria:** <100MB en operación normal
- **Base de datos:** SQLite optimizada con context managers
- **Logs:** Rotación automática (5MB por archivo)

## 🔮 **Roadmap Futuro**

### **Próximas Funcionalidades**
- [ ] **API REST completa** con Swagger/OpenAPI
- [ ] **Integración con SIEM** externos
- [ ] **Análisis de vulnerabilidades** básico
- [ ] **Geolocalización de IPs** externas
- [ ] **Machine Learning** para detección de anomalías

### **Mejoras Técnicas**
- [ ] **Base de datos PostgreSQL** para entornos enterprise
- [ ] **Contenedorización** con Docker
- [ ] **CI/CD pipeline** automatizado
- [ ] **Tests unitarios** completos

## 🛡️ **Filosofía de Desarrollo**

**"Menos es más"** - Guardian se construye bajo el principio de simplicidad y efectividad:

- **Código limpio** sobre complejidad innecesaria
- **Funcionalidad esencial** sobre features redundantes  
- **Mantenibilidad** sobre optimización prematura
- **Seguridad** como prioridad desde el diseño

## 👨‍💻 **Contribución**

Guardian es un proyecto de **aprendizaje y demostración** en ciberseguridad. Las contribuciones son bienvenidas siguiendo estos principios:

1. **Fork** del proyecto
2. **Crear rama** para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. **Abrir Pull Request**

## 📄 **Licencia**

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🔗 **Contacto**

**Desarrollador:** Agustín Lamas
**GitHub:** [agus2894](https://github.com/agus2894)  
**Proyecto enfocado en:** Ciberseguridad y Network Security

---

## 🛡️ **Disclaimer de Seguridad**

Guardian está diseñado para uso en redes propias o con autorización explícita. El usuario es responsable del cumplimiento de todas las leyes y regulaciones aplicables relacionadas con el escaneo de redes y monitoreo de dispositivos.

**Uso ético:** Este software debe usarse únicamente para mejorar la seguridad de sistemas propios o bajo autorización explícita del propietario de la red.

---

*Guardian - Protegiendo tu red con inteligencia y simplicidad* 🛡️✨