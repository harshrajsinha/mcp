from typing import Optional
from dataclasses import dataclass
import os

@dataclass
class SciKiqConfig:
    base_url: str
    client_key: str
    entity_key: str
    user_key: str

    @staticmethod
    def from_env() -> "SciKiqConfig":
        return SciKiqConfig(
            base_url=os.getenv("SCIKIQ_BASE_URL", "http://127.0.0.1:9000/base"),
            client_key=os.getenv("SCIKIQ_CLIENT_KEY", ""),
            entity_key=os.getenv("SCIKIQ_ENTITY_KEY", ""),
            user_key=os.getenv("SCIKIQ_USER_KEY", ""),
        )
