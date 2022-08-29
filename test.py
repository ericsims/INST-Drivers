from contextlib import suppress
from time import sleep
from HP_6626A_VISA import *
        

visa_rm = pyvisa.ResourceManager()

phy_sup1 = HP_6626A_VISA(visa_rm, f"GPIB0::{3}::INSTR")

psu = phy_sup1.ch1

def safe_hw():
    print("Safeing HW!")
    psu.setState(False)

print(f"Supply at '{phy_sup1.visa_inst}' is '{phy_sup1.identify()}'")

# check supply can supply 100mA at 10V
assert(psu.capabilites['max_voltage'] >= 10)
assert(psu.capabilites['max_current'] >= 0.1)
assert(psu.capabilites['max_power'] >= 10*0.1)

# set sw limits to protect DUT
psu.soft_voltage_range=[0,10]
psu.soft_current_range=[0,0.1]

try:
    psu.setState(0)
    psu.setVoltage(10)
    psu.setCurrent(.1)
    psu.setState(1)

    print(f"Voltage set point: {psu.getVoltageSetpoint()}")
    print(f"Current set point: {psu.getCurrentSetpoint()}")
    print(f"Actual Voltage: {psu.getVoltage():0.3f}V")
    print(f"Actual Current: {psu.getCurrent()*1000:0.1f}mA")
    print(f"Actual Power: {psu.getPower()*1000.0:0.1f}mW")

    assert(psu.getStatus() == psu_mode.CV)

    sleep(2)


    psu.setState(False)
except Exception as e:
    print("EXCEPTION!!")
    safe_hw()
    raise(e)


