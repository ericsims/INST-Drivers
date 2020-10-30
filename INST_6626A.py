import pyvisa, time

class INST_6626A:
    def __init__(self, Addr):
        self.ADDR = Addr
        self.visa_rm = pyvisa.ResourceManager()
        self.inst = self.visa_rm.open_resource('GPIB0::'+str(self.ADDR)+'::INSTR')

    def identify(self):
        self.inst.write("ID?")
        return self.inst.read()

    def enable(self, channel):
        if channel < 1 or channel > 4:
            raise Exception("Channel {} is not valid. Channel must be 1-4.".format(channel))
        self.inst.write("OUT {:d} 1".format(channel))

    def disable(self, channel):
        if channel < 1 or channel > 4:
            raise Exception("Channel {} is not valid. Channel must be 1-4.".format(channel))
        self.inst.write("OUT {:d} 0".format(channel))

    def setVoltage(self, channel, voltage):
        if channel < 1 or channel > 4:
            raise Exception("Channel {} is not valid. Channel must be 1-4.".format(channel))
        if voltage < 0:
            raise Exception("Voltage \"{}\" is not valid. Voltage set point must be > 0.".format(voltage))
        elif voltage > 50.5:
            raise Exception("Vurrent \"{}\" is not valid. Max voltage is 50.5V".format(voltage))
        self.inst.write("VRSET {:d},{:0.6f}".format(channel, voltage))
        self.inst.write("VSET {:d},{:0.6f}".format(channel, voltage))

    def setCurrent(self, channel, current):
        if channel < 1 or channel > 4:
            raise Exception("Channel {} is not valid. Channel must be 1-4.".format(channel))
        if current < 0:
            raise Exception("Current \"{}\" is not valid. Current set point must be > 0.".format(current))
        elif (channel == 1 or channel == 2) and current > 0.515:
            raise Exception("Current \"{}\" is not valid. Max current for channels 1 and 2 is 0.515A".format(current))
        elif (channel == 3 or channel == 4) and current > 2.060:
            raise Exception("Current \"{}\" is not valid. Max current for channels 1 and 2 is 2.060A".format(current))           
        self.inst.write("IRSET {:d},{:0.6f}".format(channel, current))
        self.inst.write("ISET {:d},{:0.6f}".format(channel, current))
    
        
