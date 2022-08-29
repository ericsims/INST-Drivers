import math
import pyvisa

from PowerSupply import PowerSupply 
from Instrument import *



class _HP_6626A_VISA_Channel(PowerSupply):
    def __init__(self, visa_inst, channel):
        super().__init__()
        self.visa_inst = visa_inst
        self.channel = channel
        self.name_str = "HP 6626A"

    def identify(self):
        super().identify(implemented=True)
        self.visa_inst.write("ID?")
        return self.visa_inst.read().strip()

    def setState(self, state):
        super().setState(state, implemented=True)
        self.visa_inst.write(f"OUT {self.channel:d} {int(state == True)}")

    def setCurrent(self, current, validate_setpoint=True, validate_actual=False):
        super().setCurrent(current, implemented=True)
        self.visa_inst.write(f"IRSET {self.channel:d},{current:0.6f}")
        self.visa_inst.write(f"ISET {self.channel:d},{current:0.6f}")
        if validate_setpoint:
            meas = self.getCurrentSetpoint()
            if not math.isclose(meas, current, rel_tol=1e-2):
                print(f"Expected supply current set point to be at {current}A, but read back {meas}A!")
                raise Exception('failed to set current!')
        if validate_actual:
            meas = self.getCurrent()
            if not math.isclose(meas, current, rel_tol=1e-2):
                print(f"Expected supply current to equal {current}A, but read back {meas}A!")
                raise Exception('current out of expected range!')
        # print(f"Current set at {current} Amps on channel {self.channel} on {self.name_str}")

    def setVoltage(self, voltage, validate_setpoint=True, validate_actual=False):
        super().setVoltage(voltage, implemented=True)
        self.visa_inst.write(f"VRSET {self.channel:d},{voltage:0.6f}")
        self.visa_inst.write(f"VSET {self.channel:d},{voltage:0.6f}")
        if validate_setpoint:
            meas = self.getVoltageSetpoint()
            if not math.isclose(meas, voltage, rel_tol=1e-2):
                print(f"Expected supply voltage set point to be at {voltage}V, but read back {meas}V!")
                raise Exception('failed to set voltage!')
        if validate_actual:
            meas = self.getVoltage()
            if not math.isclose(meas, voltage, rel_tol=1e-2):
                print(f"Expected supply voltage to equal {voltage}V, but read back {meas}V!")
                raise Exception('voltage out of expected range!')
        # print(f"Voltage set at {voltage} Volts on channel {self.channel} on {self.name_str}")

    def getVoltage(self):
        super().getVoltage(implemented=True)
        return float(self.visa_inst.query(f"VOUT? {self.channel:d}"))

    def getVoltageSetpoint(self):
        super().getVoltageSetpoint(implemented=True)
        return float(self.visa_inst.query(f"VSET? {self.channel:d}"))

    def getCurrent(self):
        super().getCurrent(implemented=True)
        return float(self.visa_inst.query(f"IOUT? {self.channel:d}"))

    def getCurrentSetpoint(self):
        super().getCurrentSetpoint(implemented=True)
        return float(self.visa_inst.query(f"ISET? {self.channel:d}"))

    def getPower(self):
        super().getPower(implemented=True)
        return float(self.getVoltage()*self.getCurrent())

class HP_6626A_VISA():
    def __init__(self, visa_rm, visa_address_str):
        self.visa_rm = visa_rm
        self.visa_inst = self.visa_rm.open_resource(visa_address_str)
        
        self.ch1=_HP_6626A_VISA_Channel(self.visa_inst, 1)
        self.ch1.capabilites['voltage_control']     = True
        self.ch1.capabilites['min_voltage']         = 0
        self.ch1.capabilites['max_voltage']         = 50.5
        self.ch1.capabilites['current_control']     = True
        self.ch1.capabilites['min_current']         = 0
        self.ch1.capabilites['max_current']         = 0.515
        self.ch1.capabilites['max_power']           = 50.5*0.515
        
        self.ch2=_HP_6626A_VISA_Channel(self.visa_inst, 2)
        self.ch2.capabilites['voltage_control']     = True
        self.ch2.capabilites['min_voltage']         = 0
        self.ch2.capabilites['max_voltage']         = 50.5
        self.ch2.capabilites['current_control']     = True
        self.ch2.capabilites['min_current']         = 0
        self.ch2.capabilites['max_current']         = 0.515
        self.ch2.capabilites['max_power']           = 50.5*0.515

        self.ch3=_HP_6626A_VISA_Channel(self.visa_inst, 3)
        self.ch3.capabilites['voltage_control']     = True
        self.ch3.capabilites['min_voltage']         = 0
        self.ch3.capabilites['max_voltage']         = 50.5
        self.ch3.capabilites['current_control']     = True
        self.ch3.capabilites['min_current']         = 0
        self.ch3.capabilites['max_current']         = 2.060
        self.ch3.capabilites['max_power']           = 50.5*2.060

        self.ch4=_HP_6626A_VISA_Channel(self.visa_inst, 4)
        self.ch4.capabilites['voltage_control']     = True
        self.ch4.capabilites['min_voltage']         = 0
        self.ch4.capabilites['max_voltage']         = 50.5
        self.ch4.capabilites['current_control']     = True
        self.ch4.capabilites['min_current']         = 0
        self.ch4.capabilites['max_current']         = 2.060
        self.ch4.capabilites['max_power']           = 50.5*2.060

    def identify(self):
        self.visa_inst.write("ID?")
        return self.visa_inst.read().strip()