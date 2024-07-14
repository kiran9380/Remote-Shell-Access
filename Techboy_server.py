import socket

# Create a socket object
patil = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
patil.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# socket.AF_INET: it uses IPv4
# socket.SOCK_STREAM: it uses TCP

# Get the host and port from user input
host = input("Enter the host (e.g., 127.0.0.1): ")
port = int(input("Enter the port (e.g., 8888): "))

# Bind the socket to a public host, and a port
patil.bind((host, port))
print("listening")

# Become a server socket
patil.listen(1)

# Accept connections from outside
kiran, addr = patil.accept()
print("connected to", addr)

# Send and receive data
while True:
    # Prompt for user input
    cmd = input("$ ")
    # Send command to client
    kiran.send(cmd.encode())
    # Check for exit command
    if cmd == "exit":
        break
    # Receive output from client and print
    output = kiran.recv(1024).decode()
    print(output)

# Close the connection
kiran.close()
patil.close()
