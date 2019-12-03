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
    self.uart = UART(1)
    self.uart.init(baudrate=115200, bits=8, parity=None, stop=1)
    self.ppp = PPP(self.uart)
    self.ppp.ifconfig(('192.168.48.4', '255.255.255.0', '192.168.48.254', '8.8.8.8'))
    self.ppp.active(True)
    self.ppp.connect()
    sleep_ms(10000)

  def demo(self):
    print("demo")


def demo():
  t = ppptun()
  t.demo()
  del t

print("usage:")
print("ppptun.demo()")
