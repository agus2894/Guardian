// static/js/dashboard.js

// Escanear red
function getScan() {
    const range = document.getElementById("network_range").value || "192.168.0.0/24";
    fetch(`/scan/?network_range=${encodeURIComponent(range)}`)
        .then(res => res.json())
        .then(data => {
            const table = document.getElementById("devices");
            table.innerHTML = "<tr><th>IP</th><th>Autorizado</th></tr>";
            data.dispositivos_detectados.forEach(dev => {
                table.innerHTML += `
                    <tr>
                        <td>${dev.ip}</td>
                        <td>${dev.autorizado ? "Sí" : "No"}</td>
                    </tr>
                `;
            });
        });
}

// Obtener alertas
function getAlerts() {
    fetch("/alerts/")
        .then(res => res.json())
        .then(data => {
            const table = document.getElementById("alerts");
            table.innerHTML = "<tr><th>ID</th><th>Tipo</th><th>Hora</th><th>Descripción</th></tr>";
            data.forEach(alert => {
                table.innerHTML += `
                    <tr>
                        <td>${alert.id}</td>
                        <td>${alert.type}</td>
                        <td>${alert.timestamp}</td>
                        <td>${alert.description}</td>
                    </tr>
                `;
            });
        });
}

// Limpiar alertas
function clearAlerts() {
    fetch("/alerts/clear", { method: "DELETE" })
        .then(res => res.json())
        .then(data => {
            alert(data.mensaje);
            getAlerts();
        });
}

// Obtener whitelist
function getWhitelist() {
    fetch("/whitelist/")
        .then(res => res.json())
        .then(data => {
            const table = document.getElementById("whitelist");
            table.innerHTML = "<tr><th>Nombre</th><th>IP</th></tr>";
            data.whitelist.forEach(item => {
                table.innerHTML += `
                    <tr>
                        <td>${item.name}</td>
                        <td>${item.ip}</td>
                    </tr>
                `;
            });
        });
}

// Agregar a whitelist (usando FormData)
function addToWhitelist() {
    const name = document.getElementById("device_name").value;
    const ip = document.getElementById("device_ip").value;

    const formData = new FormData();
    formData.append("nombre", name);
    formData.append("ip", ip);

    fetch("/whitelist/agregar", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        alert(data.mensaje);
        getWhitelist();
    });
}
