import SongSource

class SongTracker:
    def __init__(self):
        self.SongList = list()

    def AddSong(self, Filename, IpAddress, PortNumber):
        Song = SongSource.SongSource(Filename, IpAddress, PortNumber)

        if not Song in self.SongList:
            self.SongList.append(Song)

    def GetList(self):
        return self.SongList

    def RemoveSongsForClient(self, IpAddress):
        self.SongList = list(filter(lambda Song: Song.IpAddress() != IpAddress, self.SongList))