import socket
import threading
import pymysql
import bcrypt

# Server settings
HOST = '127.0.0.1'
PORT = 12345

# Database settings
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'drowsydreamy'
DB_NAME = 'chat_app'

# Store clients and their addresses
clients = []

def handle_client(client_socket, addr):
    username = None
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message.startswith("/login"):
                username, password = message.split()[1:3]
                if authenticate_user(username, password):
                    client_socket.send("/login_success".encode('utf-8'))
                    clients.append((client_socket, username))
                    broadcast(f"{username} has joined the chat!", client_socket)
                else:
                    client_socket.send("/login_failed".encode('utf-8'))
            elif message.startswith("/register"):
                username, password = message.split()[1:3]
                if register_user(username, password):
                    client_socket.send("/register_success".encode('utf-8'))
                else:
                    client_socket.send("/register_failed".encode('utf-8'))
            else:
                if username:
                    broadcast(message, client_socket)
        except Exception as e:
            print(f"Error: {e}")
            if username:
                clients.remove((client_socket, username))
                broadcast(f"{username} has left the chat.", client_socket)
            client_socket.close()
            break

def broadcast(message, client_socket):
    for client, _ in clients:
        client.send(message.encode('utf-8'))

def authenticate_user(username, password):
    try:
        connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        cursor = connection.cursor()
        cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
        record = cursor.fetchone()
        connection.close()
        if record and bcrypt.checkpw(password.encode('utf-8'), record[0].encode('utf-8')):
            return True
        return False
    except Exception as e:
        print(f"Error in authenticate_user: {e}")
        return False

def register_user(username, password):
    try:
        connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        cursor = connection.cursor()
        cursor.execute("SELECT username FROM users WHERE username=%s", (username,))
        if cursor.fetchone():
            connection.close()
            return False
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        print(f"Error in register_user: {e}")
        return False

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f'Server started on {HOST}:{PORT}')

    while True:
        client_socket, addr = server.accept()
        print(f'Connection from {addr}')
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

if __name__ == "__main__":
    main()
