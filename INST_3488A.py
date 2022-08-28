import pyvisa, time

class INST_3488A:
    def __init__(self, Addr):
        self.ADDR = Addr
        self.visa_rm = pyvisa.ResourceManager()
        self.inst = self.visa_rm.open_resource('GPIB0::'+str(self.ADDR)+'::INSTR')

    def identify(self):
        self.inst.write("ID?")
        return self.inst.read()
        
