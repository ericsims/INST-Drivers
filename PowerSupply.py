import math, time, warnings
from enum import Enum
import numpy as np
from Instrument import *

class PowerSupply():

    def __init__(self):
        self.capabilites = {
            'voltage_control': False,
            'current_control': False,
            'power_control': False,
            'OVP': False,
            'OCP': False,
            'voltage_slew_rate_control': False,
            'voltage_slew_rate_min': -math.inf,
            'voltage_slew_rate_max': math.inf,
            'min_voltage': -math.inf,
            'max_voltage': math.inf,
            'min_current': -math.inf,
            'max_current': math.inf,
            'min_power': -math.inf,
            'max_power': math.inf
        }

        self.name_str = ""

        self.soft_voltage_range = [-math.inf, math.inf]
        self.soft_current_range = [-math.inf, math.inf]
        self.soft_power_range = [-math.inf, math.inf]

    def identify(self, implemented=False):
        if not implemented:
            raise NotImplementedError

    def reset(self, implemented=False):
        if not implemented:
            raise NotImplementedError

    def setState(self, state, implemented=False):
        if type(state)!=bool:
            if type(state) == int:
                if not (int(state)==0 or int(state)==1):
                    raise TypeError
            else:
                raise TypeError
        if not implemented:
            raise NotImplementedError

    def getState(self, implemented=False):
        if not implemented:
            raise NotImplementedError

    def setVoltage(self, voltage, implemented=False):
        if not self.capabilites['voltage_control']:
             raise ExceededInstrumentCapabilitesError("Voltage control not supported")
        if voltage < self.capabilites['min_voltage'] or voltage > self.capabilites['max_voltage']:
            raise ExceededInstrumentCapabilitesError(f"Voltage setpoint of {voltage}V is out of supply limits of {self.capabilites['min_voltage']}V to {self.capabilites['max_voltage']}V")
        if voltage < self.soft_voltage_range[0] or voltage > self.soft_voltage_range[1]:
            raise ExceededInstrumentSoftLimitError(f"Voltage setpoint of {voltage}V is out soft voltage limits of {self.soft_voltage_range[0]}V to {self.soft_voltage_range[1]}V")
        I = self.getCurrentSetpoint()
        if voltage*I > self.capabilites['max_power']:
            raise ExceededInstrumentCapabilitesError(f"Voltage setpoint of {voltage}V at a current setpoint of {I}A is too high for the rated power of {self.capabilites['max_power']}W")
        # TODO: check that voltage set point is within negative power limit
        if not implemented:
            raise NotImplementedError

    def getVoltage(self, implemented=False):
        if not implemented:
            raise NotImplementedError

    def getVoltageSetpoint(self, implemented=False):
        if not implemented:
            raise NotImplementedError

    def setCurrent(self, current, implemented=False):
        if not self.capabilites['current_control']:
             raise ExceededInstrumentCapabilitesError("Current control not supported")
        if current < self.capabilites['min_current'] or current > self.capabilites['max_current']:
            raise ExceededInstrumentCapabilitesError(f"Current setpoint of {current}A is out of supply limits of {self.capabilites['min_current']}A to {self.capabilites['max_current']}A")
        if current < self.soft_current_range[0] or current > self.soft_current_range[1]:
            raise ExceededInstrumentSoftLimitError(f"Current setpoint of {current}A is out soft current limits of {self.soft_current_range[0]}A to {self.soft_current_range[1]}A")
        V = self.getVoltageSetpoint()
        if current*V > self.capabilites['max_power']:
            raise ExceededInstrumentCapabilitesError(f"Current setpoint of {current}A at a voltage setpoint of {V}V is too high for the rated power of {self.capabilites['max_power']}W")
        # TODO: check that voltage set point is within negative power limit
        if not implemented:
            raise NotImplementedError

    def getCurrent(self, implemented=False):
        if not implemented:
            raise NotImplementedError

    def getCurrentSetpoint(self, implemented=False):
        if not implemented:
            raise NotImplementedError

    def setPower(self, power, implemented=False):
        if not self.capabilites['power_control']:
             raise ExceededInstrumentCapabilitesError("Power control not supported")
        if power < self.capabilites['min_power'] or power > self.capabilites['max_power']:
            raise ExceededInstrumentCapabilitesError(f"Power setpoint of {power}W is out of supply limits of {self.capabilites['min_power']}W to {self.capabilites['max_power']}W")
        if power < self.soft_power_range[0] or power > self.soft_power_range[1]:
            raise ExceededInstrumentSoftLimitError(f"Power setpoint of {power}W is out soft power limits of {self.soft_power_range[0]}W to {self.soft_power_range[1]}W")
        if not implemented:
            raise NotImplementedError
      
    def getPower(self, implemented=False):
        if not implemented:
            raise NotImplementedError

    def getPowerSetpoint(self, implemented=False):
        if not implemented:
            raise NotImplementedError

    def setVoltageSlewRate(self, slew_rate, implemented=False):
        if not self.capabilites['voltage_slew_rate_control']:
             raise ExceededInstrumentCapabilitesError("Voltage slew rate control not supported")
        if slew_rate < self.capabilites['voltage_slew_rate_min'] or voltage > self.capabilites['voltage_slew_rate_max']:
            raise ExceededInstrumentCapabilitesError(f"Voltage slew rate set point of {slew_rate} is out of supply limits of {self.capabilites['voltage_slew_rate_min']} to {self.capabilites['voltage_slew_rate_max']}")
        if not implemented:
            raise NotImplementedError

    def getVoltageSlewRate(self, implemented=False):
        if not implemented:
            raise NotImplementedError

    def getStatus(self, implemented=False):
        if not implemented:
            raise NotImplementedError



    def sw_slewOutput(self, endVoltage, slewRate, startVoltage=None, stepsize=0.1):
        raise Exception("NEED TO FIX THIS FUNCTION TO RESPECT COMMAND TIMING")

        if slewRate < 0:
            raise Exception(f"Slew rate \"{slewRate}\" V/s is not valid. Must be > 0.")
        elif slewRate > 5:
            warnings.warn("Slew rate is > 5 V/s. This will cause the output voltage to be stepped in large steps. Consider a lower slew rate")
        if stepsize <= 0:
            raise Exception("Step size must be > 0")
        if stepsize > 0.25:
            warnings.warn("Step size is > 0.25 s. This will cause the output voltage to be stepped in large steps. Consider a lower step size")

        if startVoltage is not None:
            pass
            # defering validation to the individual set functions 
            # if startVoltage < 0:
            #     raise Exception("Start Voltage \"{}\" is not valid. Voltage set point must be > 0.".format(startVoltage))
            # elif startVoltage > 50.5:
            #     raise Exception("Start Voltage \"{}\" is not valid. Max voltage is 50.5V".format(startVoltage))
        else:
            startVoltage=self.getVoltageSetpoint()
        # defering validation to the individual set functions 
        # if endVoltage < 0:
        #     raise Exception("End Voltage \"{}\" is not valid. Voltage set point must be > 0.".format(endVoltage))
        # elif endVoltage > 50.5:
        #     raise Exception("End Voltage \"{}\" is not valid. Max voltage is 50.5V".format(endVoltage))

        
        if endVoltage < startVoltage:
            stepsize = -stepsize
            
        self.setVoltage(startVoltage)
        start = time.time()
        count = 0
        for V in np.arange(startVoltage, endVoltage, slewRate*stepsize):
            self.setVoltage(V)
            count += 1
            while time.time() < start+(count+1)*stepsize:
                pass

        self.setVoltage(endVoltage)

class psu_mode(Enum):
    OFF = 0
    CV = 1
    CC = 2
    OVP = 3
    OCP = 4
    FAULT = 5