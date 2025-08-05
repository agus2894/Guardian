async function getScan() {
    const range = document.getElementById('network_range').value || "192.168.0.0/24";

    const res = await fetch('/scan/?network_range=' + encodeURIComponent(range));
    const data = await res.json();
    const table = document.getElementById('devices');
    table.innerHTML = "<tr><th>IP</th><th>Autorizado</th><th>Última conexión</th></tr>";

    const response = await fetch("/devices/");
    const allDevices = await response.json();

    allDevices.forEach(d => {
        const estado = d.authorized ? "Autorizado" : "No autorizado";
        const clase = d.authorized ? "table-success" : "table-danger";
        table.innerHTML += `<tr class="${clase}"><td>${d.ip}</td><td>${estado}</td><td>${d.last_seen}</td></tr>`;
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
    const mac = document.getElementById('device_mac').value;
    const ip = document.getElementById('device_ip').value;

    const data = { name: name, mac: mac, ip: ip };

    const res = await fetch('/whitelist/agregar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    if (res.ok) {
        alert("Dispositivo agregado a la whitelist");
        document.getElementById('device_name').value = "";
        document.getElementById('device_mac').value = "";
        document.getElementById('device_ip').value = "";
    } else {
        alert("Error al agregar a whitelist");
    }
}
