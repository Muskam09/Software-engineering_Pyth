import socket
import select


HOST = '127.0.0.1'
PORT = 10500


def start_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Сервер запущено на {HOST}:{PORT}")

    sockets_list = [server_socket]
    clients = {}

    def broadcast_message(message, sender_socket):
        for client_socket in clients:
            if client_socket != sender_socket:
                try:
                    client_socket.send(message)
                except Exception:
                    client_socket.close()
                    sockets_list.remove(client_socket)
                    del clients[client_socket]

    while True:
        read_sockets, _, exception_sockets = select.select(
            sockets_list, [], sockets_list
        )
        for notified_socket in read_sockets:
            if notified_socket == server_socket:
                client_socket, client_address = server_socket.accept()
                user = client_socket.recv(1024).decode('utf-8')
                sockets_list.append(client_socket)
                clients[client_socket] = user
                print(f"Підключився новий клієнт: {user} ({client_address})")
                broadcast_message(
                    f"{user} приєднався до чату!\n".encode('utf-8'),
                    client_socket)
            else:
                try:
                    message = notified_socket.recv(1024)
                    if not message:
                        raise ConnectionResetError()
                    user = clients[notified_socket]
                    print(
                        f"Отримано повідомлення від {user}: "
                        f"{message.decode('utf-8')}"
                    )
                    broadcast_message(
                        f"{user}: {message.decode('utf-8')}".encode('utf-8'),
                        notified_socket)
                except Exception:
                    print(f"Клієнт {clients[notified_socket]} відключився")
                    sockets_list.remove(notified_socket)
                    del clients[notified_socket]

        for notified_socket in exception_sockets:
            sockets_list.remove(notified_socket)
            del clients[notified_socket]


if __name__ == "__main__":
    start_server()
