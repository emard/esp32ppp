# esp32ppp

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

and route for the other computer on WiFi network which needs to know how to return
packet back to ESP32. Assume ESP32 has been assigned WiFi address 192.168.28.118:

    route add -host 10.0.5.2 gw 192.168.28.118

