import serial
import time

class Shutter():
    def __init__(self,COM='COM7',readTime=1):
        self.ins=serial.Serial(port=COM,timeout=readTime)
        self.writeTime=1E-2
        self.readTime=1E-2
        self.setOpenMode(0)
        self.setControlMode(0)
        self.__write('NFT=0000%')
        self.__write('ONT=010%')
        self.__write('OFT=010%')

    # def __del__(self):
    #     self.close()

    def __read(self):
        time.sleep(self.readTime)
        text=''
        c=self.ins.read().decode()
        while(c!='%'):
            text+=c
            c=self.ins.read().decode()
        return text

    def __write(self,cmd):
        self.ins.write(cmd.encode())
        time.sleep(self.writeTime)

    def __query(self,cmd):
        self.__write(cmd)
        return self.__read()

# Basic methods
    def close(self):
        self.setOpenMode(0)
        self.setControlMode(1)
        self.__write('NFT=0000%')
        self.__write('ONT=010%')
        self.__write('OFT=010%')
        self.save()
        self.ins.close()

    def save(self):
        return self.__query('SAVE%')

    def setOpenMode(self,mode=0):
        cmd='NFM={}%'.format(int(bool(mode)))
        self.__write(cmd)

    def setControlMode(self,mode=0):
        cmd='CM={}%'.format(mode)
        self.__write(cmd)

    def setOn(self):
        self.__write('PCO=1%')

    def setOff(self):
        self.__write('PCO=0%')

    def controlMode(self):
        return self.__query('?CM%')

    def setWindowOpen(self,t=1):
        ''''
        ~3ms 误差
        '''
        t-=self.writeTime
        self.setOff()
        self.setOn()
        time.sleep(t)
        self.setOff()
# Basic methods