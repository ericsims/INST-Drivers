import math
import pyvisa

from PowerSupply import PowerSupply, psu_mode 
from Instrument import *



class _HP_6626A_VISA_Channel(PowerSupply):
    def __init__(self, visa_inst, channel):
        super().__init__()
        self.visa_inst = visa_inst
        self.channel = channel
        self.name_str = "HP 6626A"

    def identify(self):
        super().identify(implemented=True)
        return self.visa_inst.query("ID?").strip()

    def reset(self):
        super().reset(implemented=True)
        return self.visa_inst.write("CLR")

    def setState(self, state, validate_setpoint=True):
        super().setState(state, implemented=True)
        self.visa_inst.write(f"OUT {self.channel:d} {int(state == True)}")
        if validate_setpoint:
            meas = self.getState()
            if state != meas:
                print(f"Expected supply output state to be {state}, but read back {meas}!")
                raise Exception('failed to set output state!')

    def getState(self):
        super().getState(implemented=True)
        return self.visa_inst.query(f"OUT? {self.channel}").strip() == '1'

    def setCurrent(self, current, validate_setpoint=True, validate_actual=False):
        super().setCurrent(current, implemented=True)
        self.visa_inst.write(f"IRSET {self.channel:d},{current:0.6f}")
        self.visa_inst.write(f"ISET {self.channel:d},{current:0.6f}")
        if validate_setpoint:
            meas = self.getCurrentSetpoint()
            if not math.isclose(meas, current, abs_tol=1e-2):
                print(f"Expected supply current set point to be at {current}A, but read back {meas}A!")
                raise Exception('failed to set current!')
        if validate_actual:
            meas = self.getCurrent()
            if not math.isclose(meas, current, abs_tol=1e-2):
                print(f"Expected supply current to equal {current}A, but read back {meas}A!")
                raise Exception('current out of expected range!')
        # print(f"Current set at {current} Amps on channel {self.channel} on {self.name_str}")

    def setVoltage(self, voltage, validate_setpoint=True, validate_actual=False):
        super().setVoltage(voltage, implemented=True)
        self.visa_inst.write(f"VRSET {self.channel:d},{voltage:0.6f}")
        self.visa_inst.write(f"VSET {self.channel:d},{voltage:0.6f}")
        if validate_setpoint:
            meas = self.getVoltageSetpoint()
            if not math.isclose(meas, voltage, abs_tol=1e-2):
                print(f"Expected supply voltage set point to be at {voltage}V, but read back {meas}V!")
                raise Exception('failed to set voltage!')
        if validate_actual:
            meas = self.getVoltage()
            if not math.isclose(meas, voltage, abs_tol=1e-2):
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

    def getStatus(self):
        super().getStatus(implemented=True)
        stat = int(self.visa_inst.query(f"STS? {self.channel}"))
        if stat ==  0:
            return psu_mode.OFF
        elif stat == 1:
            return psu_mode.CV
        elif stat == 2:
            return psu_mode.CC
        else:
            return psu_mode.FAULT


class HP_6626A_VISA():
    def __init__(self, visa_inst):
        self.visa_inst = visa_inst
        
        self.ch1=_HP_6626A_VISA_Channel(self.visa_inst, 1)
        self.ch1.capabilites['voltage_control']     = True
        self.ch1.capabilites['min_voltage']         = 0
        self.ch1.capabilites['max_voltage']         = 50 # true limit is 50.5
        self.ch1.capabilites['current_control']     = True
        self.ch1.capabilites['min_current']         = 0
        self.ch1.capabilites['max_current']         = 0.50 # true limit is 0.515
        self.ch1.capabilites['max_power']           = 25
        
        self.ch2=_HP_6626A_VISA_Channel(self.visa_inst, 2)
        self.ch2.capabilites['voltage_control']     = True
        self.ch2.capabilites['min_voltage']         = 0
        self.ch2.capabilites['max_voltage']         = 50 # true limit is 50.5
        self.ch2.capabilites['current_control']     = True
        self.ch2.capabilites['min_current']         = 0
        self.ch2.capabilites['max_current']         = 0.50 # true limit is 0.515
        self.ch2.capabilites['max_power']           = 25

        self.ch3=_HP_6626A_VISA_Channel(self.visa_inst, 3)
        self.ch3.capabilites['voltage_control']     = True
        self.ch3.capabilites['min_voltage']         = 0
        self.ch3.capabilites['max_voltage']         = 50 # true limit is 50.5
        self.ch3.capabilites['current_control']     = True
        self.ch3.capabilites['min_current']         = 0
        self.ch3.capabilites['max_current']         = 2 # true limit is 2.06
        self.ch3.capabilites['max_power']           = 50

        self.ch4=_HP_6626A_VISA_Channel(self.visa_inst, 4)
        self.ch4.capabilites['voltage_control']     = True
        self.ch4.capabilites['min_voltage']         = 0
        self.ch4.capabilites['max_voltage']         = 50 # true limit is 50.5
        self.ch4.capabilites['current_control']     = True
        self.ch4.capabilites['min_current']         = 0
        self.ch4.capabilites['max_current']         = 2 # true limit is 2.06
        self.ch4.capabilites['max_power']           = 50

    def identify(self):
        return self.visa_inst.query("ID?").strip()