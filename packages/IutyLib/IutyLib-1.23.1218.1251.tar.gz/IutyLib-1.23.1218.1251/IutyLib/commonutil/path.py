import os,sys

def getRoot(key,prefer):
    rtn = "C:\\"
    if sys.platform != "win32":
        rtn = "/"
    
    if os.path.exists(prefer):
        rtn = prefer
    
    ev = os.environ.get(key)
    if os.path.exists(ev):
        rtn = ev
    return rtn
    

def getAppRoot():
    return getRoot("AppRoot","D:\\") if sys.platform == "win32" else getRoot("AppRoot","/srv/")

def getDataRoot():
    return getRoot("DataRoot","E:\\") if sys.platform == "win32" else getRoot("DataRoot","/dat/")



if __name__ == "__main__":
    print(getAppRoot())
    print(getDataRoot())