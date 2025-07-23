# settings.py
from pathlib import Path

import tomli
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    max_grid_size: int = 20
    max_grid_size_x: int = 20
    max_grid_size_y: int = 20
    log_level: str = "info"


def load_settings():
    toml_path = Path(__file__).parent / "settings.toml"
    if toml_path.exists():
        with open(toml_path, "rb") as f:
            config = tomli.load(f)
        return Settings(**config)
    return Settings()


settings = load_settings()
