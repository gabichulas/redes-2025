import socket
import threading

clientes_conectados = {}  # Diccionario: {socket: nombre_usuario}
lock = threading.Lock()

def manejar_cliente(conn, addr):
    try:
        # Paso 1: Recibir nombre de usuario al conectarse
        nombre = conn.recv(1024).decode()
        
        with lock:
            if nombre in clientes_conectados.values():
                conn.send("Nombre ya en uso. Desconectando...".encode())
                conn.close()
                return
            clientes_conectados[conn] = nombre
        
        print(f"{nombre} se ha conectado desde {addr}")
        conn.send(f"Bienvenido, {nombre}!".encode())
        
        # Paso 2: Recibir mensajes del cliente
        while True:
            mensaje = conn.recv(1024).decode()
            if not mensaje or mensaje.lower() == "exit":
                break
            print(f"[{nombre}]:{mensaje}")
            
    except Exception as e:
        print(f"Error con {nombre}: {e}")
    finally:
        with lock:
            if conn in clientes_conectados:
                print(f"{clientes_conectados[conn]} se desconectó")
                del clientes_conectados[conn]
        conn.close()

def enviar_mensajes_servidor():
    while True:
        mensaje = input()
        if mensaje.lower() == "exit":
            if clientes_conectados:
                print("No se puede cerrar con clientes conectados")
            else:
                print("Cerrando servidor...")
                os._exit(0)
        
        with lock:
            for cliente in list(clientes_conectados.keys()):
                try:
                    cliente.send(f"[Servidor]: {mensaje}".encode())
                except:
                    del clientes_conectados[cliente]

def servidor():
    host = '0.0.0.0'
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"Servidor escuchando en {host}:{port}")

    threading.Thread(target=enviar_mensajes_servidor, daemon=True).start()

    try:
        while True:
            conn, addr = server_socket.accept()
            threading.Thread(target=manejar_cliente, args=(conn, addr)).start()
    except KeyboardInterrupt:
        if clientes_conectados:
            print("No se puede cerrar con clientes conectados")
        else:
            server_socket.close()

if __name__ == "__main__":
    import os
    servidor()