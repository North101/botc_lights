import bluetooth
import utime as time
from machine import Pin

from botc_lights.ble_peripheral import BLEPeripheral
from botc_lights.game import Game
from botc_lights.packets import unpack_player_state


def start():
    led = Pin("LED", Pin.OUT)
    game = Game()

    def on_rx(v):
        unpack_player_state(v)
        game.update()

    ble_peripheral = BLEPeripheral(bluetooth.BLE(), name='BotC Lights')
    ble_peripheral.on_write(on_rx)

    while True:
        if not ble_peripheral.is_connected():
            led.toggle()
            time.sleep(1)
        else:
            led.off()

if __name__ == '__main__':
    start()
