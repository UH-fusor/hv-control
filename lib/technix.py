#!/usr/bin/env python3
"""
Module for controlling Technix SR high voltage PSU via serial bus
"""

import configparser
import serial
import time

configfile = 'hv.conf'
cfg = configparser.ConfigParser()
cfg.read(configfile)

# In config file, the voltages are given in kV for convenience.  But
# the module uses V internally.  Therefore multiplying voltages by
# 1000.0.  The currents are given and used in mA.
MAX_VOLTAGE   = float( cfg.get('voltage', 'MAX_VOLTAGE'   )) * 1000.0
MAX_CURRENT   = float( cfg.get('current', 'MAX_CURRENT'   ))
VOLTAGE_LIMIT = float( cfg.get('voltage', 'VOLTAGE_LIMIT' )) * 1000.0
CURRENT_LIMIT = float( cfg.get('current', 'CURRENT_LIMIT' ))
SER_PORT      =        cfg.get('serial',  'port'          )
SER_BAUDRATE  = int(   cfg.get('serial',  'baudrate'      ))
SER_PARITY    =        cfg.get('serial',  'parity'        )
SER_STOPBITS  =        cfg.get('serial',  'stopbits'      )
SER_BYTESIZE  = int(   cfg.get('serial',  'bytesize'      ))
SER_TIMEOUT   =        cfg.get('serial',  'timeout'       )
SER_RTSCTS    =        cfg.get('serial',  'rtscts'        )
SER_DSRDTR    =        cfg.get('serial',  'dsrdtr'        )
SER_XONXOFF   =        cfg.get('serial',  'xonxoff'       )

# The serial protocol uses 12-bit unsigned integer for setting the
# voltage and current.
INT_MAX=2**12-1

#The minimum steps are (in V and mA):
delta_U = MAX_VOLTAGE/INT_MAX
delta_I = MAX_CURRENT/INT_MAX

#
# Global variables:
#

# Book keeping the present values of U and I.
U_counted = 0.0
I_counted = 0.0

# High voltage on or off
HV=False

# The connection object
serconnection=None

def safehalt(message):
    """Prints 'message', turns off the HV and exits."""
    print(message)
    if serconnection!=None:
        # Here only, if the connection has already been opened.
        print("Turning off the HV output.")
        set_voltage(0.0)
        set_current(0.0)
        hv_off()
        serconnection.close()
    print("Stopping!")
    import sys
    sys.exit(1)

def istrue(boolean):
    """Tries to interpret a string as True or False.  Halts if fails, or
    if called with an object which doesn't have upper() attribute."""
    try:
        if boolean.upper()=='TRUE' or boolean.upper()=='YES' or \
           boolean.upper()=='Y' or boolean=='1':
            return True
        elif boolean.upper()=='FALSE' or boolean.upper()=='NO' or \
             boolean.upper()=='F' or boolean=='0':
            return False
        else:
            safehalt("Don't know how to interpret boolean " + str(boolean))
    except AttributeError:
        safehalt("technix.istrue(): boolean '" + str(boolean) + "' seems too problematic for me.")

