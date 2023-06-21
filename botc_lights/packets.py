import usocket as socket

from botc_lights.players import MAX_PLAYER_COUNT, PlayerState


def pack_player_state():
  data = (PlayerState.nominated_player + 1) & 0b11111
  for (alive_state, type_state) in reversed(PlayerState.players):
    data <<= 1
    data |= type_state & 0b1
    data <<= 2
    data |= alive_state & 0b11
  return data.to_bytes(length=65, byteorder='little')


def unpack_player_state(data):
  data = int.from_bytes(data, 'little')
  for i in range(MAX_PLAYER_COUNT):
    alive_state = data & 0b11
    data >>= 2
    type_state = data & 0b1
    data >>= 1
    PlayerState.players[i] = (alive_state, type_state)
  PlayerState.nominated_player = (data & 0b11111) - 1


def recv_data_from(socket: socket.socket):
  data, addr = socket.recvfrom(1024)
  return data, addr


def send_data_to(socket: socket.socket, data: bytes, address: tuple[str, int]):
  data_sent = 0
  while data_sent < len(data):
    data_sent += socket.sendto(data[data_sent:], address)
