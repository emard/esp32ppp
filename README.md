# esp32ppp

Linux PPP daemon will connect with this
(needs some modified passthru for GPIO 16=RX 17=TX

    output wire wifi_gpio16, // RX input on ESP32
    input  wire wifi_gpio17, // TX output on ESP32

I suggest to have DIP switch alternate between passthru
to default ESP32 serial where the prompt is and this secondary
serial where PPP traffic is.

From linux side, this command will connect:

    stty -F /dev/ttyUSB0 raw
    pppd /dev/ttyUSB0 115200 10.0.5.2:10.0.5.1 noauth local debug dump defaultroute nocrtscts

More details on [Linux PPP setup](https://www.instructables.com/id/Connect-the-Raspberry-Pi-to-network-using-UART)
