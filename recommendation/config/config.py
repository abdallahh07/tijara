import yaml
from pathlib import Path
 
CONFIG_PATH = Path(__file__).parent / "config.yml"
 
 
def load_config(path: Path = CONFIG_PATH) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)

settings = load_config()
 