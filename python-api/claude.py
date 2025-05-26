#!/usr/bin/python

import anthropic
import dotenv
import os

dotenv.load_dotenv()
my_api_key = os.getenv("my_api_key")

client = anthropic.Anthropic(
    api_key=my_api_key
)
def send_message(messages_array):
  message = client.messages.create(
      model="claude-opus-4-20250514",
      max_tokens=1024,
      messages=messages_array,
      #tools=[{
      #    "type": "web_search_20250305",
      #    "name": "web_search",
      #    "max_uses": 1,
      #    "allowed_domains": ["github.com"],
      #}]
  )
  return message

messages_array=[]
messages_array.append({"role": "user", "content": "what is one plus one"})
foo = send_message(messages_array)

# Add Claude's response to the history
messages_array.append({"role": "assistant", "content": foo.content[0].text})
print(messages_array)
print("\n\n")

messages_array.append({"role": "user", "content": "answer in binary"})
print(messages_array)
foo2 = send_message(messages_array)
print("\n\n")
print(foo2.content[0].text)
