#bin/sh
python3 tools/update_urls.py
mpremote connect id:$1 mip install file:. 
mpremote connect id:$1 run botc_lights/main.py