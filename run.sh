#bin/sh
python3 tools/update_urls.py
mpremote connect id:$1 cp -r botc_lights/ main.py config.py :
mpremote connect id:$1 run main.py
