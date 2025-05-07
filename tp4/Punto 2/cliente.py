import socket
import threading

def recibir_mensajes(sock):
    while True:
        try:
            mensaje = sock.recv(1024).decode()
            if not mensaje:
                print("Servidor cerró la conexión")
                break
            print(mensaje)
        except:
            print("Desconectado del servidor")
            break

def cliente():
    host = input("IP del servidor: ")
    port = 5000
    nombre = input("Tu nombre de usuario: ")

    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect((host, port))
    
    # Paso 1: Enviar nombre al servidor
    cliente_socket.send(nombre.encode())
    
    # Paso 2: Iniciar hilo de recepción
    threading.Thread(target=recibir_mensajes, args=(cliente_socket,), daemon=True).start()

    # Paso 3: Enviar mensajes
    while True:
        mensaje = input()
        cliente_socket.send(mensaje.encode())
        if mensaje.lower() == "exit":
            cliente_socket.close()
            break

if __name__ == "__main__":
    cliente()