from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from utils.auth import get_current_user
import sqlite3
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import io
from typing import Optional

router = APIRouter(prefix="/reports", tags=["Reportes"])

def create_pdf_header(canvas, doc):
    """Crear encabezado personalizado para el PDF"""
    canvas.saveState()
    
    # Logo/Título en el encabezado
    canvas.setFont('Helvetica-Bold', 16)
    canvas.setFillColor(colors.HexColor('#1e3a8a'))
    canvas.drawString(50, 750, "Guardian - Sistema de Monitoreo de Red")
    
    # Línea separadora
    canvas.setStrokeColor(colors.HexColor('#3b82f6'))
    canvas.setLineWidth(2)
    canvas.line(50, 740, 550, 740)
    
    # Fecha de generación
    canvas.setFont('Helvetica', 10)
    canvas.setFillColor(colors.black)
    canvas.drawRightString(550, 750, f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    canvas.restoreState()

def create_pdf_footer(canvas, doc):
    """Crear pie de página"""
    canvas.saveState()
    
    # Línea separadora
    canvas.setStrokeColor(colors.HexColor('#e5e7eb'))
    canvas.setLineWidth(1)
    canvas.line(50, 50, 550, 50)
    
    # Información del pie
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(colors.HexColor('#6b7280'))
    canvas.drawString(50, 35, "Guardian Security Report - Confidencial")
    canvas.drawRightString(550, 35, f"Página {doc.page}")
    
    canvas.restoreState()

@router.get("/security-report")
async def generate_security_report(
    hours: int = 24,
    current_user: str = Depends(get_current_user)
):
    """Generar reporte de seguridad completo"""
    try:
        # Buffer para el PDF
        buffer = io.BytesIO()
        
        # Crear documento PDF
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=100,
            bottomMargin=80
        )
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#1e3a8a'),
            alignment=TA_CENTER
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.HexColor('#3b82f6'),
            borderWidth=1,
            borderColor=colors.HexColor('#e5e7eb'),
            borderPadding=8,
            backColor=colors.HexColor('#f8fafc')
        )
        
        # Contenido del documento
        story = []
        
        # Título principal
        story.append(Paragraph("📊 Reporte de Seguridad de Red", title_style))
        story.append(Spacer(1, 20))
        
        # Información del reporte
        info_data = [
            ['Período del Reporte:', f'Últimas {hours} horas'],
            ['Generado por:', current_user],
            ['Fecha:', datetime.now().strftime('%d de %B de %Y')],
            ['Hora:', datetime.now().strftime('%H:%M:%S')]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 30))
        
        # Obtener datos de la base de datos
        conn = sqlite3.connect("guardian.db")
        cursor = conn.cursor()
        
        since_time = (datetime.now() - timedelta(hours=hours)).isoformat()
        
        # === RESUMEN EJECUTIVO ===
        story.append(Paragraph("🎯 Resumen Ejecutivo", subtitle_style))
        
        # Estadísticas generales
        cursor.execute('''
            SELECT 
                COUNT(DISTINCT ip) as total_devices,
                COUNT(DISTINCT CASE WHEN w.id IS NOT NULL THEN d.ip END) as authorized_devices,
                COUNT(DISTINCT CASE WHEN w.id IS NULL THEN d.ip END) as unauthorized_devices
            FROM devices d
            LEFT JOIN whitelist w ON (d.ip = w.ip OR d.mac = w.mac)
            WHERE d.last_seen > ?
        ''', (since_time,))
        
        stats = cursor.fetchone()
        total_devices, authorized_devices, unauthorized_devices = stats
        
        # Alertas
        cursor.execute('''
            SELECT COUNT(*) FROM alerts 
            WHERE timestamp > ?
        ''', (since_time,))
        
        total_alerts = cursor.fetchone()[0]
        
        # Crear tabla de resumen
        summary_data = [
            ['📊 MÉTRICA', '📈 VALOR', '⚠️ ESTADO'],
            ['Dispositivos Detectados', str(total_devices), '✅ Normal' if total_devices < 20 else '⚠️ Alto'],
            ['Dispositivos Autorizados', str(authorized_devices), '✅ Bien'],
            ['Dispositivos No Autorizados', str(unauthorized_devices), '✅ Seguro' if unauthorized_devices == 0 else '🚨 ATENCIÓN'],
            ['Alertas Generadas', str(total_alerts), '✅ Normal' if total_alerts < 5 else '⚠️ Revisar']
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # === DISPOSITIVOS DETECTADOS ===
        story.append(Paragraph("💻 Dispositivos Detectados", subtitle_style))
        
        cursor.execute('''
            SELECT 
                d.ip,
                d.mac,
                d.last_seen,
                CASE WHEN w.id IS NOT NULL THEN 'SÍ' ELSE 'NO' END as authorized,
                w.name as whitelist_name
            FROM devices d
            LEFT JOIN whitelist w ON (d.ip = w.ip OR d.mac = w.mac)
            WHERE d.last_seen > ?
            ORDER BY d.last_seen DESC
            LIMIT 20
        ''', (since_time,))
        
        devices = cursor.fetchall()
        
        if devices:
            device_data = [['IP Address', 'MAC Address', 'Última Conexión', 'Autorizado', 'Nombre']]
            
            for device in devices:
                ip, mac, last_seen, authorized, name = device
                last_seen_formatted = datetime.fromisoformat(last_seen).strftime('%d/%m %H:%M')
                device_data.append([
                    ip,
                    mac or 'No disponible',
                    last_seen_formatted,
                    authorized,
                    name or '-'
                ])
            
            device_table = Table(device_data, colWidths=[1.2*inch, 1.5*inch, 1*inch, 0.8*inch, 1*inch])
            device_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            
            # Colorear filas según autorización
            for i, device in enumerate(devices, 1):
                if device[3] == 'NO':  # No autorizado
                    device_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, i), (-1, i), colors.HexColor('#fef2f2')),
                        ('TEXTCOLOR', (3, i), (3, i), colors.HexColor('#dc2626')),
                    ]))
                else:
                    device_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, i), (-1, i), colors.HexColor('#f0fdf4')),
                        ('TEXTCOLOR', (3, i), (3, i), colors.HexColor('#16a34a')),
                    ]))
            
            story.append(device_table)
        else:
            story.append(Paragraph("No se detectaron dispositivos en el período especificado.", styles['Normal']))
        
        story.append(PageBreak())
        
        # === ALERTAS DE SEGURIDAD ===
        story.append(Paragraph("🚨 Alertas de Seguridad", subtitle_style))
        
        cursor.execute('''
            SELECT id, type, timestamp, description 
            FROM alerts 
            WHERE timestamp > ?
            ORDER BY timestamp DESC
            LIMIT 15
        ''', (since_time,))
        
        alerts = cursor.fetchall()
        
        if alerts:
            alert_data = [['ID', 'Tipo', 'Fecha/Hora', 'Descripción']]
            
            for alert in alerts:
                alert_id, alert_type, timestamp, description = alert
                timestamp_formatted = datetime.fromisoformat(timestamp).strftime('%d/%m %H:%M:%S')
                alert_data.append([
                    str(alert_id),
                    alert_type,
                    timestamp_formatted,
                    description[:50] + '...' if len(description) > 50 else description
                ])
            
            alert_table = Table(alert_data, colWidths=[0.5*inch, 1*inch, 1.2*inch, 3*inch])
            alert_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc2626')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fef2f2')),
            ]))
            
            story.append(alert_table)
        else:
            story.append(Paragraph("✅ No se generaron alertas de seguridad en el período especificado.", styles['Normal']))
        
        conn.close()
        
        # Agregar línea final
        story.append(Spacer(1, 30))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#e5e7eb')))
        story.append(Spacer(1, 10))
        story.append(Paragraph(
            "Este reporte fue generado automáticamente por Guardian Security System.",
            ParagraphStyle('Footer', fontSize=8, textColor=colors.HexColor('#6b7280'), alignment=TA_CENTER)
        ))
        
        # Construir PDF
        doc.build(story, onFirstPage=create_pdf_header, onLaterPages=create_pdf_header)
        
        # Obtener el PDF del buffer
        buffer.seek(0)
        pdf_data = buffer.getvalue()
        buffer.close()
        
        # Generar nombre de archivo
        filename = f"guardian_security_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        return Response(
            content=pdf_data,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando reporte: {str(e)}")

@router.get("/network-report")
async def generate_network_report(current_user: str = Depends(get_current_user)):
    """Generar reporte de estado de red"""
    try:
        # Similar structure but focused on network topology and authorized devices
        # Implementation would be similar to security_report but with different data focus
        pass
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando reporte de red: {str(e)}")