import uuid
from datetime import UTC, datetime

from app.domain.conversation import Conversation, Message


class ConversationStore:
    def __init__(self):
        self.conversations = {}

    def create(self) -> Conversation:
        conversation = Conversation(
            id=str(uuid.uuid4()),
            messages=[],
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )

        self.conversations[conversation.id] = conversation

        return conversation

    def get(self, conversation_id: str) -> Conversation:
        return self.conversations[conversation_id]

    def add_message(
        self,
        conversation_id: str,
        message: Message,
    ) -> None:
        conversation = self.get(conversation_id)

        conversation.messages.append(message)
        conversation.updated_at = message.created_at
