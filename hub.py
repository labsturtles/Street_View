
import sys
import serial
import time
usleep = lambda x: time.sleep(x/1000000.0)


datatext="------"
dataicon=11
dataspeed=295
datarpm=263

def openMirror(step=7):
    t=400
    for i in range(0,step,1):
      s.setDTR(False)
      usleep(t)
      s.setDTR(True)
      usleep(20000-t)

def closeMirror():
    t=2100
    while(not s.getDSR()):
      for i in range(0,1,1):
        s.setDTR(False)
        usleep(t)
        s.setDTR(True)
        usleep(20000-t)

    s.setDTR(False)
    usleep(t)
    s.setDTR(True)
    usleep(20000-t)

def endString():
    s.write(serial.to_bytes([0xff,0xff,0xff]))

def writeText(data):
      s.write(b't0.txt=\"')
      s.write(str(data).encode('utf-8'))
      s.write(b'\"')
      endString()

def writeIcon(data):
      s.write(b'p0.pic=')
      s.write(str(data).encode('utf-8'))
      endString()

def writeSpeed(data):
      s.write(b'z0.val=')
      s.write(str(data).encode('utf-8'))
      endString()

def writeRPM(data):
      s.write(b'z1.val=')
      s.write(str(data).encode('utf-8'))
      endString()

def refreshScreen():
      writeSpeed(dataspeed)
      writeRPM(datarpm)
      writeIcon(dataicon)
      writeText(datatext)

def putText(data):
      global datatext
      datatext=data
      refreshScreen()

def putIcon(data):
      global dataicon
      dataicon=data
      refreshScreen()
  
def putSpeed(data):
      global dataspeed
      dataspeed=data
      refreshScreen()

def putRpm(data):
      global datarpm
      datarpm=data
      refreshScreen()

#--------------------------
# Module HUD
#--------------------------
if __name__=='__main__':

  
    try:
        
        print("PUERTO USB")
        #-- Abrir puerto serie
        s = serial.Serial('/dev/ttyUSB0', xonxoff=0, dsrdtr=0, rtscts=0)
        s.setDTR(True)
        usleep(200000)

        if(not s.getDSR()):
            closeMirror()

        openMirror()
        time.sleep(1)


        for i in range(263,95,-1):
           putRpm(i)
           putText(i)

        print("TFT OFF")
        time.sleep(1)
        putSpeed(329)
        putIcon(8)

   

        time.sleep(10)
        closeMirror()


    

        #-- Cerrar puerto
        s.close()
                
      #-- Si hay un error se ignora      
    except:
        print ("NO")
