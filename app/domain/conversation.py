from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


@dataclass
class Message:
    role: str
    content: str
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


@dataclass
class Conversation:
    id: str
    messages: list[Message]
    created_at: datetime
    updated_at: datetime
