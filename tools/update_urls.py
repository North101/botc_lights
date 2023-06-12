import fnmatch
import json
import os


def list_python_files(dir):
  for root, dirs, files in os.walk(dir):
    for name in list(dirs):
      if name.startswith('.'):
        dirs.remove(name)
    if root != dir and 'package.json' in files:
      dirs.clear()
      continue

    for file in files:
      if file.endswith('.py'):
        yield os.path.relpath('/'.join(os.path.join(root, file).split(os.path.sep)), dir)


for root, dirs, files in os.walk('.'):
  for dir in list(dirs):
    if dir.startswith('.'):
      dirs.remove(dir)

  if 'package.json' in files:
    with open(os.path.join(root, 'package.json'), 'r') as f:
      package = json.load(f)
      repository = package['repository']
      exclude = package.get('exclude', [])

      package['urls'] = [
        [file, f'{repository}/{file}']
        for file in list_python_files(root)
        if not any(fnmatch.fnmatch(file, pattern) for pattern in exclude)
      ]
    with open(os.path.join(root, 'package.json'), 'w') as f:
      json.dump(package, f, indent=2)
