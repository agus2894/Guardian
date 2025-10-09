// static/js/dashboard.js

// Variables globales
let autoRefreshEnabled = false;
let autoRefreshInterval = null;
let refreshCountdown = 30;
let countdownInterval = null;
let currentDeviceView = 'basic'; // 'basic' o 'detailed'
let notificationsEnabled = false;
let lastKnownDevices = new Set();

// === FUNCIONES DE NOTIFICACIONES PUSH ===
async function requestNotificationPermission() {
    if (!("Notification" in window)) {
        showToast('Este navegador no soporta notificaciones', 'warning');
        updateNotificationUI();
        return false;
    }

    if (Notification.permission === "granted") {
        notificationsEnabled = true;
        localStorage.setItem('notificationsEnabled', 'true');
        showToast('Notificaciones ya están habilitadas', 'success');
        updateNotificationUI();
        return true;
    }

    if (Notification.permission !== "denied") {
        const permission = await Notification.requestPermission();
        if (permission === "granted") {
            notificationsEnabled = true;
            localStorage.setItem('notificationsEnabled', 'true');
            showToast('¡Notificaciones habilitadas! 🔔', 'success');
            
            // Mostrar notificación de bienvenida
            showNotification(
                'Guardian - Notificaciones Activas',
                'Recibirás alertas de seguridad en tiempo real',
                'info'
            );
            updateNotificationUI();
            return true;
        } else {
            showToast('Notificaciones denegadas', 'warning');
            updateNotificationUI();
            return false;
        }
    }
    
    showToast('Notificaciones bloqueadas. Habilítalas en configuración del navegador', 'warning');
    updateNotificationUI();
    return false;
}

function showNotification(title, message, type = 'info', data = {}) {
    if (!notificationsEnabled || Notification.permission !== "granted") {
        return;
    }

    const iconMap = {
        'info': '🛡️',
        'warning': '⚠️',
        'danger': '🚨',
        'success': '✅'
    };

    const icon = iconMap[type] || '🛡️';
    const fullTitle = `${icon} ${title}`;

    const notification = new Notification(fullTitle, {
        body: message,
        icon: '/static/icons/favicon-32x32.png',
        badge: '/static/icons/favicon-16x16.png',
        tag: `guardian-${type}-${Date.now()}`,
        requireInteraction: type === 'danger' || type === 'warning',
        data: data,
        actions: type === 'danger' ? [
            { action: 'view', title: 'Ver Dashboard' },
            { action: 'dismiss', title: 'Descartar' }
        ] : []
    });

    // Auto-cerrar notificaciones informativas después de 5 segundos
    if (type === 'info' || type === 'success') {
        setTimeout(() => {
            notification.close();
        }, 5000);
    }

    // Manejar clics en la notificación
    notification.onclick = function(event) {
        event.preventDefault();
        window.focus();
        this.close();
        
        // Scroll a la sección relevante si hay datos
        if (data.section) {
            const element = document.getElementById(data.section);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth' });
            }
        }
    };
}

function toggleNotifications() {
    const toggle = document.getElementById('notifications-toggle');
    
    if (toggle.checked) {
        requestNotificationPermission();
    } else {
        notificationsEnabled = false;
        localStorage.setItem('notificationsEnabled', 'false');
        showToast('Notificaciones deshabilitadas', 'info');
        updateNotificationUI();
    }
}

function initializeNotifications() {
    const saved = localStorage.getItem('notificationsEnabled');
    const toggle = document.getElementById('notifications-toggle');
    
    if (saved === 'true' && Notification.permission === "granted") {
        notificationsEnabled = true;
        if (toggle) toggle.checked = true;
    } else {
        notificationsEnabled = false;
        if (toggle) toggle.checked = false;
    }
    
    // Actualizar UI
    updateNotificationUI();
}

