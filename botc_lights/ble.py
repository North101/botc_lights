import aioble
import ubluetooth as bluetooth

_SERVICE                         = bluetooth.UUID('AAD80980-48AC-4763-8848-513873A69E15')
_STATE_CHARACTERISTIC            = bluetooth.UUID('AAD80981-48AC-4763-8848-513873A69E15')
_PLAYER_LIVING_CHARACTERISTIC    = bluetooth.UUID('AAD80982-48AC-4763-8848-513873A69E15')
_PLAYER_TYPE_CHARACTERISTIC      = bluetooth.UUID('AAD80983-48AC-4763-8848-513873A69E15')
_PLAYER_TEAM_CHARACTERISTIC      = bluetooth.UUID('AAD80984-48AC-4763-8848-513873A69E15')
_PLAYER_NOMINATED_CHARACTERISTIC = bluetooth.UUID('AAD80985-48AC-4763-8848-513873A69E15')


# Register GATT server.
SERVICE = aioble.Service(_SERVICE)
STATE_CHARACTERISTIC = aioble.Characteristic(
  SERVICE,
  _STATE_CHARACTERISTIC,
  write=True,
  write_no_response=True,
  capture=True,
)
PLAYER_LIVING_CHARACTERISTIC = aioble.Characteristic(
  SERVICE,
  _PLAYER_LIVING_CHARACTERISTIC,
  write=True,
  write_no_response=True,
  capture=True,
)
PLAYER_TYPE_CHARACTERISTIC = aioble.Characteristic(
  SERVICE,
  _PLAYER_TYPE_CHARACTERISTIC,
  write=True,
  write_no_response=True,
  capture=True,
)
PLAYER_TEAM_CHARACTERISTIC = aioble.Characteristic(
  SERVICE,
  _PLAYER_TEAM_CHARACTERISTIC,
  write=True,
  write_no_response=True,
  capture=True,
)
PLAYER_NOMINATED_CHARACTERISTIC = aioble.Characteristic(
  SERVICE,
  _PLAYER_NOMINATED_CHARACTERISTIC,
  write=True,
  write_no_response=True,
  capture=True,
)
aioble.register_services(SERVICE)
