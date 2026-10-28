import re

import ollama
import pyttsx3

try:
    engine = pyttsx3.init()
except Exception as exc:
    print(f"Text-to-speech unavailable: {exc}")
    engine = None



def get_model_name():
    try:
        installed = {model.model for model in ollama.list().models}
    except Exception:
        installed = set()

    for candidate in ("llama3.2:1b", "llama3.2:latest", "llama3.2"):
        if candidate in installed:
            return candidate

    return "llama3.2"


# Ollama can take longer than 30 seconds to generate a response,
# especially on a local CPU model. Give it a much longer timeout so
# the chat loop can actually receive the reply.
client = ollama.Client(timeout=300)
MODEL_NAME = get_model_name()

system_prompt = '''
You are Jerry, act like a friend.
the user is named master, and you are a helpful assistant.
so say master in your responses, and be friendly and helpful.
speak in a oltimey speech line in middle ages.
act super smart.
'''


chat_history = [
    {
        "role": "system",
        "content": system_prompt,
    },
]

while True:
    prompt = input("hi im jerry you need help with anything: ")

    if prompt.strip().lower() == "exit":
        break

    chat_history.append({
        "role": "user",
        "content": prompt,
    })

    try:
        response = client.chat(
            model=MODEL_NAME,
            keep_alive=300,
            messages=chat_history,
            options={"temperature": 0, "num_procs": 4},
        )

        prompt_tokens = response.get('prompt_eval_count', 0)
        generation_tokens = response.get('eval_count', 0)
        total_tokens_used = prompt_tokens + generation_tokens

        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Generation tokens: {generation_tokens}")
        print(f"total_tokens: {total_tokens_used}")

    except Exception as exc:
        print(f"Sorry, I couldn't reach the AI right now: {exc}")
        chat_history.pop()
        if engine is not None:
            engine.say("The AI is unavailable right now. Please try again.")
            engine.runAndWait()
        continue

    if "message" not in response or "content" not in response["message"]:
        print("The AI returned an unexpected response.")
        chat_history.pop()
        continue

    response_text = response["message"]["content"].strip()
    response_text = re.sub(
        r"\bit(?:['’]?s| is)\s+tome\b",
        lambda match: "It's time" if match.group(0)[0].isupper() else "it's time",
        response_text,
        flags=re.IGNORECASE,
    )
    response["message"]["content"] = response_text
    chat_history.append(response["message"])

    print(response_text)
    if engine is not None:
        engine.say(response_text)
        engine.runAndWait()

    print("=" * 24)
    print("")
    # Remove the '#' from the next line if you want to see the
    # entire chat history
    # print(chat_history)


# Two datatypes to discuss
#   lists []
#   dictionaries {}


#  List - collection of things
#       - ["apple", "banana", "cherry"]
#       - [ 
#           12,
#           20, 
#           24, 
#         ] 
        

# Dictionary - collection of attributes
#              with a "key" and "value" pair

#            - {"name": "Bob", "level": 10}
#            - { 
#               "class": "wizard",
#               "hitpoints": 120,
#               "mana": 200
#
#              }

