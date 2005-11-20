from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
import time, os

class Test(Protocol):
    def connectionMade(self):
        self.starttime = time.time()
        self.lengthreceived = 0
        
    def dataReceived(self, data):
        if " ".join(data.split()[-2:]) != "TEST END":
            self.lengthreceived += len(data)
            self.transport.write(data)
        else:
            self.endtime = time.time()
            self.duration = self.endtime - self.starttime
            self.speed = self.lengthreceived/self.duration
            self.transport.write("##")
            self.transport.write(str(self.speed))


def main():
    fact = Factory()
    fact.protocol = Test
    reactor.listenTCP(57234, fact)
    reactor.run()

if __name__ == '__main__':
    main()