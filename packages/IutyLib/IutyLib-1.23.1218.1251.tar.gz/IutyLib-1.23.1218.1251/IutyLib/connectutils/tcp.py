import socket
import threading


class TcpClient:
    IP = "127.0.0.1"
    Port = 2600
    
    def __init__(self):
        self._socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.OnEvent = []
        self._running = False
        pass
    
    
    def doReceive(self):
        while self._running:
           
            try:
                rcv = self._socket.recv(1024)
                
                if not rcv:
                    #close
                    self.close()
                    break
                #receive
                rcv = rcv.decode("gbk")
                for e in self.OnEvent:
                    try:
                        e(self,"receive",rcv)
                    except:
                        pass
            except socket.timeout:
                pass
        pass
    
    def startReceive(self,tout = 1):
        
        self._socket.settimeout(tout)
        thx = threading.Thread(target=self.doReceive)
        thx.daemon = True
        self._running = True
        thx.start()
        
        pass
    
    def send(self,msg):
        try:
            self._socket.send(msg.encode('gbk'))
        except:
            pass
    
    def connect(self):
        self._socket.connect((self.IP,self.Port))
        pass
    
    def close(self):
        self._running = False
        self._socket.close()
        for e in self.OnEvent:
            try:
                e(self,"closed",[])
            except:
                
                pass
        pass
    pass

class TcpService:
    IP = "0.0.0.0"
    Port = 2600
    MaxConnection = 20
    _running = False
    
    
    def __init__(self):
        self.Connections = []
        self._socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        self.OnEvent = []
        pass
    
    def isConnected(self):
        return self._running
    
    def handleClientsEvent(self,sender,msg,args):
        if msg == "closed":
            self.Connections.remove(sender)
        
        for e in self.OnEvent:
            try:
                e(sender,msg,args)
            except:
                pass
        
        pass
        
    
    def doConnect(self):
        try:
            self._socket.bind((self.IP,self.Port))
            self._socket.listen()
            self._running = True
            while self._running:
                con,ip = self._socket.accept()
                tcp = TcpClient()
                tcp.IP = ip[0]
                tcp.Port = ip[1]
                tcp._socket = con
                tcp.OnEvent.append(self.handleClientsEvent)
                
                self.Connections.append(tcp)
                tcp.startReceive()
                for e in self.OnEvent:
                    try:
                        e(self,"connected",ip)
                    except Exception as err:
                        print(err)
                        pass
        except OSError as oerr:
            pass
        pass
    
    def connect(self):
        if not self._running:
            thx = threading.Thread(target=self.doConnect)
            thx.daemon = True
            thx.start()
        pass
    
    def send(self,msg):
        for c in self.Connections:
            c.send(msg)
        pass
    
    def close(self):
        if self._running:
            self._socket.close()
            
            for t in self.Connections:
                t.close()
            self.Connections.clear()
        
        pass


if __name__ == "__main__":
    def handleConnect(sender,etype,ip):
        print("{}:{} is connected".format(ip[0],ip[1]))
        
        if len(sender.Connections) > 2:
            sender.close()
    
    #ss.accept()
    
    #c = TcpClient()
    s = TcpService()
    s.OnEvent.append(handleConnect)
    #c.connect()
    
    s.connect()
    input()