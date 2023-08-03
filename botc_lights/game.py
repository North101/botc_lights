import math

import plasma
import utime as time
from plasma import plasma_stick

from botc_lights.constants import (
    COLOR_WHITE,
    GAME_STATE_GAME,
    LIVING_STATE_ALIVE,
    LIVING_STATE_DEAD,
    LIVING_STATE_HIDDEN,
    MAX_PLAYER_COUNT,
    PLAYER_COLOR_CHARACTER,
    PLAYER_COLOR_DEAD,
    PLAYER_COLOR_EVIL,
    PLAYER_COLOR_GOOD,
    PLAYER_COLOR_HIDDEN,
    PLAYER_COLOR_TRAVELLER,
    PLAYER_COLORS,
    TEAM_STATE_EVIL,
    TEAM_STATE_GOOD,
    TEAM_STATE_HIDDEN,
    TYPE_STATE_CHARACTER,
    TYPE_STATE_TRAVELLER,
)


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
      (LIVING_STATE_HIDDEN, TYPE_STATE_CHARACTER, TEAM_STATE_HIDDEN)
      for _ in range(MAX_PLAYER_COUNT)
    ]
    self.colors: dict[int, tuple[int, int, int]] = PLAYER_COLORS

  def led_index(self, i: int):
    return self.num_leds - 1 - i if self.reverse_leds else i

  def set_led(self, i: int, r: int, g: int, b: int, brightness: float = 1.0):
    brightness = brightness * self.brightness
    self.led_strip.set_rgb(self.led_index(i), int(r * brightness), int(g * brightness), int(b * brightness))

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
          color = self.colors[PLAYER_COLOR_TRAVELLER]
        else:
          color = self.colors[PLAYER_COLOR_CHARACTER]
      elif living_state == LIVING_STATE_DEAD:
        color = self.colors[PLAYER_COLOR_DEAD]
      else:
        color = self.colors[PLAYER_COLOR_HIDDEN]

      self.set_led(i, *color, v)

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

        self.set_led(i, *COLOR_WHITE, v)
    else:
      for i, (_, _, team_state) in enumerate(self.players):
        if team_state == TEAM_STATE_GOOD:
          color = self.colors[PLAYER_COLOR_GOOD]
        elif team_state == TEAM_STATE_EVIL:
          color = self.colors[PLAYER_COLOR_EVIL]
        else:
          color = self.colors[PLAYER_COLOR_HIDDEN]

        self.set_led(i, *color)
