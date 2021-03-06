import spidev

spi = spidev.SpiDev()

class Register(object):
    _bits = ()

    def __init__(self, from_int=0, **kwargs):
        for bit in _bits:
            setattr(self, bit, kwargs.get(bit, 0))
        if from_int:
            self.unpack(from_int)

    def pack(self):
        value = 0
        for index, flag in enumerate(self._bits):
            value = value | (getattr(self, flag) << index)
        return value
    
    def unpack(self, value):
        for index, flag_name in enumerate(self._bits):
            setattr(self, flag_name, (value >> index) & 1)

    def __repr__(self):
        desc = '' 
        for flag_name in self._bits:
            desc += "{0}: {1}\n".format(flag_name, getattr(self, flag_name))

        return desc
 
    def __eq__(self, target):
        return self.pack == target

class ConfigRegister(Register):
    _bits = ( "PRIM_RX", "PWR_UP", "CRCO", "EN_CRC", "MASK_MAX_RT", "MASK_TX_DS", "MASK_RX_DR" )

def read_register(register, size=1):
    if register < 0 or register > 31:
        raise Exception("register must be 0 to 31")
    command = 0 | register
    padding = [ 0 ] * size
    return spi.xfer([command] + padding)

def write_register(register, *payload):
    if register < 0 or register > 31:
        raise Exception("register must be 0 to 31")
    command = 0x20 | register

    return spi.xfer([command] + payload)[0]

spi.open(0,0)
status, config = read_register(0)
print "status: %d config: %d" % (status, config)

if status == 14 and config == 8:
    print "Device is powered down. Powering up to PRX mode."
    write_register(0, config | 0x3)
    status, config = read_register(0)
    if config == 11:
        print "Device is in PRX mode."
    else:
        raise Exception("Device in wrong state. status: %d config: %d" % (status, config))

print "Dropping to IPython shell"
import IPython
IPython.embed()
