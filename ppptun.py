# micropython ESP32
# PPP tunnel

# stty -F /dev/ttySL0 raw
# pppd /dev/ttySL0 115200 10.0.5.2:10.0.5.1 noauth local debug dump nodefaultroute nocrtscts nodetach

# AUTHOR=EMARD
# LICENSE=BSD

from machine import UART
from network import PPP

class ppptun:

  def __init__(self):
    print("PPP tunnel")
    self.uart = UART(2) # 16:RX 17:TX
    #  on Linux:
    #  output wire wifi_gpio16, // RX input on ESP32
    #  input  wire wifi_gpio17, // TX output on ESP32
    self.uart.init(baudrate=230400, bits=8, parity=None, stop=1)
    self.ppp = PPP(self.uart)
    #self.ppp.ifconfig(('192.168.48.4', '255.255.255.0', '192.168.48.254', '8.8.8.8')) # not needed
    self.ppp.active(True)
    self.ppp.connect()

print("usage:")
print("p=ppptun.ppptun()")
print("... PPP traffic at RX=GPIO16, TX=GPIO17")
print("del p")
