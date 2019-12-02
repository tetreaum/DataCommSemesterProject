class HostConnection:
    def __init__(self, ip, hostname, fileList, speed, username):
        self.ip = ip  # instance variable unique to each instance
        self.hostname = hostname
        self.fileList = fileList
        self.speed = speed
        self.username = username
