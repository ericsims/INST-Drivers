import pyvisa, time

class INST_8842A:
    def __init__(self, Addr):
        self.ADDR = Addr
        self.visa_rm = pyvisa.ResourceManager()
        self.inst = self.visa_rm.open_resource('GPIB0::'+str(self.ADDR)+'::INSTR')

    def identify(self):
        self.inst.write("*IDN?")
        return self.inst.read()

    def getVoltage(self):
        self.inst.write('F1')
        self.inst.write('R0')
        self.inst.write('S1')
        return float(self.inst.read())
    
        
