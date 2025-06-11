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
import logging

# Initialize Flask application
app = Flask(__name__)

# Load the environment variables from the .env file.
load_dotenv()
my_api_key = os.getenv("my_api_key")

# Initialize the array for the conversation between the LLM and the agent
messages_array=[]


# Create a new anthropic client
client = anthropic.Anthropic(
    api_key=my_api_key
)


# Function to send messages to the LLM. 
#This only requires BOTH the question and the answer to be added to the messages array.
# 
# The example below appends a message to the array and asks a question
#   messages_array.append({"role": "user", "content": "what is one plus one"})
#   foo = send_message(messages_array)
#
# In order to add the response, add the response from the question to the array.
#   messages_array.append({"role": "assistant", "content": foo.content[0].text})
# 
# Each Q/A pair will be appended and the conversation history will be maintained. 
# There is a tradeoff between the size of the context window and the size of the array per Q/A thread.



def send_message(messages_array):
  message = client.beta.messages.create(
      model="claude-opus-4-20250514",
      max_tokens=1024,
      messages=messages_array,
      #tools=[{
      #    "type": "web_search_20250305",
      #    "name": "web_search",
      #    "max_uses": 3,
      #    #"allowed_domains": ["github.com"],
      #}],
      #mcp_servers=[{
      #  "type": "url",
      #  "url": "https://someurl.com",
      #  "name": "example-mcp",
      #}],
      #betas=["mcp-client-2025-04-04"]
  )
  return message


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%y-%m-%d %H:%M',
                    filename='./myapp.log',
                    filemode='w')
api_error_log = logging.getLogger('api.errors')


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
        try:
          git.Repo.clone_from("https://github.com/codecowboydotio/swapi-json-server","/tmp/foo") 
        except:
          response = jsonify({
            "status": "error",
            "message": "There was a problem cloning the repo",
        })
        messages_array.append({"role": "user", "content": "what is one plus one"})
        print("sending message")
        foo = send_message(messages_array)
        
        # Add Claude's response to the history
        messages_array.append({"role": "assistant", "content": foo.content[0].text})
        print(messages_array)
        print("\n\n")

        response = jsonify({
            #"1-test": received_data['entities'][0]['policies'][0]['name'],
            "image_name": received_data['entities'][0]['policyEvents'][0]['eventLabels']['container.image.repo'],
            "deployment_name": received_data['entities'][0]['policyEvents'][0]['eventLabels']['kubernetes.deployment.name'],
            "status": "success",
            "message": "Data received successfully",
            "ai convo": messages_array,
            #"received_data": received_data,
            #"data_type": str(type(received_data)),
        })
        try:
          mydir="/tmp/foo"
          shutil.rmtree(mydir)
        except OSError as e:
          print("Error: %s - %s." % (e.filename, e.strerror))
          api_error_log.debug('Testing debug')
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
