# memory.py

from langchain_redis import RedisChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
import os
import redis

# Use the environment variable if set, otherwise default to localhost
REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379")
print(f"Connecting to Redis at: {REDIS_URL}")

# Initialize a Redis client
redis_client = redis.StrictRedis.from_url(REDIS_URL)

APP_PREFIX = "osdr:chat:"  # Prefix for App 1 keys
# APP_PREFIX = ""

def clear_chat_history_in_redis():
    """Clear only chat-related entries in Redis without dropping the schema."""
    try:
        # Assuming the keys for chat entries follow APP_PREFIX
        keys = redis_client.keys(f"{APP_PREFIX}*")  # Get all chat keys
        print('what are the keys:', keys)
        if keys:
            redis_client.delete(*keys)  # Delete only chat keys
            print(f"Deleted {len(keys)} chat-related keys for OSDR app.")
        else:
            print("No chat-related keys found for OSDR.")
    except Exception as e:
        print(f"Error clearing chat-related entries in Redis: {e}")

print('Clearing chat history in Redis at startup...')
clear_chat_history_in_redis()


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """Get or create a Redis-based session history and add initial messages if empty."""
    history = RedisChatMessageHistory(session_id=session_id, key_prefix=APP_PREFIX,  redis_url=REDIS_URL, index_name="idx:osdr_chat_history")
    
    # Check if the history is empty (new session)
    if len(history.messages) == 0:
        # Add initial user and AI messages
        history.add_user_message("Hello, can you help me with NASA's Open Science Data Repository?")
        history.add_ai_message(
            "Hello! I’m Astro, NASA’s AI assistant for the Open Science Data Repository (OSDR). "
            "I can help you explore datasets, explain scientific studies, or guide you through "
            "using the repository. You can ask questions like 'What is the effect of spaceflight on gene expression?' "
            "or 'Can you help me find datasets related to Mars research?'"
        )
    
    return history



