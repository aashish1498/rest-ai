# REST AI

Leverage AI to parse human language to REST API calls.

## Description

**Note: this package is still in development. There will be features not yet available, but contributions are welcome.**

Features:
- Translates plain language to rest api requests using an openapi schema
- Invokes the request, and verifies a correct response
- Uses reasoned retry logic to try and correct invalid requests

Find out more about the package at https://aashishmehta.com/rest-ai-queries-making-apis-smarter/

## Installation

`pip install rest-ai`

## Usage

To use this package, you must have:
- An Openapi schema (loaded as a python dictionary)
- Access to a langchain ChatModel that supports structured outputs
- Details of the API endpoint to call

## Examples

```python
from rest_ai import RestAi
import json
import logging
import sys
from langchain_ollama import ChatOllama

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

base_url = "http://localhost:8000"
file_path = "/path/to/openapi.json"

with open(file_path, "r", encoding="utf-8") as file:
    openapi_spec = file.read()
    openapi_spec = json.loads(openapi_spec)

base_model = ChatOllama(
    base_url="localhost:11434",
    model="llama3.2:3b",
    temperature=0,
)

rest_ai_controller = RestAi(base_url, openapi_spec, base_model)

while True:
    user_input = input("Enter a command to parse into REST API call (or 'exit' to quit): ")
    
    if user_input.lower() == 'exit':
        break
    
    response = rest_ai_controller.invoke(user_input)
    if response:
        print("Response: ")
        print(response.json())
```
