# Simple Chat System

A lightweight terminal-based chat application built using Python and WebSockets.
The project supports multiple users communicating in real time, along with basic admin moderation features.

---

## Features

* Real-time messaging using WebSockets
* Multiple client support
* Admin controls (username: admin, pass: adminpass)

  * Kick users
  * Ban users
* Simple terminal-based interaction
* Beginner-friendly project structure

---

## Tech Stack

* Python
* WebSockets
* Async Programming

---

## Project Structure

```bash
.
├── server.py
├── client.py
└── bans.txt
```

---

## How to Run

### 1. Install dependencies

```bash
pip install websockets
```

### 2. Start the server

```bash
python server.py
```

### 3. Start clients in separate terminals

```bash
python client.py
```

Open multiple terminals to simulate different users chatting with each other.

---

## Admin Functionality

The admin user can perform moderation actions such as:

* Kicking users from the chat
* Banning users

---

## Future Improvements

* Graphical UI/UX
* Timestamped messages
* Authentication system
* Private messaging
* Better admin dashboard/features
* Persistent chat history

---

## Learning Outcomes

This project helped in understanding:

* WebSocket communication
* Client-server architecture
* Async programming in Python
* Real-time systems

---

## Author

Developed as a learning project to explore networking and real-time communication concepts using Python.
