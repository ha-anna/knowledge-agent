from app.services.conversation_store import ConversationStore

conversation_store = ConversationStore()


def get_conversation_store() -> ConversationStore:
    return conversation_store
