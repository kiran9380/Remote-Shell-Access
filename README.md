
---
## Remote_Shell_Access Project Documentation

### Overview
This project consists of two Python scripts that allow remote command execution and file transfer between a server and a client. The server listens for incoming connections, accepts a client connection, and can execute commands on the client or transfer files between the server and client.

### Files
1. **Techboy_server.py** - The server script.
2. **kiran_client.py** - The client script.

### Techboy_server.py

### Code
```
import socket

# Create a socket object for IPv4 and TCP
patil = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
patil.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Get the host and port from user input
host = input("Enter the host (e.g., 127.0.0.1): ")
port = int(input("Enter the port (e.g., 8888): "))

# Bind the socket to the specified host and port
patil.bind((host, port))
print("listening")

# Listen for incoming connections (allow only 1 connection)
patil.listen(1)

# Accept a connection from a client
kiran, addr = patil.accept()
print("connected to", addr)

# Loop to send and receive data
while True:
    # Prompt for user input
    cmd = input("$ ")
    # Send the command to the client
    kiran.send(cmd.encode())
    # Check for exit command to break the loop
    if cmd == "exit":
        break
    # Handle file upload command
    elif cmd.startswith("upload "):
        filename = cmd.split(" ", 1)[1]
        try:
            # Open the file and read its contents
            with open(filename, "rb") as f:
                file_data = f.read()
            # Send the file data to the client
            kiran.sendall(file_data)
            # Send a DONE marker to indicate end of file
            kiran.send(b"DONE")
            print(f"Uploaded {filename} successfully")
        except FileNotFoundError:
            print(f"File {filename} not found")
            kiran.send(b"ERROR")
    # Handle file download command
    elif cmd.startswith("download "):
        filename = cmd.split(" ", 1)[1]
        with open(filename, "wb") as f:
            while True:
                # Receive file data from the client
                file_data = kiran.recv(1024)
                # Check for DONE marker to end file writing
                if file_data.endswith(b"DONE"):
                    f.write(file_data[:-4])
                    break
                f.write(file_data)
            print(f"Downloaded {filename} successfully")
    else:
        # Receive and print the command output from the client
        output = kiran.recv(1024).decode()
        print(output)

# Close the connection
kiran.close()
patil.close()

```

#### Code Explanation

```python
import socket

# Create a socket object for IPv4 and TCP
patil = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
patil.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
```
- **socket.socket(socket.AF_INET, socket.SOCK_STREAM)**: Creates a socket object using IPv4 and TCP.
- **patil.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)**: Allows the socket to reuse the address.

```python
# Get the host and port from user input
host = input("Enter the host (e.g., 127.0.0.1): ")
port = int(input("Enter the port (e.g., 8888): "))
```
- **input**: Prompts the user to enter the host and port for the server.

```python
# Bind the socket to the specified host and port
patil.bind((host, port))
print("listening")
```
- **patil.bind((host, port))**: Binds the socket to the given host and port.
- **print("listening")**: Informs the user that the server is now listening for connections.

```python
# Listen for incoming connections (allow only 1 connection)
patil.listen(1)
```
- **patil.listen(1)**: Listens for incoming connections. The parameter `1` specifies the maximum number of queued connections.

```python
# Accept a connection from a client
kiran, addr = patil.accept()
print("connected to", addr)
```
- **kiran, addr = patil.accept()**: Accepts a connection from a client and returns a new socket object (`kiran`) and the address of the client (`addr`).
- **print("connected to", addr)**: Prints the address of the connected client.

```python
# Loop to send and receive data
while True:
    # Prompt for user input
    cmd = input("$ ")
    # Send the command to the client
    kiran.send(cmd.encode())
    # Check for exit command to break the loop
    if cmd == "exit":
        break
    # Handle file upload command
    elif cmd.startswith("upload "):
        filename = cmd.split(" ", 1)[1]
        try:
            # Open the file and read its contents
            with open(filename, "rb") as f:
                file_data = f.read()
            # Send the file data to the client
            kiran.sendall(file_data)
            # Send a DONE marker to indicate end of file
            kiran.send(b"DONE")
            print(f"Uploaded {filename} successfully")
        except FileNotFoundError:
            print(f"File {filename} not found")
            kiran.send(b"ERROR")
    # Handle file download command
    elif cmd.startswith("download "):
        filename = cmd.split(" ", 1)[1]
        with open(filename, "wb") as f:
            while True:
                # Receive file data from the client
                file_data = kiran.recv(1024)
                # Check for DONE marker to end file writing
                if file_data.endswith(b"DONE"):
                    f.write(file_data[:-4])
                    break
                f.write(file_data)
            print(f"Downloaded {filename} successfully")
    else:
        # Receive and print the command output from the client
        output = kiran.recv(1024).decode()
        print(output)
```
- **while True**: Starts an infinite loop to continuously send and receive data.
- **cmd = input("$ ")**: Prompts the user to enter a command.
- **kiran.send(cmd.encode())**: Sends the command to the client.
- **if cmd == "exit"**: Breaks the loop if the command is "exit".
- **elif cmd.startswith("upload ")**: Handles file upload from server to client.
  - **filename = cmd.split(" ", 1)[1]**: Extracts the filename from the command.
  - **with open(filename, "rb") as f**: Opens the file in binary read mode.
  - **file_data = f.read()**: Reads the file contents.
  - **kiran.sendall(file_data)**: Sends the file data to the client.
  - **kiran.send(b"DONE")**: Sends a DONE marker to indicate end of file.
  - **print(f"Uploaded {filename} successfully")**: Prints success message.
  - **except FileNotFoundError**: Handles the case where the file is not found.
  - **kiran.send(b"ERROR")**: Sends an error message to the client.