function updateNotificationUI() {
    const btn = document.getElementById('notification-btn');
    const text = document.getElementById('notification-text');
    const icon = btn?.querySelector('i');
    
    if (!btn) return;
    
    if (notificationsEnabled && Notification.permission === "granted") {
        btn.className = 'btn btn-success';
        if (text) text.textContent = 'Activas';
        if (icon) {
            icon.className = 'fas fa-bell btn-icon';
        }
        btn.title = 'Notificaciones activas';
    } else if (Notification.permission === "denied") {
        btn.className = 'btn btn-danger';
        if (text) text.textContent = 'Bloqueadas';
        if (icon) {
            icon.className = 'fas fa-bell-slash btn-icon';
        }
        btn.title = 'Notificaciones bloqueadas - Habilitar en configuración del navegador';
    } else {
        btn.className = 'btn btn-outline-warning';
        if (text) text.textContent = 'Inactivas';
        if (icon) {
            icon.className = 'fas fa-bell btn-icon';
        }
        btn.title = 'Activar notificaciones push';
    }
}

function checkForNewThreats(devices) {
    if (!notificationsEnabled) return;
    
    const currentDevices = new Set(devices.map(d => d.ip));
    const unauthorizedDevices = devices.filter(d => !d.authorized);
    
    // Detectar nuevos dispositivos no autorizados
    unauthorizedDevices.forEach(device => {
        if (!lastKnownDevices.has(device.ip)) {
            showNotification(
                'Dispositivo No Autorizado Detectado',
                `IP: ${device.ip} | MAC: ${device.mac || 'No disponible'}`,
                'danger',
                { section: 'devices-section', ip: device.ip }
            );
        }
    });
    
    // Actualizar lista conocida
    lastKnownDevices = currentDevices;
}

// === FUNCIONES DE TEMA ===
function toggleTheme() {
    const toggle = document.getElementById('theme-toggle');
    const currentTheme = document.documentElement.getAttribute('data-theme');
    
    if (toggle.checked) {
        // Cambiar a tema oscuro
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
        showToast('Tema oscuro activado', 'info');
    } else {
        // Cambiar a tema claro
        document.documentElement.removeAttribute('data-theme');
        localStorage.setItem('theme', 'light');
        showToast('Tema claro activado', 'info');
    }
}

function initializeTheme() {
    const savedTheme = localStorage.getItem('theme');
    const toggle = document.getElementById('theme-toggle');
    
    if (savedTheme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        if (toggle) toggle.checked = true;
    } else {
        document.documentElement.removeAttribute('data-theme');
        if (toggle) toggle.checked = false;
    }
}

// Inicialización cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tema antes que nada
    initializeTheme();
    
    // Inicializar notificaciones
    initializeNotifications();
    
    // Cargar datos iniciales
    getWhitelist();
    getAlerts();
    getSchedulerStatus();
    
    // Iniciar auto-refresh si está configurado
    const savedAutoRefresh = localStorage.getItem('autoRefresh');
    if (savedAutoRefresh === 'true') {
        toggleAutoRefresh();
    }
    
    // Actualizar estado del scheduler cada 30 segundos
    setInterval(getSchedulerStatus, 30000);
});

