#!/usr/bin/env python3
"""
Module for controlling Technix SR high voltage PSU via serial bus
"""

import configparser

configfile = 'hv.conf'
cfg = configparser.ConfigParser()
cfg.read(configfile)

MAX_VOLTAGE   = float(cfg.get('default', 'MAX_VOLTAGE'  ))
MAX_CURRENT   = float(cfg.get('default', 'MAX_CURRENT'  ))
VOLTAGE_LIMIT = float(cfg.get('default', 'VOLTAGE_LIMIT'))
CURRENT_LIMIT = float(cfg.get('default', 'CURRENT_LIMIT'))

def set_voltage(U):
    pass

def set_current(I):
    pass

def get_status():
    pass

def get_voltage():
    pass

def get_current():
    pass

def inc_voltage(dU):
    pass

def inc_current(dI):
    pass

def hv_on():
    pass

def hv_off():
    pass

def get_voltagelimit():
    return VOLTAGE_LIMIT

def get_currentlimit():
    return CURRENT_LIMIT

def get_maxvoltage():
    return MAX_VOLTAGE

def get_maxcurrent():
    return MAX_CURRENT



def __send_command(command):
    """Checks whether the 'command' is valid, and that the resulting
    voltage and current values will still be within the allowed
    limits, and sends the command to the serial bus if everything is
    Ok.  Retuns a tuple (voltage, current).
    """
    
    print(command)
    return (0.0, 0.0)


if __name__=='__main__':
    __send_command("Testing 1-2-3")