- **elif cmd.startswith("download ")**: Handles file download from client to server.
  - **filename = cmd.split(" ", 1)[1]**: Extracts the filename from the command.
  - **with open(filename, "wb") as f**: Opens the file in binary write mode.
  - **while True**: Starts an infinite loop to receive file data.
  - **file_data = kiran.recv(1024)**: Receives file data from the client.
  - **if file_data.endswith(b"DONE")**: Checks for DONE marker to end file writing.
  - **f.write(file_data[:-4])**: Writes the last chunk of file data excluding the DONE marker.
  - **break**: Breaks the loop.
  - **f.write(file_data)**: Writes the file data to the file.
  - **print(f"Downloaded {filename} successfully")**: Prints success message.
- **else**: Handles regular command execution.
  - **output = kiran.recv(1024).decode()**: Receives and decodes the command output from the client.
  - **print(output)**: Prints the output.

```python
# Close the connection
kiran.close()
patil.close()
```
- **kiran.close()**: Closes the client socket.
- **patil.close()**: Closes the server socket.

### kiran_client.py

### Code
```
import socket
import subprocess
import os

# Create a socket object for IPv4 and TCP
patil = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("connecting....")

# Get the server host and port from user input
host = input("Enter the server host (e.g., 127.0.0.1): ")
port = int(input("Enter the server port (e.g., 8888): "))

# Attempt to connect to the server
while True:
    try:
        patil.connect((host, port))
        break
    except ConnectionRefusedError:
        pass
print("connected")

current_dir = os.getcwd()

# Loop to receive and execute commands from the server
while True:
    # Receive command from server
    receive = patil.recv(1024).decode()
    # Check for exit command to break the loop
    if receive == "exit":
        break
    # Handle cd command to change directory
    elif receive.startswith("cd "):
        try:
            new_dir = receive[3:].strip()
            os.chdir(new_dir)
            current_dir = os.getcwd()
            output = f"Changed directory to {current_dir}"
        except Exception as e:
            output = str(e)
        patil.send(output.encode())
    # Handle file upload command
    elif receive.startswith("upload "):
        filename = receive.split(" ", 1)[1]
        with open(filename, "wb") as f:
            while True:
                # Receive file data from the server
                file_data = patil.recv(1024)
                # Check for DONE marker to end file writing
                if file_data.endswith(b"DONE"):
                    f.write(file_data[:-4])
                    break
                f.write(file_data)
        patil.send(b"Upload complete")
    # Handle file download command
    elif receive.startswith("download "):
        filename = receive.split(" ", 1)[1]
        try:
            # Open the file and read its contents
            with open(filename, "rb") as f:
                file_data = f.read()
            # Send the file data to the server
            patil.sendall(file_data)
            # Send a DONE marker to indicate end of file
            patil.send(b"DONE")
        except FileNotFoundError:
            patil.send(b"ERROR")
    else:
        # Execute command and capture output
        try:
            output = subprocess.check_output(receive, shell=True, stderr=subprocess.STDOUT, cwd=current_dir).decode()
        except subprocess.CalledProcessError as e:
            output = e.output.decode()
        # Send the output back to the server
        patil.send(output.encode())

# Close the connection
patil.close()

```

#### Code Explanation

```python
import socket
import subprocess
import os

# Create a socket object for IPv4 and TCP
patil = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("connecting....")
```
- **socket.socket(socket.AF_INET, socket.SOCK_STREAM)**: Creates a socket object using IPv4 and TCP.
- **print("connecting....")**: Prints a message indicating that the client is attempting to connect to the server.

```python
# Get the server host and port from user input
host = input("Enter the server host (e.g., 127.0.0.1): ")
port = int(input("Enter the server port (e.g., 8888): "))
```
- **input**: Prompts the user to enter the server host and port.

```python
# Attempt to connect to the server
while True:
    try:
        patil.connect((host, port))
        break
    except ConnectionRefusedError:
        pass
print("connected")
```
- **while True**: Starts an infinite loop to attempt connecting to the server.
- **try...except ConnectionRefusedError**: Attempts to connect to the server and handles the case where the connection is refused.
- **patil.connect((host, port))**: Connects to the server.
- **print("connected")**: Prints a message indicating that the client is connected to the server.

```python
current_dir = os.getcwd()
```
- **os.getcwd()**: Gets the current working directory.

