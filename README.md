
# Chat Application

This repository contains the files for a chat application with both a client and a server component. The application supports user registration, login, and real-time messaging between connected clients. The client includes a graphical user interface (GUI) for a better user experience.

## Files in this Repository

1. `client.py` - The primary client-side script with a GUI implemented using Tkinter.
2. `client2.py` - An alternative client-side script with similar functionality.
3. `server.py` - The server-side script that handles client connections, user authentication, and message routing.
4. `acaDB.sql` - The SQL script to create the necessary database schema.

## Features

- **User Authentication**: Supports user registration and login using a MySQL database with hashed passwords.
- **Real-time Messaging**: Clients can send and receive messages in real time.
- **Graphical User Interface**: The client uses Tkinter for a user-friendly chat interface.
- **Multi-threading**: The server handles multiple client connections concurrently.

## Getting Started

### Prerequisites

- Python 3.x
- Tkinter library (included with standard Python installations)
- MySQL server
- `pymysql` library for Python
- `bcrypt` library for password hashing

### Setup

1. **Database Setup**:
   - Import the `acaDB.sql` script to set up the database.
   - Ensure your MySQL server is running and accessible.

2. **Install Required Libraries**:
   ```sh
   pip install pymysql bcrypt
   ```

3. **Configure Server Settings**:
   - Edit the `server.py` file to match your database settings:
     ```python
     DB_HOST = 'localhost'
     DB_USER = 'root'
     DB_PASSWORD = 'your_password'
     DB_NAME = 'chat_app'
     ```

### Running the Application

1. **Start the Server**:
   ```sh
   python server.py
   ```
   - The server will start and listen for incoming connections.

2. **Start the Client**:
   ```sh
   python client.py
   ```
   - This will open the client GUI where you can register or log in.

### Using the Application

- **Register**: Enter a username and password, then click the "Register" button.
- **Login**: Enter your registered username and password, then click the "Login" button.
- **Send Messages**: Type a message and press Enter to send it to the chat.
