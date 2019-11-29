class HostFile:
    def __init__(self, name, user, port, speed, hostname, keywords):
        self.name = name # instance variable unique to each instance
        self.user = user
        self.port = port
        self.speed = speed
        self.hostname = hostname
        self.keywords = keywords

    def getName(self):
        return self.name

    def getUser(self):
        return self.user

    def getKeywords(self):
        return self.keywords