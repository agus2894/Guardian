# scripts/add_whitelist.py

from db.whitelist import add_to_whitelist

def main():
    print("Agregar dispositivo a la Whitelist")
    nombre = input("Nombre del dispositivo: ")
    ip = input("Dirección IP del dispositivo: ")

    if nombre and ip:
        add_to_whitelist(nombre, ip)
        print(" Dispositivo agregado correctamente.")
    else:
        print(" Faltan datos.")

if __name__ == "__main__":
    main()