def init_serial():
    """Initializes the serial port and returns the connection object, if
    success.  Halts otherwise.
    """

    # If there is too much garbage in the configfile, either
    # ValueError or KeyError will be thrown before the serial.Serial()
    # is called.

    global serconnection

    paritydict = {
        'N' : serial.PARITY_NONE,
        'E' : serial.PARITY_EVEN,
        'O' : serial.PARITY_ODD,
        'S' : serial.PARITY_SPACE,
        'M' : serial.PARITY_MARK }
    try:
        parity = paritydict[SER_PARITY.upper()]
    except KeyError:
        safehalt("Unknown parity in the config file: " + str(SER_PARITY))

    stopbitsdict = {
        '1'   : serial.STOPBITS_ONE,
        '1.5' : serial.STOPBITS_ONE_POINT_FIVE,
        '2'   : serial.STOPBITS_TWO }
    try:
        stopbits = stopbitsdict[SER_STOPBITS]
    except KeyError:
        safehalt("Unknown stopbits in the config file: " + str(SER_STOPBITS))

    bytesizedict = {
        5 : serial.FIVEBITS,
        6 : serial.SIXBITS,
        7 : serial.SEVENBITS,
        8 : serial.EIGHTBITS }
    try:
        bytesize = bytesizedict[SER_BYTESIZE]
    except KeyError:
        safehalt("Unknown stopbits in the config file: " + str(SER_BYTESIZE))

    if SER_TIMEOUT.upper()=='NONE':
        timeout=None
    else:
        try:
            timeout=float(SER_TIMEOUT)
        except ValueError:
            safehalt("Unknown timeout in the config file: " + str(SER_TIMEOUT))

    rtscts  = istrue(SER_RTSCTS)
    dsrdtr  = istrue(SER_DSRDTR)
    xonxoff = istrue(SER_XONXOFF)

    # Exclusive was introduced in pySerial v3.3
    if float(serial.VERSION)<3.3:
        serconnection = serial.Serial(port=SER_PORT,
                                      baudrate=SER_BAUDRATE, parity=parity,
                                      stopbits=stopbits, bytesize=bytesize,
                                      timeout=timeout, rtscts=rtscts,
                                      dsrdtr=dsrdtr, xonxoff=xonxoff)
    else:
        serconnection = serial.Serial(port=SER_PORT,
                                      baudrate=SER_BAUDRATE, parity=parity,
                                      stopbits=stopbits, bytesize=bytesize,
                                      timeout=timeout, rtscts=rtscts,
                                      dsrdtr=dsrdtr, xonxoff=xonxoff,
                                      exclusive=True)
    return serconnection

def set_voltage(U):
    """Tries to set the voltage as U (given in volts).
    """
    global U_counted
    # Using only 'int' rounds always towards zero.  By rounding first,
    # we will have the closest value instead.
    int_U = int(round(U/delta_U))
    if int_U<0: int_U=0
    if int_U>INT_MAX: int_U=INT_MAX
    command = 'd1,'+str(int_U)
    U_counted = int_U * delta_U
    return __send_command(command)

def set_current(I):
    global I_counted
    # Using only 'int' rounds always towards zero.  By rounding first,
    # we will have the closest value instead.
    int_I = int(round(I/delta_I))
    if int_I<0: int_I=0
    if int_I>INT_MAX: int_I=INT_MAX
    command = 'd2,'+str(int_I)
    I_counted = int_I * delta_I
    return __send_command(command)

def get_status():
    inquiry_result = __send_inquiry('E')
    if inquiry_result:
        return decrypt_the_inquiry(inquiry_result)
    else:
        return False

def get_counted_voltage():
    return U_counted

def get_counted_current():
    return I_counted

def get_measured_voltage():
    return __send_inquiry('a1')

def get_measured_current():
    return __send_inquiry('a2')

def inc_voltage(dU=delta_U):
    U_new = U_counted + dU
    return set_voltage(U_new)

def inc_current(dI=delta_I):
    I_new = I_counted + dI
    return set_current(I_new)

def dec_voltage(dU=delta_U):
    U_new = U_counted - dU
    return set_voltage(U_new)

def dec_current(dI=delta_I):
    I_new = I_counted - dI
    return set_current(I_new)

def hv_on():
    global HV
    __send_command('P5,1')
    time.sleep(0.1) # delay 100ms
    __send_command('P5,0')
    HV=True

def hv_off():
    global HV
    __send_command('P6,1')
    time.sleep(0.1) # delay 100ms
    __send_command('P6,0')
    HV=False

def local_mode():
    return __send_command('P7,1')

def remote_mode():
    return __send_command('P7,0')

def inhibit():
    return __send_command('P8,1')

def idle():
    return __send_command('P8,0')

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
    Ok.  Retuns a tuple (voltage, current) of measured values.
    """
    
    print(command)
    return (0.0, 0.0)

def __send_inquiry(command):
    """Checks whether the 'command' is both valid and such that it will
    not change the output of the PSU.  If true, sends the command and
    returns the result.
    """

    print(command)
    return "The result"

def decrypt_the_inquiry(X):
    """Returns the answer X for instruction E in more user friendly manner.
    """
    print("Sorry, not implemented:", X)


if __name__=='__main__':
    set_voltage(-10.0)
