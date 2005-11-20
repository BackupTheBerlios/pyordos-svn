# -*- coding: UTF-8 -*-
import os
try:
    import psyco
    psyco.full
except:
    print "psyco unavailable"


def getCpuPerf():
    import sha, time
    
    tmp = sha.new()
    deb = time.time()
    for nb_char in range(256**2):
        for inc in range(256):
            tmp.update(chr(inc))
    fin = time.time()
    return int(10**4/(fin - deb))

def getMemAmount():
    try:
        import win32com.client
        strComputer = "."
        objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
        objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2")
        colItems = objSWbemServices.ExecQuery("Select * from Win32_PhysicalMemory")
        amount = 0
        for objItem in colItems:
            amount += int(objItem.Capacity)/(1024)
    except ImportError:
        if os.name == "posix":
            meminfo = file("/proc/meminfo", "r")
            for ligne in meminfo:
                if ligne.split(":")[0] == "MemTotal":
                    amount = int(ligne.split()[1])
    return(amount)

def getDiskSpace(storage):
    space = 0
    try:
        import win32com.client
        strComputer = "."
        objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
        objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2")
        colItems = objSWbemServices.ExecQuery("Select * from Win32_LogicalDisk")
        for objItem in colItems:
            if storage.upper() == objItem.DeviceID.upper():
                space = int(objItem.Size)/(1024**2)
            break
    except:
        if os.name == "posix":
            partitions = file("/proc/partitions", "r")
            for ligne in partitions:
                if len(ligne.strip()) > 0:
                    if storage.lower() == ligne.split()[-1]:
                        space = int(ligne.split()[-2])/(1024)
    return(space)
    
def getNetSpeed(host):
    from twisted.internet.protocol import ClientFactory
    from twisted.protocols.basic import LineReceiver
    from twisted.internet import reactor
    import sys, time
    
    class EchoClient(LineReceiver):
        def connectionMade(self):
            self.sizereceived = 0
            self.setRawMode()
            self.sizesent = (1024**2)*10
            self.sendLine(self.sizesent*"A")
            self.sendLine("TEST END")

        def rawDataReceived(self, data):
                tmp = ""
                if data.find("##") != -1:
                    tmp = data.split("##")[-1]
                    data = data.split("##")[0]
                    self.transport.loseConnection()
                self.sizereceived += len(data.strip())
                if tmp != "":
                    return "%0.2f" % (float(tmp)/1024.0)
                    
                
    
    class EchoClientFactory(ClientFactory):
        protocol = EchoClient
    
        def clientConnectionFailed(self, connector, reason):
#            print "Connection failed :", reason
            reactor.stop()
    
        def clientConnectionLost(self, connector, reason):
            reactor.stop()
    
    fact = EchoClientFactory()
    reactor.connectTCP(host, 57234, fact)
    reactor.run()
    

#print getCpuPerf()
print getMemAmount()/(1024)
print getDiskSpace("hda2")
print getDiskSpace("c:")
print getNetSpeed("192.168.1.2")
