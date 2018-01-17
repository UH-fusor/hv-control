# hv-control

The power supplies from Technix-HV can be controlled via RS232 bus
through a simple ASCII based protocol.  The aim of the hv-control
project is to implement a Python3 control library for the Technix-HV
SR series.

The dependencies of the library are tried to keep simple.  Currently
only the pyserial module is needed, the versions used for testing are
pySerial v3.2.1 from Debian python3-serial package v3.2.1-1 and v3.4
from PyPi.
