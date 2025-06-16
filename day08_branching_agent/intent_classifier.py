from typing import Literal

Intent = Literal["chitchat","task"]

def classify_intent(message:str) ->Intent:
    """Simple rule-based intent classifier."""
    chitchat_keywords = ["hi", "hello", "how are you", "what's up", "yo", "sup", "good morning", "good night"]
    lower_message = message.lower()

    if any(kw in lower_message for kw in chitchat_keywords):
        return "chitchat"
    return "task"