// Mostrar notificaciones toast
function showToast(message, type = 'info') {
    const toastContainer = document.querySelector('.toast-container');
    const toastId = 'toast-' + Date.now();
    
    const toastHtml = `
        <div class="toast align-items-center text-bg-${type}" role="alert" id="${toastId}">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas fa-${getIconForType(type)} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHtml);
    
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, { delay: 5000 });
    toast.show();
    
    // Remover del DOM después de que se oculte
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

function getIconForType(type) {
    const icons = {
        'success': 'check-circle',
        'danger': 'exclamation-triangle',
        'warning': 'exclamation-circle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

// Toggle auto-refresh
function toggleAutoRefresh() {
    autoRefreshEnabled = !autoRefreshEnabled;
    const button = document.getElementById('auto-refresh-text');
    
    if (autoRefreshEnabled) {
        button.textContent = 'Desactivar Auto-refresh';
        startAutoRefresh();
        localStorage.setItem('autoRefresh', 'true');
        showToast('Auto-refresh activado (30 segundos)', 'success');
    } else {
        button.textContent = 'Activar Auto-refresh';
        stopAutoRefresh();
        localStorage.setItem('autoRefresh', 'false');
        showToast('Auto-refresh desactivado', 'info');
    }
}

function startAutoRefresh() {
    refreshCountdown = 30;
    updateRefreshBadge();
    
    countdownInterval = setInterval(() => {
        refreshCountdown--;
        updateRefreshBadge();
        
        if (refreshCountdown <= 0) {
            refreshCountdown = 30;
            getScan(true); // Escaneo silencioso
        }
    }, 1000);
}

function stopAutoRefresh() {
    if (countdownInterval) {
        clearInterval(countdownInterval);
        countdownInterval = null;
    }
    document.getElementById('refresh-status').style.display = 'none';
}

function updateRefreshBadge() {
    const badge = document.getElementById('refresh-status');
    const countdown = document.getElementById('refresh-countdown');
    
    if (autoRefreshEnabled) {
        badge.style.display = 'inline-block';
        countdown.textContent = refreshCountdown;
    } else {
        badge.style.display = 'none';
    }
}

// Actualizar estadísticas
function updateStats(devices = [], alerts = [], whitelist = []) {
    document.getElementById('stats-devices').textContent = devices.length;
    document.getElementById('stats-alerts').textContent = alerts.length;
    document.getElementById('stats-whitelist').textContent = whitelist.length;
    
    const unauthorized = devices.filter(d => !d.authorized).length;
    document.getElementById('stats-unauthorized').textContent = unauthorized;
}

// Escanear red
function getScan(silent = false) {
    const range = document.getElementById("network_range").value || "192.168.0.0/24";
    const loadingIcon = document.getElementById("scan-loading");
    
    if (!silent) {
        loadingIcon.classList.add('show');
        showToast('Iniciando escaneo de red...', 'info');
    }
    
    fetch(`/scan/?network_range=${encodeURIComponent(range)}`)
        .then(res => {
            if (!res.ok) throw new Error('Error en el escaneo');
            return res.json();
        })
        .then(data => {
            const table = document.getElementById("devices");
            const tbody = table.querySelector('tbody');
            tbody.innerHTML = "";
            
            data.dispositivos_detectados.forEach(dev => {
                const statusClass = dev.authorized ? 'status-online' : 'status-unauthorized';
                const authText = dev.authorized ? 'Sí' : 'No';
                const authBadge = dev.authorized ? 'bg-success' : 'bg-danger';
                
                tbody.innerHTML += `
                    <tr>
                        <td><span class="status-indicator ${statusClass}"></span></td>
                        <td><code>${dev.ip}</code></td>
                        <td><code class="fw-bold">${dev.mac || 'No disponible'}</code></td>
                        <td><span class="badge ${authBadge}">${authText}</span></td>
                        <td>
                            ${!dev.authorized ? `
                                <button class="btn btn-sm btn-primary" onclick="quickAddToWhitelist('${dev.ip}', '${dev.mac || ''}')">
                                    <i class="fas fa-plus"></i> Autorizar
                                </button>
                            ` : ''}
                            <button class="btn btn-sm btn-info" onclick="copyToClipboard('${dev.mac || dev.ip}')" title="Copiar">
                                <i class="fas fa-copy"></i>
                            </button>
                        </td>
                    </tr>
                `;
            });
            
            // Actualizar estadísticas
            updateStats(data.dispositivos_detectados);
            
            // Verificar amenazas para notificaciones
            checkForNewThreats(data.dispositivos_detectados);
            
            if (!silent) {
                if (data.alertas_generadas.length > 0) {
                    showToast(`Escaneo completado. ${data.alertas_generadas.length} alertas generadas.`, 'warning');
                    getAlerts(); // Actualizar alertas
                    
                    // Notificación push para alertas críticas
                    if (notificationsEnabled && data.alertas_generadas.length > 0) {
                        showNotification(
                            'Alertas de Seguridad Generadas',
                            `Se detectaron ${data.alertas_generadas.length} nuevas alertas críticas`,
                            'warning',
                            { section: 'alerts-section' }
                        );
                    }
                } else {
                    showToast('Escaneo completado. No se detectaron dispositivos no autorizados.', 'success');
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            if (!silent) {
                showToast('Error al escanear la red', 'danger');
            }
        })
        .finally(() => {
            if (!silent) {
                loadingIcon.classList.remove('show');
            }
        });
}

// Agregar rápidamente a whitelist
function quickAddToWhitelist(ip, mac) {
    const name = prompt(`Ingrese un nombre para el dispositivo ${ip}:`);
    if (name) {
        const formData = new FormData();
        formData.append("nombre", name);
        formData.append("ip", ip);
        if (mac && mac !== 'N/A') {
            formData.append("mac", mac);
        }
        
        fetch("/whitelist/agregar", {
            method: "POST",
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            showToast(data.mensaje, 'success');
            getWhitelist();
            getScan(); // Actualizar escaneo
        })
        .catch(error => {
            showToast('Error al agregar dispositivo', 'danger');
        });
    }
}

// Obtener alertas
function getAlerts() {
    fetch("/alerts/")
        .then(res => res.json())
        .then(data => {
            const table = document.getElementById("alerts");
            const tbody = table.querySelector('tbody');
            tbody.innerHTML = "";
            
            if (data.length === 0) {
                tbody.innerHTML = '<tr><td colspan="4" class="text-center text-muted">No hay alertas</td></tr>';
            } else {
                data.forEach(alert => {
                    tbody.innerHTML += `
                        <tr>
                            <td>${alert.id}</td>
                            <td><span class="badge bg-warning">${alert.type}</span></td>
                            <td>${new Date(alert.timestamp).toLocaleString()}</td>
                            <td>${alert.description}</td>
                        </tr>
                    `;
                });
            }
            
            // Actualizar estadísticas
            updateStats([], data);
        });
}

// Limpiar alertas
function clearAlerts() {
    if (confirm('¿Está seguro de que desea eliminar todas las alertas?')) {
        fetch("/alerts/clear", { method: "DELETE" })
            .then(res => res.json())
            .then(data => {
                showToast(data.mensaje, 'success');
                getAlerts();
            })
            .catch(error => {
                showToast('Error al limpiar alertas', 'danger');
            });
    }
}

// Obtener whitelist
function getWhitelist() {
    fetch("/whitelist/")
        .then(res => res.json())
        .then(data => {
            const table = document.getElementById("whitelist");
            const tbody = table.querySelector('tbody');
            tbody.innerHTML = "";
            
            if (data.whitelist.length === 0) {
                tbody.innerHTML = '<tr><td colspan="3" class="text-center text-muted">No hay dispositivos autorizados</td></tr>';
            } else {
                data.whitelist.forEach(item => {
                    tbody.innerHTML += `
                        <tr>
                            <td>
                                <i class="fas fa-shield-alt text-success me-2"></i>
                                <strong>${item.name}</strong>
                            </td>
                            <td><code class="text-info">${item.ip}</code></td>
                            <td>
                                <div>
                                    <code class="fw-bold text-warning">${item.mac || 'No disponible'}</code>
                                    ${item.mac && item.mac !== 'No disponible' ? `
                                        <button class="btn btn-xs btn-outline-light ms-1" onclick="copyToClipboard('${item.mac}')" title="Copiar MAC">
                                            <i class="fas fa-copy fa-xs"></i>
                                        </button>
                                    ` : ''}
                                </div>
                            </td>
                        </tr>
                    `;
                });
            }
            
            // Actualizar estadísticas
            updateStats([], [], data.whitelist);
        });
}

// Agregar a whitelist (formulario)
function addToWhitelist() {
    const name = document.getElementById("device_name").value;
    const ip = document.getElementById("device_ip").value;
    const mac = document.getElementById("device_mac").value;

    const formData = new FormData();
    formData.append("nombre", name);
    formData.append("ip", ip);
    if (mac) {
        formData.append("mac", mac);
    }

    fetch("/whitelist/agregar", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        showToast(data.mensaje, 'success');
        getWhitelist();
        
        // Limpiar formulario
        document.getElementById("device_name").value = '';
        document.getElementById("device_ip").value = '';
        document.getElementById("device_mac").value = '';
    })
    .catch(error => {
        showToast('Error al agregar dispositivo', 'danger');
    });
}

// === FUNCIONES DEL SCHEDULER ===

// Obtener estado del scheduler
function getSchedulerStatus() {
    fetch("/scheduler/status")
        .then(res => res.json())
        .then(data => {
            updateSchedulerUI(data);
        })
        .catch(error => {
            console.error('Error al obtener estado del scheduler:', error);
        });
}

// Actualizar UI del scheduler
function updateSchedulerUI(status) {
    const statusElement = document.getElementById('scheduler-status');
    const isRunning = status.running && status.jobs > 0;
    
    let statusHtml = '';
    
    if (isRunning) {
        statusHtml = `
            <span class="badge bg-success me-2">
                <i class="fas fa-play"></i> Activo
            </span>
            <span class="badge bg-info me-2">
                Escaneos: ${status.scan_count}
            </span>
        `;
        
        if (status.last_scan) {
            const lastScan = new Date(status.last_scan).toLocaleString();
            statusHtml += `
                <span class="badge bg-secondary me-2">
                    Último: ${lastScan}
                </span>
            `;
        }
        
        if (status.next_run) {
            const nextRun = new Date(status.next_run).toLocaleString();
            statusHtml += `
                <span class="badge bg-warning">
                    Próximo: ${nextRun}
                </span>
            `;
        }
    } else {
        statusHtml = `
            <span class="badge bg-secondary">
                <i class="fas fa-pause"></i> Inactivo
            </span>
        `;
    }
    
    statusElement.innerHTML = statusHtml;
}

// Iniciar scheduler
function startScheduler() {
    const interval = document.getElementById('scan_interval').value;
    const networkRange = document.getElementById('scheduled_network_range').value;
    
    if (!interval || interval < 1 || interval > 1440) {
        showToast('El intervalo debe ser entre 1 y 1440 minutos', 'warning');
        return;
    }
    
    const formData = new FormData();
    formData.append('interval_minutes', interval);
    formData.append('network_range', networkRange);
    
    fetch('/scheduler/start', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        showToast(data.mensaje, 'success');
        getSchedulerStatus();
    })
    .catch(error => {
        showToast('Error al iniciar scheduler', 'danger');
    });
}

// Detener scheduler
function stopScheduler() {
    if (confirm('¿Está seguro de que desea detener el escaneo automático?')) {
        fetch('/scheduler/stop', {
            method: 'POST'
        })
        .then(res => res.json())
        .then(data => {
            showToast(data.mensaje, 'info');
            getSchedulerStatus();
        })
        .catch(error => {
            showToast('Error al detener scheduler', 'danger');
        });
    }
}

// Escanear ahora
function scanNow() {
    const networkRange = document.getElementById('scheduled_network_range').value;
    
    const formData = new FormData();
    formData.append('network_range', networkRange);
    
    showToast('Ejecutando escaneo inmediato...', 'info');
    
    fetch('/scheduler/scan-now', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (data.resultado) {
            const result = data.resultado;
            showToast(
                `Escaneo completado: ${result.devices_found} dispositivos encontrados, ${result.unauthorized} no autorizados`, 
                result.unauthorized > 0 ? 'warning' : 'success'
            );
            
            // Actualizar datos en el dashboard
            getScan(true);
            getAlerts();
        } else {
            showToast(data.mensaje, 'success');
        }
        
        getSchedulerStatus();
    })
    .catch(error => {
        showToast('Error al ejecutar escaneo', 'danger');
    });
}

// === FUNCIONES DE MÉTRICAS Y ANÁLISIS ===

// Cargar métricas
function loadMetrics() {
    showToast('Cargando métricas...', 'info');
    
    fetch('/metrics/chart?metric_type=network&hours=24')
        .then(res => res.json())
        .then(data => {
            if (data.chart) {
                document.getElementById('chart-placeholder').style.display = 'none';
                const chartContainer = document.getElementById('metrics-chart-container');
                chartContainer.innerHTML = `<img src="${data.chart}" class="img-fluid" alt="Gráfico de métricas">`;
                showToast(`Gráfico cargado con ${data.data_points} puntos de datos`, 'success');
            }
        })
        .catch(error => {
            showToast('Error al cargar métricas', 'danger');
        });
}

// Mostrar estadísticas de red
function showNetworkStats() {
    fetch('/metrics/network-stats?hours=24')
        .then(res => res.json())
        .then(data => {
            document.getElementById('stat-unique-devices').textContent = data.unique_devices;
            document.getElementById('stat-total-detections').textContent = data.total_detections;
            document.getElementById('stat-intrusion-alerts').textContent = data.intrusion_alerts;
            
            document.getElementById('network-stats').style.display = 'block';
            showToast('Estadísticas de red actualizadas', 'info');
        })
        .catch(error => {
            showToast('Error al cargar estadísticas', 'danger');
        });
}

// Descargar logs
function downloadLogs() {
    fetch('/metrics/logs')
        .then(res => res.json())
        .then(data => {
            if (data.logs.length === 0) {
                showToast('No hay archivos de log disponibles', 'warning');
                return;
            }
            
            let logList = '<div class="list-group">';
            data.logs.forEach(log => {
                const size = (log.size / 1024).toFixed(1);
                const date = new Date(log.modified).toLocaleDateString();
                logList += `
                    <a href="/metrics/logs/${log.filename}" class="list-group-item list-group-item-action" target="_blank">
                        <div class="d-flex w-100 justify-content-between">
                            <h6 class="mb-1">${log.filename}</h6>
                            <small>${date}</small>
                        </div>
                        <small>Tamaño: ${size} KB</small>
                    </a>
                `;
            });
            logList += '</div>';
            
            // Crear modal para mostrar logs
            const modalHtml = `
                <div class="modal fade" id="logsModal" tabindex="-1">
                    <div class="modal-dialog modal-lg">
                        <div class="modal-content bg-dark">
                            <div class="modal-header">
                                <h5 class="modal-title text-white">Archivos de Log</h5>
                                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                ${logList}
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            // Remover modal existente si existe
            const existingModal = document.getElementById('logsModal');
            if (existingModal) {
                existingModal.remove();
            }
            
            // Agregar nuevo modal
            document.body.insertAdjacentHTML('beforeend', modalHtml);
            const modal = new bootstrap.Modal(document.getElementById('logsModal'));
            modal.show();
        })
        .catch(error => {
            showToast('Error al obtener lista de logs', 'danger');
        });
}

