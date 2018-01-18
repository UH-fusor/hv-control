# hvcontrol

The power supplies from Technix http://www.technix-hv.com can be
controlled via RS232 bus using a simple ASCII based protocol.  The aim
of the hvcontrol project is to implement a Python3 control library for
the Technix SR 5kW to 10kW series
http://www.technix-hv.com/technix/products/HV-generators/sr-5000-to-10000-watts.
We are testing the implementation with Technix SR100kV-5kW, which has
negative polarity (i.e. the voltage range from ground potential 0.0 V
down to -100.0 kV).

The dependencies of the library are tried to keep simple.  Currently,
besides of the standard library, only the pyserial module is needed,
the versions used for testing are pySerial v3.2.1 from Debian
python3-serial package v3.2.1-1 and v3.4 from PyPi.  Developers are
using both Python v3.5 and v3.6.
