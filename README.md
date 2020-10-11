# esp32ppp

# Micropython idf3 official binary

It doesn't have IP forwarding so we will use socks to connect.
ESP32 must first active PPP and then connect to WiFi network.
If PPP is started after WiFi, it will spoil WiFi routing.

To verify that ESP32 WiFi internet routing is still working,
we can check by trying to set NTP time. If WiFi internet (still) works
it will just give prompt, if not some some error will appear.

    from ntptime import settime
    settime()

ESP32 PPP has limited time (about 10 seconds) when it tries to connect with linux
and then it will give up. PPP must be started before WiFi, otherwise if
PPP is started after, it will spoil WiFi routing. For the same reason PPP can't
be restarted to retry, so we have one chance in a time window to connect.

In practice we power up board with autostart
scripts. ESP32 autostart script first waits 1 minute and then starts ppp, wifi, uftpd, socks, in this order.
Saxonsoc linux boots about 50 seconds and then it runs autostart scripts
from "/etc/init.d/", there is S30ppp which starts pppd daemon.

Copy "main.py" to root of ESP32 micropython internal flash disk.
Copy "S30ppp" to "/etc/init.d/S30ppp" at saxonsoc linux.
Few seconds after saxonsoc boots, you should see them connected with ppp
interface:

    ifconfig

    ppp0      Link encap:Point-to-Point Protocol  
              inet addr:10.0.5.2  P-t-P:10.0.5.1  Mask:255.255.255.255
              UP POINTOPOINT RUNNING NOARP MULTICAST  MTU:1500  Metric:1
              RX packets:5 errors:0 dropped:0 overruns:0 frame:0
              TX packets:4 errors:0 dropped:0 overruns:0 carrier:0
              collisions:0 txqueuelen:3 
              RX bytes:90 (90.0 B)  TX bytes:58 (58.0 B)

    curl --socks5 10.0.5.1:1080 http://87.248.100.216/index.html
    ... webpage should be printed to stdout ...

This should also work but currently there's some problem at esp32 socks proxy

    curl --proxy socks5h://10.0.5.1:1080 http://www.yahoo.com/index.html

# Micropython compiled with IP forward

[Paul Ruiz recompiled micropython with IP forwarding enabled](https://gitlab.com/pnru/ulx3s-misc/blob/master/upython/upython_pnr5.bin)

    #define IP_FORWARD 1

Load this to ESP32 first.

Linux PPP daemon will connect with this
(needs some modified passthru for GPIO 16=RX 17=TX

    output wire wifi_gpio16, // RX input on ESP32
    input  wire wifi_gpio17, // TX output on ESP32

I suggest to have DIP switch alternate between passthru
to default ESP32 serial where the prompt is and this secondary
serial where PPP traffic is. At ULX3S there's modified passthru

    TOP_MODULE_FILE = ../../rtl/ulx3s_v20_passthru_serial2.vhd

set DIP SW1=ON: ESP32 python prompt:

    screen /dev/ttyUSB0

    >>> import ppptun
    >>> p=ppptun.ppptun()

Now you have cca 15 seconds to connect. Don't rush, there's enough time to:
set DIP SW1=OFF: ESP32 should show some PPP packets.

    ~�}#�!}!}!} }4}"}&} } } } }%}&y��#}'}"}(}"b\~

disconnect terminal "screen /dev/ttyUSB0 115200"

    Ctrl-A \

("\\" on my keyboard is Right AltGr-Q)

and run this command as linux root user (prepare it in a script):

    stty -F /dev/ttyUSB0 raw
    pppd /dev/ttyUSB0 115200 10.0.5.2:10.0.5.1 noauth local debug dump defaultroute nocrtscts nodetach

it should print something like this as successful connect:

    sent [LCP ProtRej id=0x2 80 57 01 01 00 0e 01 0a 19 48 30 02 45 eb 9a 9a]
    rcvd [IPCP ConfAck id=0x1 <compress VJ 0f 01> <addr 10.0.5.2>]
    rcvd [IPCP ConfReq id=0x2 <compress VJ 0f 01> <addr 0.0.0.0>]
    sent [IPCP ConfNak id=0x2 <addr 10.0.5.1>]
    rcvd [IPCP ConfReq id=0x3 <compress VJ 0f 01> <addr 10.0.5.1>]
    sent [IPCP ConfAck id=0x3 <compress VJ 0f 01> <addr 10.0.5.1>]
    not replacing default route to enp2s0 [192.168.18.254]
    local  IP address 10.0.5.2
    remote IP address 10.0.5.1

If ESP32 is running FTP server you can connect there:

    ftp 10.0.5.1
    Connected to 10.0.5.1.
    220 Hello, this is the ESP8266.
    230 Logged in.
    Remote system type is UNIX.
    Using binary mode to transfer files.
    ftp> ls
    200 OK
    150 Directory listing:
    -rw-r--r-- 1 owner group        137 Jan  1 00:01 boot.py
    -rw-r--r-- 1 owner group         14 Jan  1 07:38 webrepl_cfg.py
    ...

More details on [Linux PPP setup](https://www.instructables.com/id/Connect-the-Raspberry-Pi-to-network-using-UART)

ESP32 will route PPP traffic but can't do NAT so some static
routes are required for the computer connected to ESP32 PPP:

    route add default gw 10.0.5.1

DNS can be set by editing file "/etc/resolv.conf"

    domain lan
    search lan
    nameserver 192.168.28.254

and route for the other computer on WiFi network which needs to know how to return
packet back to ESP32. Assume ESP32 has been assigned WiFi address 192.168.28.118:

    route add -host 10.0.5.2 gw 192.168.28.118

remote linux on LAN can be used to provide internet access by activating
its masquerade option:

    echo 1 > /proc/sys/net/ipv4/ip_forward
    iptables --table nat --append POSTROUTING -s 10.0.5.2 -j MASQUERADE
    iptables --append FORWARD -d 10.0.5.2 -j ACCEPT

ESP32 has no NAT but linux can use IPIP or GRE kernel module
to get full featured internet access. Howto is here:

[Linux tunnels](https://developers.redhat.com/blog/2019/05/17/an-introduction-to-linux-virtual-interfaces-tunnels/)

# SOCKS server

KOST released [socks server for
micropython](https://github.com/kost/micropython-socks)
that means you can tunnel any SOCKS5 connection over ESP32
since micropython does not come with NAT support, that means you can go to the internet over ESP32 using SOCKS server.
Installation is simple if you have connected ESP32 already to the internet:
You have to run this on ulx3s repl shell:

    import upip
    upip.install('micropython-socks')

and then you can just simply say:

    import socks
    socks.start()

it will start listening on 0.0.0.0:1080 for SOCKS5 connections.
Then you can simply from SaxonSoc test it with the following (or any other host):

    curl --socks5 10.0.5.1:1080 http://87.248.100.216/index.html