// Limpiar datos antiguos
function cleanupData() {
    const days = prompt('¿Cuántos días de datos desea conservar? (mínimo 1, máximo 365)', '30');
    
    if (!days || isNaN(days) || days < 1 || days > 365) {
        showToast('Número de días inválido', 'warning');
        return;
    }
    
    if (!confirm(`¿Está seguro de que desea eliminar todos los datos anteriores a ${days} días?`)) {
        return;
    }
    
    fetch(`/metrics/cleanup?days=${days}`, { method: 'DELETE' })
        .then(res => res.json())
        .then(data => {
            showToast(
                `Limpieza completada: ${data.deleted_metrics} métricas, ${data.deleted_alerts} alertas, ${data.deleted_devices} dispositivos eliminados`,
                'success'
            );
        })
    .catch(error => {
        showToast('Error al limpiar datos', 'danger');
    });
}

// === FUNCIONES DE DISPOSITIVOS ===

// Copiar al portapapeles
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast(`Copiado: ${text}`, 'success');
    }).catch(() => {
        showToast('Error al copiar', 'danger');
    });
}

// Toggle entre vista básica y detallada
function toggleDeviceView() {
    const basicView = document.getElementById('basic-device-view');
    const detailedView = document.getElementById('detailed-device-view');
    const toggleText = document.getElementById('view-toggle-text');
    
    if (currentDeviceView === 'basic') {
        basicView.style.display = 'none';
        detailedView.style.display = 'block';
        toggleText.textContent = 'Vista Básica';
        currentDeviceView = 'detailed';
        loadDetailedDevices();
    } else {
        basicView.style.display = 'block';
        detailedView.style.display = 'none';
        toggleText.textContent = 'Vista Detallada';
        currentDeviceView = 'basic';
    }
}

