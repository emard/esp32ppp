from time import sleep
sleep(50)
import ppptun
p=ppptun.ppptun()
from ntptime import settime
try:
  import wifiman
except:
  print("no WiFi")
import uftpd
try:
  settime()
except:
  print("NTP not available")
import socks
socks.start()
#try:
#  import rtceink
#except:
#  print("rtceink not loaded")
