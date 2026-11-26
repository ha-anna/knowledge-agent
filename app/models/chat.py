from typing import Annotated

from pydantic import BaseModel, StringConstraints


class MessageRequest(BaseModel):
    content: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    document_id: str | None = None
