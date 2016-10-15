import spidev

spi = spidev.SpiDev()
spi.open(0,0)
print spi.xfer([0x00, 0x00])

import IPython
IPython.embed()
