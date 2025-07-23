# settings.py
import tomli
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    max_grid_size: int = 20
    log_level: str = "info"

def load_settings():
    toml_path = Path(__file__).parent / "settings.toml"
    if toml_path.exists():
        with open(toml_path, "rb") as f:
            config = tomli.load(f)
        return Settings(**config)
    return Settings()

settings = load_settings()
