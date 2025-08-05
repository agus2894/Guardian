// static/js/dashboard.js

async function getScan() {
    const range = document.getElementById('network_range').value || "192.168.0.0/24";

    const res = await fetch('/scan/?network_range=' + encodeURIComponent(range));
    const data = await res.json();
    const table = document.getElementById('devices');
    table.innerHTML = "<tr><th>IP</th></tr>";
    data.dispositivos_detectados.forEach(d => {
        table.innerHTML += `<tr><td>${d.ip}</td></tr>`;
    });
}

async function getAlerts() {
    const res = await fetch('/alerts/');
    const data = await res.json();
    const table = document.getElementById('alerts');
    table.innerHTML = "<tr><th>ID</th><th>Tipo</th><th>Hora</th><th>Descripción</th></tr>";
    data.forEach(a => {
        table.innerHTML += `<tr><td>${a.id}</td><td>${a.type}</td><td>${a.timestamp}</td><td>${a.description}</td></tr>`;
    });
}

async function clearAlerts() {
    if (confirm("¿Seguro que querés eliminar todas las alertas?")) {
        await fetch('/alerts/clear', { method: 'DELETE' });
        alert("Alertas eliminadas");
        getAlerts();
    }
}

async function addToWhitelist() {
    const name = document.getElementById('device_name').value;
    const ip = document.getElementById('device_ip').value;

    const formData = new FormData();
    formData.append("nombre", name);
    formData.append("ip", ip);

    const res = await fetch('/whitelist/add', {
        method: 'POST',
        body: formData
    });

    if (res.ok) {
        alert("✅ Dispositivo agregado a la whitelist");
        document.getElementById('device_name').value = "";
        document.getElementById('device_ip').value = "";
    } else {
        alert("❌ Error al agregar a whitelist");
    }
}
