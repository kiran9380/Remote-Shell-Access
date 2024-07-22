import socket

def handle_client(kiran):
    """Handle commands and interactions with the client."""
    try:
        while True:
            # Prompt for user input
            cmd = input("$ ")
            if cmd == "exit":
                kiran.send(cmd.encode())
                break

            # Send command to client
            kiran.send(cmd.encode())
            
            # Receive and print the output from client
            kiran.settimeout(10)  # Set a timeout for receiving data
            try:
                output = kiran.recv(4096).decode()  # Adjust buffer size as needed
                if output:
                    print(output)
                else:
                    print("Client disconnected unexpectedly.")
                    break
            except socket.timeout:
                print("No response from client, retrying...")
    except BrokenPipeError:
        print("Client disconnected unexpectedly.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    # Create a socket object
    patil = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    patil.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Get the host and port from user input
    host = input("Enter the host (e.g., 127.0.0.1): ")
    port = int(input("Enter the port (e.g., 8888): "))

    # Bind the socket to a public host, and a port
    patil.bind((host, port))
    print("Listening...")

    # Become a server socket
    patil.listen(1)

    while True:
        try:
            # Accept connections from outside
            kiran, addr = patil.accept()
            print("Connected to", addr)
            handle_client(kiran)
        except KeyboardInterrupt:
            print("Server interrupted and closing...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Ensure proper cleanup
            if 'kiran' in locals():
                kiran.close()
            patil.close()

if __name__ == "__main__":
    main()
