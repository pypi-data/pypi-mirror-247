from typing import List, Dict

from pydantic.main import BaseModel


class ServiceComposeInfo(BaseModel):
    name: str
    image: str
    environment: Dict[str, str]
    ports: List[str]
    volumes: List[str]
    devices: List[str] = []
    tmpfs: List[str] = []

    privileged: bool = False
    extras: str = ""
    # Must contain valid YAML including newlines if necessary.

    labels: List = []
    extra_networks: List[str] = []
