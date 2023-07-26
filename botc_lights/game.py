import math

import plasma
import utime as time
from plasma import plasma_stick

from botc_lights.players import (
    GAME_STATE_GAME,
    LIVING_STATE_ALIVE,
    LIVING_STATE_DEAD,
    LIVING_STATE_HIDDEN,
    MAX_PLAYER_COUNT,
    TEAM_STATE_EVIL,
    TEAM_STATE_GOOD,
    TEAM_STATE_HIDDEN,
    TYPE_STATE_PLAYER,
    TYPE_STATE_TRAVELLER,
)

COLOR_HIDDEN                 = (0.000, 0.000)

COLOR_LIVING_ALIVE_PLAYER    = (0.000, 0.000)
COLOR_LIVING_ALIVE_TRAVELLER = (0.153, 0.769)
COLOR_LIVING_DEAD            = (0.808, 0.745)

COLOR_TEAM_GOOD              = (0.570, 0.680)
COLOR_TEAM_EVIL              = (0.000, 0.790)

class Game:
  def __init__(self, num_leds: int, reverse_leds: bool, brightness: float, nomination_speed_ms: int, reveal_speed_ms: int):
    self.num_leds = num_leds
    self.reverse_leds = reverse_leds
    self.brightness = brightness
    self.nomination_speed_ms = nomination_speed_ms
    self.reveal_speed_ms = reveal_speed_ms

    self.led_strip = plasma.WS2812(num_leds, 0, 0, plasma_stick.DAT, rgbw=True, color_order=plasma.COLOR_ORDER_GRB)
    self.led_strip.start()

    self.state = GAME_STATE_GAME
    self.state_changed = time.ticks_ms()
    self.nominated_player: int|None = None
    self.players: list[tuple[int, int, int]] = [
      (LIVING_STATE_HIDDEN, TYPE_STATE_PLAYER, TEAM_STATE_HIDDEN)
      for _ in range(MAX_PLAYER_COUNT)
    ]

  def led_index(self, i: int):
    return self.num_leds - 1 - i if self.reverse_leds else i

  def set_led(self, i: int, h: float, s: float, v: float):
    self.led_strip.set_hsv(self.led_index(i), h, s, self.brightness * v)

  def flicker(self, percent: float):
    v_flicker = (percent % 1.0) * 2.0
    if v_flicker > 1.0:
      v_flicker = 2.0 - v_flicker
    return v_flicker

  def update(self):
    if self.state == GAME_STATE_GAME:
      self.update_game()
    else:
      self.update_reveal()

  def update_game(self):
    for i, (living_state, type_state, _) in enumerate(self.players):
      if i == self.nominated_player:
        v = self.flicker(time.ticks_ms() / self.nomination_speed_ms)
      else:
        v = 1.0

      if living_state == LIVING_STATE_ALIVE:
        if type_state == TYPE_STATE_TRAVELLER:
          h, s = COLOR_LIVING_ALIVE_TRAVELLER
        else:
          h, s = COLOR_LIVING_ALIVE_PLAYER
      elif living_state == LIVING_STATE_DEAD:
        h, s = COLOR_LIVING_DEAD
      else:
        h, s = COLOR_HIDDEN
        v = 0.0

      self.set_led(i, h, s, v)

  def update_reveal(self):
    all_hidden = all(team_state == TEAM_STATE_HIDDEN for _, _, team_state in self.players)
    if all_hidden:
      elapsed = time.ticks_diff(time.ticks_ms(), self.state_changed) / self.reveal_speed_ms
      current = int(elapsed)
      for i in range(len(self.players)):
        if i == current:
          v = self.flicker(elapsed)
        else:
          v = 0.0

        self.set_led(i, 0, 0, v)
    else:
      for i, (_, _, team_state) in enumerate(self.players):
        v = 1.0
        if team_state == TEAM_STATE_GOOD:
          h, s = COLOR_TEAM_GOOD
        elif team_state == TEAM_STATE_EVIL:
          h, s = COLOR_TEAM_EVIL
        else:
          h, s = COLOR_HIDDEN
          v = 0.0

        self.set_led(i, h, s, v)
