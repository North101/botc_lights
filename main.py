import ubluetooth as bluetooth
import utime as time
from machine import Pin

from botc_lights.ble_peripheral import BLEPeripheral
from botc_lights.game import Game
from config import NUM_LEDS, REVERSE_LEDS


def start(num_leds: int, reverse_leds: bool):
    led = Pin("LED", Pin.OUT)
    game = Game(
        num_leds=num_leds,
        reverse_leds=reverse_leds,
    )

    ble_peripheral = BLEPeripheral(
        bluetooth.BLE(),
        name='BotC Lights',
        rx_callback=game.unpack_data,
    )

    while True:
        if not ble_peripheral.is_connected():
            led.toggle()
            time.sleep(1)
        else:
            led.off()
            game.update()


if __name__ == '__main__':
    start(
        num_leds=NUM_LEDS,
        reverse_leds=REVERSE_LEDS,
    )
