from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4

from app.domain.source import Source


@dataclass
class Message:
    role: str
    content: str
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    sources: list[Source] = field(default_factory=list)


@dataclass
class Conversation:
    id: str
    messages: list[Message]
    created_at: datetime
    updated_at: datetime
