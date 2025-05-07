import socket
import threading
import sys

username = input("Ingresa tu nombre de usuario: ")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.bind(('0.0.0.0', 60000))

stop_event = threading.Event()

def send_messages():
    while not stop_event.is_set():
        message = str(input(f"{username}:"))
        if message == "exit":
            sock.sendto(f"{username}:exit".encode(), ('255.255.255.255', 60000))
            stop_event.set() 
            break
        sock.sendto(f"{username}:{message}".encode(), ('255.255.255.255', 60000))

def receive_messages():
    while not stop_event.is_set():
        try:
            data, addr = sock.recvfrom(1024)
            ip_remitente = addr[0]
            mensaje = data.decode()
            
            usuario, contenido = mensaje.split(":", 1)
            
            if contenido == "nuevo":
                print(f"El usuario {usuario} ({ip_remitente}) se ha unido a la conversación")
            elif contenido == "exit":
                print(f"El usuario {usuario} ({ip_remitente}) ha abandonado la conversación")
                if usuario == username: 
                    stop_event.set()
            else:
                print(f"{usuario} ({ip_remitente}) dice: {contenido}")
        except OSError:
            break

receiver_thread = threading.Thread(target=receive_messages, daemon=True)
sender_thread = threading.Thread(target=send_messages)

receiver_thread.start()
sender_thread.start()

sender_thread.join()
stop_event.set()
sock.close()
print("Chat finalizado. chauuuuuuuuuuuuuuuu")