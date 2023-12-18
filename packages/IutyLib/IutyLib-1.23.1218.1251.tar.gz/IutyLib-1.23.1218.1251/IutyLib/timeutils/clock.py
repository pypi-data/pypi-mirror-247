import time
import threading
import os


class CycleClock:
    
    def __init__(self,period = 1):
        self._start = time.time()
        self._period = period
        self.OnEvent = []
        self._running = False
        pass
    
    def isRunning(self):
        return _running
    
    def doClock(self):
        
        while self._running:
            
            now = time.time() 
            dlt = now- self._start
            #print(now)
            if dlt > self._period:
                self._start = now
                for e in self.OnEvent:
                    try:
                        e(self,"cycle",[now])
                    except:
                        pass
        pass
        
    
    def start(self):
        if not self._running:
            self._running = True
            
            thx = threading.Thread(target=self.doClock)
            thx.daemon = True
            thx.start()
        pass
    
    def stop(self):
        self._running = False
        
    
    pass


if __name__ == "__main__":
    
    def handleClock(sender,msg,args):
    
        print(args[0])
    
    
    cc = CycleClock()
    cc.OnEvent.append(handleClock)
    cc.start()
    time.sleep(5)
    
    print("执行完成")
    