// Cargar vista detallada de dispositivos
function loadDetailedDevices() {
    fetch('/devices/detailed?hours=24')
        .then(res => res.json())
        .then(data => {
            const table = document.getElementById('devices-detailed');
            const tbody = table.querySelector('tbody');
            tbody.innerHTML = '';
            
            if (data.devices.length === 0) {
                tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted">No hay dispositivos detectados</td></tr>';
                return;
            }
            
            data.devices.forEach(device => {
                const authBadge = device.authorized ? 
                    '<span class="badge bg-success">Autorizado</span>' : 
                    '<span class="badge bg-danger">No Autorizado</span>';
                
                const lastSeen = new Date(device.last_seen).toLocaleString();
                const vendor = device.vendor || 'Desconocido';
                
                tbody.innerHTML += `
                    <tr>
                        <td><code>${device.ip}</code></td>
                        <td>
                            <div>
                                <code class="fw-bold text-info">${device.mac}</code>
                                <button class="btn btn-xs btn-outline-light ms-1" onclick="copyToClipboard('${device.mac}')" title="Copiar MAC">
                                    <i class="fas fa-copy fa-xs"></i>
                                </button>
                            </div>
                        </td>
                        <td><span class="badge bg-secondary">${vendor}</span></td>
                        <td>${device.whitelist_name || '-'}</td>
                        <td><span class="badge bg-info">${device.detections}</span></td>
                        <td><small>${lastSeen}</small></td>
                        <td>${authBadge}</td>
                        <td>
                            ${!device.authorized ? `
                                <button class="btn btn-sm btn-primary" onclick="quickAddToWhitelist('${device.ip}', '${device.mac}')">
                                    <i class="fas fa-plus"></i>
                                </button>
                            ` : ''}
                            <button class="btn btn-sm btn-info" onclick="showDeviceDetails('${device.ip}', '${device.mac}')">
                                <i class="fas fa-info"></i>
                            </button>
                        </td>
                    </tr>
                `;
            });
            
            // Mostrar estadísticas
            showToast(
                `${data.statistics.unique_ips} IPs únicas, ${data.statistics.known_macs} MACs conocidas`,
                'info'
            );
        })
        .catch(error => {
            showToast('Error al cargar dispositivos detallados', 'danger');
        });
}

