from dataclasses import dataclass
from pathlib import Path


@dataclass
class SavedFile:
    id: str
    path: Path
