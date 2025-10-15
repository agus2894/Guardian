#!/bin/bash
# Guardian Security System - Script de Ejecución Rápida
# Para el profesor: ejecutar este script para iniciar Guardian

echo "🛡️  Guardian Security System"
echo "=============================="
echo ""

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "⚡ Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias si no están
echo "📦 Verificando dependencias..."
pip install -r requirements.txt --quiet

echo ""
echo "🚀 Iniciando Guardian Security System..."
echo "💡 Acceso: http://localhost:8000"
echo "👤 Usuario: admin | Contraseña: admin"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo "=============================="

# Ejecutar Guardian
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload