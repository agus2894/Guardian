import sqlite3

def add_to_whitelist(name, mac, ip=None):
    conn = sqlite3.connect("guardian.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO whitelist (name, mac, ip) VALUES (?, ?, ?)", (name, mac, ip))
        conn.commit()
        print(f"[✔] {name} agregado a la lista blanca.")
    except sqlite3.IntegrityError:
        print(f"[!] Ya existe un dispositivo con esa MAC.")
    finally:
        conn.close()
if __name__ == "__main__":
    nombre = "Mi Celular"
    mac = "f8:ef:5d:bc:ed:8e"
    ip = "192.168.0.7"

    add_to_whitelist(nombre, mac, ip)
