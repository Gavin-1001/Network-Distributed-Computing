import socket
import sys
import json
import hashlib

class Client:
    def __init__(self):
        self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ServerAddress = ('localhost', 10000)

        self.Socket.connect(self.ServerAddress)
        self.TestConnection()

    def Start(self):
        try:
            while True:
                Input = input("Enter a command: ")
                if "sendfile" in Input:
                    Filename = input("Enter the name of the file: ")

                    with open("Output/" + Filename, mode = "rb") as file:
                        Content = file.read()
                        print(len(Content))

                        self.Socket.sendall(Content)
                        continue
                if "hash" in Input:
                    Input = self.ProcessHash()
            
                self.Socket.sendall(Input.encode())

                Response = json.loads(self.Socket.recv(1000).decode())

                if(Response["status"] == "OK"):
                    print(Response["message"])
                else:
                    print(Response["error"])
        finally:
            self.Socket.close()

    def ProcessHash(self):
        print("Message will be sent with a hash;")
        Command = input("Enter a command: ")
        Hash = hashlib.sha224(Command.encode()).hexdigest()

        Command += "-" + Hash

        return Command

    def TestConnection(self):
        self.Socket.sendall("[PING]".encode())
            
        Response = json.loads(self.Socket.recv(1000).decode())

        if(Response["status"] == "OK"):
            print(Response["message"])
            return
        else:
            sys.exit("Failed to connect to the server")

Client_ = Client()
Client_.Start()

                


