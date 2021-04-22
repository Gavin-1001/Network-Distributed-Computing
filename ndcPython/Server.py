from fsplit.filesplit import FileSplit
from functools import singledispatch

import socket
import sys
import json
import hashlib

import SongTracker

class Server:
    def __init__(self):
        self.Tracker = SongTracker.SongTracker()

        self.ServerAddress = ('localhost', 10000)
        self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Socket.bind(self.ServerAddress)
        self.Socket.listen(1)

        fs = FileSplit(file = "Output/samplefile.mp3", splitsize = 50000, output_dir = 'Temp/samplefile')
        fs.split()

        self.Start()

    def Start(self):
        while True:
            Connection, ClientAddress = self.Socket.accept()
            try:
                while True:
                    Data = Connection.recv(1000)
                    try:
                        Data = Data.decode()
                        self.ProcessCommand(Data, Connection)
                    except (UnicodeDecodeError, AttributeError):
                        self.ProcessFile(Data, Connection)
            finally:
                Connection.close()

    def ProcessFile(self, Data, Connection):
        Buffer = bytearray()

        while len(Data) > 0:
            Buffer += Data
            Data = Connection.recv(1000)

            try:
                Data = Data.decode()
                self.ProcessCommand(Data, Connection)
                return
            except (UnicodeDecodeError, AttributeError):
                with open("Downloads/file.mp3", "wb+") as File:
                    File.write(Buffer)


    def ProcessCommand(self, Command, Connection):
        if "[" and "]" in Command:
            if "]-" in Command:
                if not self.IsValidHash(Command):
                    Connection.sendall(json.dumps({ "status" : "FAILURE", "error": "Hash of the command does not match" }).encode())
                    return

            Command = Command.replace("[", "")
            Command = Command.replace("]", "")

            if "SONGFILENAME" in Command:
                self.AddSong(Command.split('-'))
                Connection.sendall(json.dumps({ "status" : "OK", "message" : "Song added successfully" }).encode())
            elif "LISTALL" in Command:
                Connection.sendall(json.dumps({ "status" : "OK", "message" : "Songs available: \n" + self.PrepareSongString() }).encode())
            elif "CLEARALL" in Command:
                self.RemoveSongsForClient(Command.split('-')[1])
                Connection.sendall(json.dumps({ "status" : "OK", "message" : "The songs were removed successfully" }).encode())
            elif "PING" in Command:
                Connection.sendall(json.dumps({ "status" : "OK", "message" : "Connected successfully" }).encode())
            else:
                Connection.sendall(json.dumps({ "status" : "FAILURE", "error" : "Invalid command" }).encode())
        else:
            Connection.sendall(json.dumps({ "status" : "FAILURE", "error" : "Invalid command format: [ and ] expected" }).encode())

    def AddSong(self, Arguments):
        FileName = Arguments[1]
        IpAddress = Arguments[2]
        PortNumber = Arguments[3]

        self.Tracker.AddSong(FileName, IpAddress, PortNumber)

    def PrepareSongString(self):
        String = ""

        for Song in self.Tracker.GetList():
            String += Song.Filename() + "\n"

        return String

    def RemoveSongsForClient(self, ClientIpAddress):
        self.Tracker.RemoveSongsForClient(ClientIpAddress)

    def IsValidHash(self, Command):
        Values = Command.split("]")
        
        CommandBody = str(Values[0] + "]")
        HashBody = str(Values[1])[1:]

        print(HashBody)

        return HashBody == hashlib.sha224(CommandBody.encode()).hexdigest()

Server()

