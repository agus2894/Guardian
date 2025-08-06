async function getScan() {
    const range = document.getElementById('network_range').value || "192.168.0.0/24";

    const res = await fetch('/scan/?network_range=' + encodeURIComponent(range));
    const data = await res.json();
    const table = document.getElementById('devices');
    table.innerHTML = "<tr><th>IP</th><th>Autorizado</th></tr>";

    data.dispositivos_detectados.forEach(d => {
        const autorizado = d.autorizado ? "✅" : "❌";
        table.innerHTML += `<tr><td>${d.ip}</td><td>${autorizado}</td></tr>`;
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

async function getWhitelist() {
    const res = await fetch('/whitelist/');
    const data = await res.json();
    const table = document.getElementById('whitelist');
    table.innerHTML = "<tr><th>ID</th><th>Nombre</th><th>IP</th></tr>";

    data.whitelist.forEach(w => {
        table.innerHTML += `<tr><td>${w.id}</td><td>${w.name}</td><td>${w.ip}</td></tr>`;
    });
}

async function addToWhitelist() {
    const name = document.getElementById('device_name').value;
    const ip = document.getElementById('device_ip').value;

    const data = new URLSearchParams();
    data.append("nombre", name);
    data.append("ip", ip);

    const res = await fetch('/whitelist/agregar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: data
    });

    if (res.ok) {
        alert("Dispositivo agregado a la whitelist");
        document.getElementById('device_name').value = "";
        document.getElementById('device_ip').value = "";
        getWhitelist();
    } else {
        alert("Error al agregar a whitelist");
    }
}
