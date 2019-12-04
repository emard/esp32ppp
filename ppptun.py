# micropython ESP32
# PPP tunnel

# AUTHOR=EMARD
# LICENSE=BSD

from time import sleep_ms
from machine import UART
from network import PPP
from micropython import const

class ppptun:

  def __init__(self):
    print("PPP tunnel")
    self.uart = UART(2) # 16:RX 17:TX
    #  output wire wifi_gpio16, // RX input on ESP32
    #  input  wire wifi_gpio17, // TX output on ESP32
    #  assign ftdi_rxd = wifi_gpio16 & wifi_gpio17; // echo ESP32 to FTDI, should be half duplex
    self.uart.init(baudrate=115200, bits=8, parity=None, stop=1)
    self.ppp = PPP(self.uart)
    #self.ppp.ifconfig(('192.168.48.4', '255.255.255.0', '192.168.48.254', '8.8.8.8'))
    self.ppp.active(True)
    self.ppp.connect()

  def demo(self):
    print("demo")
    sleep_ms(10000)


def demo():
  t = ppptun()
  t.demo()
  del t

print("usage:")
print("p=ppptun.ppptun()")
print("... PPP traffic at RX=GPIO16, TX=GPIO17")
print("del p")
