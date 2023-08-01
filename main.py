import aioble
import uasyncio as asyncio
import utime as time
from aioble.device import DeviceConnection

import config
from botc_lights.ble import (
    BRIGHTNESS_CHARACTERISTIC,
    PLAYER_LIVING_CHARACTERISTIC,
    PLAYER_NOMINATED_CHARACTERISTIC,
    PLAYER_TEAM_CHARACTERISTIC,
    PLAYER_TYPE_CHARACTERISTIC,
    SERVICE,
    STATE_CHARACTERISTIC,
)
from botc_lights.game import Game

# How frequently to send advertising beacons.
_ADV_INTERVAL_MS = 250_000

class GameBLE:
  def __init__(self, name: str, game: Game, interval_us = _ADV_INTERVAL_MS):
    self.name = name
    self.game = game
    self.interval_us = interval_us
    self.tasks: asyncio.Task | None = None

  async def advertise(self):
    print('Advertising')
    connection = await aioble.advertise(
      self.interval_us,
      name=self.name,
      services=[SERVICE.uuid],
    )
    if connection is None:
      return

    async with connection:
      self.on_connect(connection)

      await connection.disconnected()
      self.on_disconnect()

  def on_connect(self, connection: DeviceConnection):
    print('Connection from', connection.device)
    self.tasks = asyncio.create_task(asyncio.gather(
      self.on_characteristic(STATE_CHARACTERISTIC, self.on_state),
      self.on_characteristic(PLAYER_LIVING_CHARACTERISTIC, self.on_player_living),
      self.on_characteristic(PLAYER_TYPE_CHARACTERISTIC, self.on_player_type),
      self.on_characteristic(PLAYER_TEAM_CHARACTERISTIC, self.on_player_team),
      self.on_characteristic(PLAYER_NOMINATED_CHARACTERISTIC, self.on_player_nominated),
      self.on_characteristic(BRIGHTNESS_CHARACTERISTIC, self.on_brightness),
    ))

  def on_disconnect(self):
    print('Disconnected')
    if self.tasks:
      self.tasks.cancel()
      self.tasks = None

  async def on_characteristic(self, characteristic: aioble.Characteristic, callback):
    while True:
      _, data = await characteristic.written() # type: ignore
      callback(data)

  def on_state(self, data: bytes):
    self.game.state = int.from_bytes(data, 'little')
    self.game.state_changed = time.ticks_ms()
    self.game.update()

  def on_player_living(self, data: bytes):
    value = int.from_bytes(data, 'little')
    for i, (living_state, type_state, team_state) in enumerate(self.game.players):
      living_state = value & 0b11
      value >>= 2
      self.game.players[i] = (living_state, type_state, team_state)

  def on_player_type(self, data: bytes):
    value = int.from_bytes(data, 'little')
    for i, (living_state, type_state, team_state) in enumerate(self.game.players):
      type_state = value & 0b1
      value >>= 1
      self.game.players[i] = (living_state, type_state, team_state)

  def on_player_team(self, data: bytes):
    value = int.from_bytes(data, 'little')
    for i, (living_state, type_state, team_state) in enumerate(self.game.players):
      team_state = value & 0b11
      value >>= 2
      self.game.players[i] = (living_state, type_state, team_state)

  def on_player_nominated(self, data: bytes):
    nominated_player = int.from_bytes(data, 'little') - 1
    if nominated_player < 0:
      nominated_player = None
    self.game.nominated_player = nominated_player

  def on_brightness(self, data: bytes):
    brightness = int.from_bytes(data, 'little')
    self.game.brightness = brightness / 255


async def advertise_loop(game_ble: GameBLE):
  while True:
    try:
      await asyncio.create_task(game_ble.advertise())
    except BaseException as e:
      print(e)


async def update_loop(game_ble: GameBLE):
  while True:
    game_ble.game.update()
    await asyncio.sleep_ms(10)


async def start():
  game_ble = GameBLE(
    name='BotC Lights',
    game=Game(
      num_leds=config.NUM_LEDS,
      reverse_leds=config.REVERSE_LEDS,
      brightness=config.BRIGHTNESS,
      nomination_speed_ms=config.NOMINATION_SPEED_MS,
      reveal_speed_ms=config.REVEAL_SPEED_MS,
    ),
  )
  await asyncio.gather(
    asyncio.create_task(advertise_loop(game_ble)),
    asyncio.create_task(update_loop(game_ble)),
  )


if __name__ == '__main__':
  asyncio.run(start())
