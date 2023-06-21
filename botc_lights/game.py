import plasma
import utime as time
from plasma import plasma_stick

from botc_lights.players import (
    ALIVE_STATE_ALIVE,
    ALIVE_STATE_DEAD_NO_VOTE,
    ALIVE_STATE_DEAD_VOTE,
    ALIVE_STATE_HIDDEN,
    MAX_PLAYER_COUNT,
    TYPE_STATE_PLAYER,
    TYPE_STATE_TRAVELLER,
)

NUM_LEDS = 50
COLOR_PLAYER_ALIVE    = (160, 160, 160)
COLOR_TRAVELLER_ALIVE = (255, 239, 59)
COLOR_DEAD_VOTE       = (224, 64, 251)
COLOR_DEAD_NO_VOTE    = (255, 82, 82)
COLOR_HIDDEN          = (000, 000, 000)

class Game:
  def __init__(self):
    self.led_strip = plasma.WS2812(NUM_LEDS, 0, 0, plasma_stick.DAT, color_order=plasma.COLOR_ORDER_RGB)
    self.led_strip.start()

    self.nominated_player = -1
    self.players: list[tuple[int, int]] = [
      (ALIVE_STATE_HIDDEN, TYPE_STATE_PLAYER)
      for _ in range(MAX_PLAYER_COUNT)
    ]
  
  def pack_player_state(self):
    data = (self.nominated_player + 1) & 0b11111
    for (alive_state, type_state) in reversed(self.players):
      data <<= 1
      data |= type_state & 0b1
      data <<= 2
      data |= alive_state & 0b11
    return data.to_bytes(length=65, byteorder='little')

  def unpack_player_state(self, data):
    data = int.from_bytes(data, 'little')
    for i in range(len(self.players)):
      alive_state = data & 0b11
      data >>= 2
      type_state = data & 0b1
      data >>= 1
      self.players[i] = (alive_state, type_state)
    self.nominated_player = (data & 0b11111) - 1

  def update(self):
    flicker = (time.ticks_ms() // 500) % 2
    for i, (alive_state, type_state) in enumerate(self.players):
      if flicker and i == self.nominated_player:
        value = COLOR_HIDDEN
      elif alive_state == ALIVE_STATE_ALIVE:
        if type_state == TYPE_STATE_TRAVELLER:
          value = COLOR_TRAVELLER_ALIVE
        else:
          value = COLOR_PLAYER_ALIVE
      elif alive_state == ALIVE_STATE_DEAD_VOTE:
        value = COLOR_DEAD_VOTE
      elif alive_state == ALIVE_STATE_DEAD_NO_VOTE:
        value = COLOR_DEAD_NO_VOTE
      else:
        value = COLOR_HIDDEN

      self.led_strip.set_rgb(NUM_LEDS - 1 - i, *value)
