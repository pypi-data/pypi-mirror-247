import tomllib
from pathlib import Path

#  ──────────────────────────────────────────────────────────────────────────

# default configuration
config = {'root_password': '',
          'mongo_db_ip': '0.0.0.0',
          'mongo_db_name': 'bibtheque'}

# default config path
config_path = Path("~/.config/bibtheque.toml").expanduser()

if config_path.exists():
    with open(config_path, 'rb') as file:
        tmp = tomllib.load(file)

    # set configuration from toml
    for key in tmp.keys():
        config[key] = tmp[key]
