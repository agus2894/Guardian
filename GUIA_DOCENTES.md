# 📚 GUARDIAN - GUÍA PARA DOCENTES

## 🎯 **PROPÓSITO EDUCATIVO**

Guardian es un proyecto académico diseñado para demostrar conceptos fundamentales de **ciberseguridad** aplicados en un entorno real. El sistema implementa técnicas de detección de intrusiones, monitoreo de red y respuesta a incidentes.

---

## 🔐 **CREDENCIALES DE DEMOSTRACIÓN**

**Para facilitar la evaluación académica:**

- **Usuario:** `admin`
- **Contraseña:** `admin`

> ⚠️ **NOTA IMPORTANTE:** Estas credenciales son exclusivamente para **demostración académica**. En un entorno de producción se utilizarían credenciales robustas y hashes seguros.

---

## 🛡️ **CONCEPTOS DE CIBERSEGURIDAD IMPLEMENTADOS**

### 1. **AUTENTICACIÓN Y AUTORIZACIÓN**
- **JWT (JSON Web Tokens):** Autenticación sin estado
- **bcrypt:** Hash seguro de contraseñas con salt automático
- **CSRF Protection:** Protección contra ataques Cross-Site Request Forgery
- **Gestión de sesiones:** Expiración automática de tokens (120 minutos)

### 2. **DETECCIÓN DE INTRUSIONES**
- **Escáner de red:** Uso de nmap para reconocimiento de dispositivos
- **Whitelist:** Lista de dispositivos autorizados
- **Alertas automáticas:** Notificación inmediata de dispositivos no autorizados
- **Correlación de eventos:** Análisis de patrones sospechosos

### 3. **LOGGING Y AUDITORÍA**
- **Logging estructurado:** Formato JSON para análisis automatizado
- **Trazabilidad completa:** Registro de todos los eventos de seguridad
- **Métricas de rendimiento:** Análisis de efectividad del sistema
- **Cumplimiento:** Registros apropiados para auditorías

### 4. **RESPUESTA A INCIDENTES**
- **Alertas en tiempo real:** Notificaciones push del navegador
- **Notificaciones por email:** Alertas críticas enviadas automáticamente
- **Reportes PDF:** Documentación formal de incidentes
- **Dashboard de monitoreo:** Visualización centralizada del estado de seguridad

---

## 🏗️ **ARQUITECTURA TÉCNICA**

### **Backend (Python/FastAPI)**
```
main.py              → Aplicación principal
├── routers/         → Módulos funcionales (API endpoints)
├── db/              → Gestión de base de datos SQLite
├── utils/           → Utilidades (auth, logging, scanner)
└── templates/       → Interfaz web HTML
```

### **Frontend (HTML/CSS/JavaScript)**
- **Bootstrap 5:** Framework responsive
- **JavaScript vanilla:** Sin dependencias externas
- **Service Workers:** Notificaciones push
- **Temas adaptativos:** Modo claro/oscuro

### **Base de Datos (SQLite)**
- **devices:** Inventario de dispositivos detectados
- **alerts:** Registro de eventos de seguridad
- **whitelist:** Dispositivos autorizados
- **metrics:** Métricas del sistema

---

## 🚀 **EJECUCIÓN DEL SISTEMA**

### **Prerequisitos:**
```bash
# Python 3.12+ y dependencias
pip install -r requirements.txt

# nmap para escáner de red
sudo apt install nmap  # Ubuntu/Debian
```

### **Iniciar el sistema:**
```bash
# Método 1: Con alias configurado
guardian_run

# Método 2: Manual
source venv/bin/activate
uvicorn main:app --reload
```

### **Acceso:**
- **URL:** http://localhost:8000
- **Login:** admin / admin

---

## 🔍 **FUNCIONALIDADES PARA EVALUAR**

### 1. **Sistema de Autenticación**
- Login seguro con JWT
- Protección de rutas administrativas
- Logout con invalidación de tokens

### 2. **Escáner de Red**
- Detección automática de dispositivos
- Escaneo manual bajo demanda
- Identificación de direcciones MAC

### 3. **Gestión de Alertas**
- Creación automática de alertas
- Visualización en dashboard
- Exportación de reportes

### 4. **Monitoreo en Tiempo Real**
- Dashboard actualizable
- Notificaciones push
- Métricas de seguridad

### 5. **Administración**
- Gestión de whitelist
- Programación de escaneos
- Configuración del sistema

---

## 📊 **MÉTRICAS Y REPORTES**

El sistema genera automáticamente:

- **Reportes de seguridad en PDF**
- **Logs estructurados en JSON**
- **Métricas de rendimiento**
- **Análisis de tendencias**

---

## 💡 **PUNTOS DE EVALUACIÓN SUGERIDOS**

### **Seguridad:**
- ✅ Implementación correcta de autenticación
- ✅ Gestión segura de credenciales
- ✅ Protección contra ataques comunes
- ✅ Logging adecuado para auditoría

### **Funcionalidad:**
- ✅ Detección efectiva de dispositivos
- ✅ Generación apropiada de alertas
- ✅ Interfaz intuitiva y profesional
- ✅ Reportes informativos y útiles

### **Código:**
- ✅ Arquitectura limpia y modular
- ✅ Comentarios explicativos apropiados
- ✅ Manejo de errores robusto
- ✅ Documentación completa

---

## 🔧 **CONFIGURACIÓN AVANZADA**

### **Variables de Entorno (.env):**
```env
# Autenticación
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin
SECRET_KEY=clave_secreta_unica

# Notificaciones (opcional)
EMAIL_NOTIFICATIONS=false
SMTP_HOST=smtp.gmail.com
EMAIL_FROM=guardian@ejemplo.com
EMAIL_TO=admin@ejemplo.com
```

### **Archivos de Configuración Importantes:**
- `.env` → Variables de entorno
- `requirements.txt` → Dependencias Python
- `guardian.db` → Base de datos SQLite
- `logs/` → Archivos de log del sistema

---

## 📱 **CASOS DE USO REALES**

### **Escenario 1: Detección de Dispositivo No Autorizado**
1. Un dispositivo desconocido se conecta a la red
2. Guardian lo detecta durante el escaneo automático
3. Se genera una alerta de intrusión
4. Se envía notificación push y email
5. El evento se registra en logs para auditoría

### **Escenario 2: Monitoreo Proactivo**
1. El administrador accede al dashboard
2. Revisa dispositivos detectados recientemente
3. Autoriza dispositivos legítimos en whitelist
4. Programa escaneos automáticos
5. Genera reporte de seguridad semanal

---

## 🎓 **VALOR ACADÉMICO**

Este proyecto demuestra:

- **Aplicación práctica** de conceptos teóricos de ciberseguridad
- **Integración** de múltiples tecnologías y frameworks
- **Desarrollo** de un sistema completo y funcional
- **Documentación** apropiada para un entorno profesional
- **Buenas prácticas** de desarrollo seguro

---

## 📞 **SOPORTE Y PREGUNTAS**

Para dudas técnicas o aclaraciones sobre la implementación, consultar:

- **Documentación completa:** `README.md`
- **Comentarios en código:** Incluidos en archivos principales
- **Logs del sistema:** Directorio `logs/`
- **Configuración:** Archivo `.env.example`

---

*Guardian v2.0 - Sistema Educativo de Ciberseguridad*
*Desarrollado como proyecto académico para demostrar conceptos de seguridad informática*