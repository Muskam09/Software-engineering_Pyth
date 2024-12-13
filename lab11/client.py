import socket
import threading


HOST = '127.0.0.1'
PORT = 10500


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except Exception:
            print("З'єднання з сервером втрачено")
            client_socket.close()
            break


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    user = input("Введіть ваше ім'я: ")
    client_socket.send(user.encode('utf-8'))

    threading.Thread(target=receive_messages, args=(client_socket,),
                     daemon=True).start()

    print("Ви можете надсилати повідомлення:")
    while True:
        try:
            message = input()
            if message.lower() == 'exit':
                break
            client_socket.send(message.encode('utf-8'))
        except Exception:
            break

    client_socket.close()


if __name__ == "__main__":
    start_client()
