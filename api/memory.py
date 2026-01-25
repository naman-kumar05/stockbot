# api/memory.py

from typing import Optional, Dict, List


class ConversationMemory:
    """
    Enhanced conversation memory for ChatGPT-style interactions.
    Stores full conversation history for context-aware responses.
    """

    def __init__(self):
        self.last_company: Optional[str] = None
        self.last_ticker: Optional[str] = None
        self.last_intent: Optional[str] = None
        self.history: List[str] = []  # Legacy: simple message list
        self.conversation_history: List[Dict[str, str]] = []  # Full conversation for LLM

    # -----------------------------
    # Update memory
    # -----------------------------

    def update(
        self,
        company: Optional[str] = None,
        ticker: Optional[str] = None,
        intent: Optional[str] = None,
        user_message: Optional[str] = None,
        assistant_message: Optional[str] = None
    ):
        if company:
            self.last_company = company

        if ticker:
            self.last_ticker = ticker

        if intent:
            self.last_intent = intent

        if user_message:
            self.history.append(user_message)
            self.history = self.history[-10:]  # keep last 10 only
            # Add to conversation history
            self.conversation_history.append({"role": "user", "content": user_message})
        
        if assistant_message:
            # Add assistant response to conversation history
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
        
        # Keep conversation history manageable (last 20 messages = 10 exchanges)
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]

    # -----------------------------
    # Resolve helpers
    # -----------------------------

    def resolve_company(self, fallback: Optional[str] = None) -> Optional[str]:
        return fallback or self.last_company

    def resolve_ticker(self, fallback: Optional[str] = None) -> Optional[str]:
        return fallback or self.last_ticker

    def resolve_intent(self, fallback: Optional[str] = None) -> Optional[str]:
        return fallback or self.last_intent

    # -----------------------------
    # Snapshot (debug / logging)
    # -----------------------------

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Returns conversation history in LLM format."""
        return self.conversation_history.copy()
    
    def clear_history(self):
        """Clears conversation history."""
        self.conversation_history = []
        self.history = []
    
    def snapshot(self) -> Dict:
        return {
            "last_company": self.last_company,
            "last_ticker": self.last_ticker,
            "last_intent": self.last_intent,
            "history": self.history,
            "conversation_history_length": len(self.conversation_history)
        }


# -----------------------------
# Singleton-style access
# -----------------------------

_memory_instance: Optional[ConversationMemory] = None


def get_memory() -> ConversationMemory:
    """
    Returns a single memory instance per session/runtime.
    """
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = ConversationMemory()
    return _memory_instance
