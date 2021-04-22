class SongSource:
    def __init__(self, Filename_, IpAddress_, Port_):
        self.Filename_ = Filename_
        self.IpAddress_ = IpAddress_
        self.Port_ = Port_

    def Filename(self):
        return self.Filename_

    def IpAddress(self):
        return self.IpAddress_

    def Port(self):
        return self.Port_

    def __eq__(self, Other):
        return (self.Filename_ == Other.Filename()) and (self.IpAddress_ == Other.IpAddress()) and (self.Port == Other.port())

    def __str__(self):
        return "Filename: " + self.Filename_ + "; Ip address: " + self.IpAddress_ + "; Port number: " + self.Port_ + ";"