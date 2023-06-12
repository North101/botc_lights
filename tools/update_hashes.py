import os
import json
import binascii
import hashlib

_CHUNK_SIZE = 128

def _chunk(src, dest):
    buf = memoryview(bytearray(_CHUNK_SIZE))
    while True:
        n = src.readinto(buf)
        if n == 0:
            break
        dest(buf if n == _CHUNK_SIZE else buf[:n])

def hash(path):
    with open(path, "rb") as f:
        hs256 = hashlib.sha256()
        _chunk(f, hs256.update)
        existing_hash = str(binascii.hexlify(hs256.digest()), "utf-8")
        return existing_hash


for root, dirs, files in os.walk('.'):
    for name in list(dirs):
        if name.startswith('.'):
            dirs.remove(name)
    if 'package.json' in files:
        with open(f'{root}/package.json', 'r') as f:
            package = json.load(f)
            package['hashes'] = [
                [path, hash(f'{root}/{path}')[:8]]
                for (path, url) in package['urls']
            ]
        with open(f'{root}/package.json', 'w') as f:
            json.dump(package, f, indent=4)
