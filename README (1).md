
# Remote-Shell-Access

This is a Simple Remote-Shell-Access Project. I created this using Python Socket. With this, we can interact with another computer shell




## Usage

- First Run the Techboy_server.py on your host computer(computer-1) and give your host ip addr and port no

```bash
    C:\project>python Techboy_server.py
  	Enter the host (e.g., 127.0.0.1): 192.168.231.58
  	Enter the port (e.g., 8888): 4444
  	listening
```

- After that run kiran_client.py on client computer(computer-2) and give the host computer(computer-1) ip adrr and port no

```bash
     D:\project>python kiran_client.py
 	 connecting....
 	 Enter the server host (e.g., 127.0.0.1): 192.168.231.58
 	 Enter the server port (e.g., 8888): 4444