```python
# Loop to receive and execute commands from the server
while True:
    # Receive command from server
    receive = patil.recv(1024).decode()
    # Check for exit command to break the loop
    if receive == "exit":
        break
    # Handle cd command to change directory
    elif receive.startswith("cd "):
        try:
            new_dir = receive[3:].strip()
            os.chdir(new_dir)
            current_dir = os.getcwd()
            output = f"Changed directory to {current_dir}"
        except Exception as e:
            output = str(e)
        patil.send(output.encode())
    # Handle file upload command
    elif receive.startswith("upload "):
        filename = receive.split(" ", 1)[1]
        with open(filename, "wb") as f:
            while True:
                # Receive file data from the server
                file_data = patil.recv(1024)
                # Check for DONE marker to end file writing
                if file_data.endswith(b"DONE"):
                    f.write(file_data[:-4])
                    break
                f.write(file_data)
        patil.send(b"Upload complete")
    # Handle file download command
    elif receive.startswith("download "):
        filename = receive.split(" ", 1)[1]
        try:
            # Open the file and read its contents
            with open(filename, "rb") as f:
                file_data = f.read()
            # Send the file data to the server
            patil.sendall(file_data)
            # Send a DONE marker

 to indicate end of file
            patil.send(b"DONE")
        except FileNotFoundError:
            patil.send(b"ERROR")
    else:
        # Execute command and capture output
        try:
            output = subprocess.check_output(receive, shell=True, stderr=subprocess.STDOUT, cwd=current_dir).decode()
        except subprocess.CalledProcessError as e:
            output = e.output.decode()
        # Send the output back to the server
        patil.send(output.encode())
```
- **while True**: Starts an infinite loop to receive and execute commands from the server.
- **receive = patil.recv(1024).decode()**: Receives a command from the server and decodes it.
- **if receive == "exit"**: Breaks the loop if the command is "exit".
- **elif receive.startswith("cd ")**: Handles the `cd` command to change directory.
  - **new_dir = receive[3:].strip()**: Extracts the new directory from the command.
  - **os.chdir(new_dir)**: Changes the current working directory to the new directory.
  - **current_dir = os.getcwd()**: Updates the current working directory.
  - **output = f"Changed directory to {current_dir}"**: Prepares a success message.
  - **except Exception as e**: Handles any exceptions that occur during the directory change.
  - **output = str(e)**: Prepares an error message.
  - **patil.send(output.encode())**: Sends the message back to the server.
- **elif receive.startswith("upload ")**: Handles file upload from server to client.
  - **filename = receive.split(" ", 1)[1]**: Extracts the filename from the command.
  - **with open(filename, "wb") as f**: Opens the file in binary write mode.
  - **while True**: Starts an infinite loop to receive file data.
  - **file_data = patil.recv(1024)**: Receives file data from the server.
  - **if file_data.endswith(b"DONE")**: Checks for DONE marker to end file writing.
  - **f.write(file_data[:-4])**: Writes the last chunk of file data excluding the DONE marker.
  - **break**: Breaks the loop.
  - **f.write(file_data)**: Writes the file data to the file.
  - **patil.send(b"Upload complete")**: Sends a success message back to the server.
- **elif receive.startswith("download ")**: Handles file download from client to server.
  - **filename = receive.split(" ", 1)[1]**: Extracts the filename from the command.
  - **try...except FileNotFoundError**: Attempts to open and read the file, and handles the case where the file is not found.
  - **with open(filename, "rb") as f**: Opens the file in binary read mode.
  - **file_data = f.read()**: Reads the file contents.
  - **patil.sendall(file_data)**: Sends the file data to the server.
  - **patil.send(b"DONE")**: Sends a DONE marker to indicate end of file.
  - **patil.send(b"ERROR")**: Sends an error message to the server.
- **else**: Handles regular command execution.
  - **try...except subprocess.CalledProcessError**: Executes the command and captures the output or error.
  - **output = subprocess.check_output(receive, shell=True, stderr=subprocess.STDOUT, cwd=current_dir).decode()**: Executes the command and captures the output.
  - **output = e.output.decode()**: Captures the error output if the command fails.
  - **patil.send(output.encode())**: Sends the output back to the server.

```python
# Close the connection
patil.close()
```
- **patil.close()**: Closes the client socket.

---

### Usage

1. **Start the Server**:
   - Run `Techboy_server.py`.
   - Enter the host (e.g., `127.0.0.1`) and port (e.g., `8888`).

2. **Start the Client**:
   - Run `kiran_client.py`.
   - Enter the server host (e.g., `127.0.0.1`) and port (e.g., `8888`).

3. **Commands**:
   - Use regular shell commands (e.g., `ls`, `pwd`, `echo Hello`).
   - Use `cd <directory>` to change the directory on the client.
   - Use `upload <filename>` to upload a file from the server to the client.
   - Use `download <filename>` to download a file from the client to the server.
   - Use `exit` to close the connection.

### Notes

- Ensure the specified files exist on the respective machines for upload/download operations.
- Both scripts should be run on machines that can communicate over the specified network (e.g., same local network or configured for remote access).

With this documentation, you should have a clear understanding of how the scripts work and how to use them for remote command execution and file transfer.
