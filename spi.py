import spidev

spi = spidev.SpiDev()

class ConfigRegister(object):
    MASK_RX_DR = 0
    MASK_TX_DS = 0
    MASK_MAX_RT = 0
    EN_CRC = 0
    CRCO = 0
    PWR_UP = 0
    PRIM_RX = 0

    def __init__(self, config=0):
        self.unpack(config)

    def pack(self):
        config = 0
        for index, flag in enumerate((self.PRIM_RX, self.PWR_UP, self.CRCO, self.EN_CRC, self.MASK_MAX_RT, self.MASK_TX_DS, self.MASK_RX_DR)):
            config = config | (flag << index)
        return config
    
    def unpack(self, config):
        for index, flag_name in enumerate(("PRIM_RX", "PWR_UP", "CRCO", "EN_CRC", "MASK_MAX_RT", "MASK_TX_DS", "MASK_RX_DR")):
            setattr(self, flag_name, (config >> index) & 1)

    def __repr__(self):
        desc = '' 
        for flag_name in ("PRIM_RX", "PWR_UP", "CRCO", "EN_CRC", "MASK_MAX_RT", "MASK_TX_DS", "MASK_RX_DR"):
            desc += "{0}: {1}\n".format(flag_name, getattr(self, flag_name))

        return desc
 
    def __eq__(self, target):
        return self.unpack == target

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
