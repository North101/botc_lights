import plasma
import utime as time
from plasma import plasma_stick

from botc_lights.players import (
    ALIVE_STATE_ALIVE,
    ALIVE_STATE_DEAD_NO_VOTE,
    ALIVE_STATE_DEAD_VOTE,
    TYPE_STATE_TRAVELLER,
    PlayerState,
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

  def update(self):
    flicker = (time.ticks_ms() // 500) % 2
    for i, (alive_state, type_state) in enumerate(PlayerState.players):
      if flicker and i == PlayerState.nominated_player:
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
