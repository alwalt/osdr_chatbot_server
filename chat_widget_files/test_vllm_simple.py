# test_llm_openai.py

from openai import OpenAI

# API key for local instance (not used in this case)
openai_api_key = "EMPTY"

# Local server base URL
#openai_api_base = "https://localhost:8000/serve/v1"
openai_api_base = "http://localhost:8000/serve/v1/"

# Initialize the client with the local base URL and API key
client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

# Set up a test prompt
chat_response = client.chat.completions.create(
    #model="Meta-Llama-3.1-8B-Instruct",
    model="/home/woalvara/vllm_serve/models/Llama-3.1-8B-Instruct",
    messages=[
        {"role": "user", "content": "Tell me in one sentence what Mexico is famous for"},
    ]
)

# Print the model's response
print(chat_response.choices[0].message.content)