// Función simplificada para mostrar detalles básicos de dispositivo

// Mostrar detalles de un dispositivo específico
function showDeviceDetails(ip, mac) {
    const details = `
        <div class="card">
            <div class="card-body">
                <h6 class="card-title">Información del Dispositivo</h6>
                <div class="row">
                    <div class="col-6">
                        <strong>IP Address:</strong><br>
                        <code class="text-primary">${ip}</code>
                        <button class="btn btn-sm btn-outline-secondary ms-1" onclick="copyToClipboard('${ip}')">
                            <i class="fas fa-copy fa-xs"></i>
                        </button>
                    </div>
                    <div class="col-6">
                        <strong>MAC Address:</strong><br>
                        <code class="text-primary">${mac}</code>
                        <button class="btn btn-sm btn-outline-secondary ms-1" onclick="copyToClipboard('${mac}')">
                            <i class="fas fa-copy fa-xs"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Crear modal simple
    const modalHtml = `
        <div class="modal fade" id="deviceDetailsModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Detalles del Dispositivo</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        ${details}
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Remover modal existente
    const existingModal = document.getElementById('deviceDetailsModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Agregar y mostrar modal
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    const modal = new bootstrap.Modal(document.getElementById('deviceDetailsModal'));
    modal.show();
}

// === FUNCIONES DE GENERACIÓN DE PDFs ===

// Generar reporte de seguridad completo
async function generateSecurityReport() {
    try {
        showToast('Generando reporte de seguridad...', 'info');
        
        const response = await fetch('/reports/security', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `guardian_security_report_${new Date().toISOString().split('T')[0]}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            showToast('Reporte de seguridad generado exitosamente', 'success');
        } else {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error al generar reporte');
        }
    } catch (error) {
        console.error('Error generando reporte de seguridad:', error);
        showToast('Error al generar reporte de seguridad: ' + error.message, 'error');
    }
}

// Generar reporte de dispositivos
async function generateDeviceReport() {
    try {
        showToast('Generando reporte de dispositivos...', 'info');
        
        const response = await fetch('/reports/devices', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `guardian_devices_report_${new Date().toISOString().split('T')[0]}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            showToast('Reporte de dispositivos generado exitosamente', 'success');
        } else {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error al generar reporte');
        }
    } catch (error) {
        console.error('Error generando reporte de dispositivos:', error);
        showToast('Error al generar reporte de dispositivos: ' + error.message, 'error');
    }
}

// Generar reporte de alertas
async function generateAlertsReport() {
    try {
        showToast('Generando reporte de alertas...', 'info');
        
        const response = await fetch('/reports/alerts', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `guardian_alerts_report_${new Date().toISOString().split('T')[0]}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            showToast('Reporte de alertas generado exitosamente', 'success');
        } else {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error al generar reporte');
        }
    } catch (error) {
        console.error('Error generando reporte de alertas:', error);
        showToast('Error al generar reporte de alertas: ' + error.message, 'error');
    }
}