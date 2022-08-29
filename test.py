from contextlib import suppress
from time import sleep
from HP_6626A_VISA import *
        

visa_rm = pyvisa.ResourceManager()

phy_sup1 = HP_6626A_VISA(visa_rm, f"GPIB0::{3}::INSTR")

psu = phy_sup1.ch1

print(f"Supply at '{phy_sup1.visa_inst}' is '{phy_sup1.identify()}'")

psu.setVoltage(1)
psu.setCurrent(.03)
psu.setState(1)

print(f"voltage set point: {psu.getVoltageSetpoint()}")
print(f"current set point: {psu.getCurrentSetpoint()}")
print(f"Actual Voltage: {psu.getVoltage():0.3f}V")
print(f"Actual Current: {psu.getCurrent()*1000:0.1f}mA")
print(f"Actual Power: {psu.getPower()*1000.0:0.1f}mW")

psu.setState(False)
