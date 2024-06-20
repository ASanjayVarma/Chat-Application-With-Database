import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime

# Client settings
HOST = '127.0.0.1'
PORT = 12345

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Application")
        self.root.geometry("600x400")

        self.username = tk.StringVar()
        self.password = tk.StringVar()
        
        self.setup_login()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((HOST, PORT))

    def setup_login(self):
        self.login_frame = tk.Frame(self.root, bg='lightblue')
        self.login_frame.pack(pady=20)

        tk.Label(self.login_frame, text="Username:", font=("Arial", 14), bg='lightblue', fg='black').grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(self.login_frame, textvariable=self.username, font=("Arial", 14)).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.login_frame, text="Password:", font=("Arial", 14), bg='lightblue', fg='black').grid(row=1, column=0, padx=10, pady=5)
        tk.Entry(self.login_frame, textvariable=self.password, show='*', font=("Arial", 14)).grid(row=1, column=1, padx=10, pady=5)

        tk.Button(self.login_frame, text="Login", command=self.login, font=("Arial", 14), bg='white', fg='black').grid(row=2, column=0, padx=10, pady=5)
        tk.Button(self.login_frame, text="Register", command=self.register, font=("Arial", 14), bg='white', fg='black').grid(row=2, column=1, padx=10, pady=5)

    def setup_chat(self):
        self.login_frame.pack_forget()

        self.chat_frame = tk.Frame(self.root, bg='white')
        self.chat_frame.pack(fill=tk.BOTH, expand=True)

        self.message_entry = tk.Entry(self.root, font=("Arial", 14), bg='lightgray', fg='black')
        self.message_entry.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        self.message_entry.bind("<Return>", self.send_message)

        self.chat_area = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, state='disabled', font=("Arial", 12), bg='white', fg='black')
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_area.pack_propagate(False)
        self.chat_area.configure(height=15)  # Set a minimum height for the chat area

        self.root.bind("<FocusIn>", lambda event: self.message_entry.focus_set())

        threading.Thread(target=self.receive_messages).start()

    def login(self):
        username = self.username.get()
        password = self.password.get()
        
        self.client_socket.send(f"/login {username} {password}".encode('utf-8'))
        
        response = self.client_socket.recv(1024).decode('utf-8')
        if response == "/login_success":
            self.setup_chat()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def register(self):
        try:
            username = self.username.get()
            password = self.password.get()
            
            self.client_socket.send(f"/register {username} {password}".encode('utf-8'))
            
            response = self.client_socket.recv(1024).decode('utf-8')
            if response == "/register_success":
                messagebox.showinfo("Register Success", "Registration successful, you can now login")
            else:
                messagebox.showerror("Register Failed", "Username already exists")
        except Exception as e:
            print(f"Error in register: {e}")
            messagebox.showerror("Error", f"An error occurred during registration: {e}")

    def send_message(self, event):
        message = self.message_entry.get()
        self.client_socket.send(f"{self.username.get()}: {message}".encode('utf-8'))
        self.message_entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                self.display_message(message)
            except:
                self.client_socket.close()
                break

    def display_message(self, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message + '\n')
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
