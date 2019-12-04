# esp32ppp

Linux PPP daemon will connect with this
(needs some modified passthru for GPIO 16=RX 17=TX

    output wire wifi_gpio16, // RX input on ESP32
    input  wire wifi_gpio17, // TX output on ESP32

I suggest to have DIP switch alternate between passthru
to default ESP32 serial where the prompt is and this secondary
serial where PPP traffic is. At ULX3S there's modified passthru

    TOP_MODULE_FILE = ../../rtl/ulx3s_v20_passthru_serial2.vhd

set DIP SW1=ON: ESP32 python prompt:

    import ppptun
    p=ppptun.ppptun()

Now you have cca 15 seconds to set DIP SW1=OFF: ESP32 should show some PPP
traffic like this:

    ~�}#�!}!}!} }4}"}&} } } } }%}&y��#}'}"}(}"b\~

Withing 15 seconds you should exit terminal to /dev/ttyUSB0 and run this command from linux side,
it will connect:

    stty -F /dev/ttyUSB0 raw
    pppd /dev/ttyUSB0 115200 10.0.5.2:10.0.5.1 noauth local debug dump defaultroute nocrtscts nodetach

More details on [Linux PPP setup](https://www.instructables.com/id/Connect-the-Raspberry-Pi-to-network-using-UART)
