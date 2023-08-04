import aioble
import ubluetooth as bluetooth

# Register GATT server.
SERVICE = aioble.Service(bluetooth.UUID('AAD80980-48AC-4763-8848-513873A69E15'))
STATE_CHARACTERISTIC = aioble.Characteristic(
  SERVICE,
  bluetooth.UUID('AAD80981-48AC-4763-8848-513873A69E15'),
  write=True,
  capture=True,
)
PLAYER_LIVING_CHARACTERISTIC = aioble.Characteristic(
  SERVICE,
  bluetooth.UUID('AAD80982-48AC-4763-8848-513873A69E15'),
  write=True,
  capture=True,
)
PLAYER_TYPE_CHARACTERISTIC = aioble.Characteristic(
  SERVICE,
  bluetooth.UUID('AAD80983-48AC-4763-8848-513873A69E15'),
  write=True,
  capture=True,
)
PLAYER_TEAM_CHARACTERISTIC = aioble.Characteristic(
  SERVICE,
  bluetooth.UUID('AAD80984-48AC-4763-8848-513873A69E15'),
  write=True,
  capture=True,
)
PLAYER_NOMINATED_CHARACTERISTIC = aioble.Characteristic(
  SERVICE,
  bluetooth.UUID('AAD80985-48AC-4763-8848-513873A69E15'),
  write=True,
  capture=True,
)
BRIGHTNESS_CHARACTERISTIC = aioble.Characteristic(
  SERVICE,
  bluetooth.UUID('AAD80986-48AC-4763-8848-513873A69E15'),
  write=True,
  capture=True,
)
COLORS_CHARACTERISTIC = aioble.Characteristic(
  SERVICE,
  bluetooth.UUID('AAD80987-48AC-4763-8848-513873A69E15'),
  write=True,
  capture=True,
)
aioble.register_services(SERVICE)
