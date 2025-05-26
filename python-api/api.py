from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import git
import asyncio
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import anthropic
from dotenv import load_dotenv
import os
import sys
import shutil

# Initialize Flask application
app = Flask(__name__)

load_dotenv()
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
print("sending message")
foo = send_message(messages_array)

# Add Claude's response to the history
messages_array.append({"role": "assistant", "content": foo.content[0].text})
print(messages_array)
print("\n\n")


# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*", "allow_headers": ["Content-Type", "Authorization"]}})

# Alternatively, for more specific CORS configuration:
# CORS(app, resources={r"/foo": {"origins": ["http://localhost:3000", "https://yourdomain.com"]}})

# Define the /foo endpoint that accepts both GET and POST
@app.route('/foo', methods=['GET', 'POST', 'OPTIONS'])
def foo():
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return build_cors_preflight_response()
    
    # Process the actual request
### MATCH KubeResource HAS Label WHERE KubeResource.name CONTAINS 'swapi'
    elif request.method == 'POST':
        # For POST requests, return the data that was sent
        received_data = request.get_json(force=True)
        policy_name = received_data['entities'][0]['policies'][0]['name']
        deployment_name = received_data['entities'][0]['policyEvents'][0]['eventLabels']['kubernetes.deployment.name'],
        git.Repo.clone_from("https://github.com/codecowboydotio/swapi-json-server","/tmp/foo") 
        response = jsonify({
            #"1-test": received_data['entities'][0]['policies'][0]['name'],
            "image_name": received_data['entities'][0]['policyEvents'][0]['eventLabels']['container.image.repo'],
            "deployment_name": received_data['entities'][0]['policyEvents'][0]['eventLabels']['kubernetes.deployment.name'],
            "status": "success",
            "message": "Data received successfully",
            #"received_data": received_data,
            "data_type": str(type(received_data)),
        })
        try:
          mydir="/tmp/foo"
          shutil.rmtree(mydir)
        except OSError as e:
          print("Error: %s - %s." % (e.filename, e.strerror))
        return response
    
    else:
        # For GET requests, return the original response
        response = jsonify({
            "status": "success",
            "message": "Here is your answer!",
            "data": {
                "answer": 42,
                "description": "The Answer to the Ultimate Question of Life, the Universe, and Everything"
            }
        })
        return response

# Helper function for preflight response
def build_cors_preflight_response():
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
    return response

# Run the application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
