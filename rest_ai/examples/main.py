import yaml
import json
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser


def openapi_to_custom_json_schema(openapi_spec: dict):
    schemas = []
    for path_key in openapi_spec["paths"].keys():
        path = openapi_spec["paths"][path_key]
        for method_key in path.keys():
            method = path[method_key]
            

        # path = list(openapi_spec["paths"].keys())[0]
        # method = list(openapi_spec["paths"][path].keys())[0]
        # operation = openapi_spec["paths"][path][method]

        # Extract query parameters
            query_params = {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            }

            for param in method.get("parameters", []):
                if param["in"] == "query":
                    query_params["properties"][param["name"]] = param["schema"]
                    if param.get("required", False):
                        query_params["required"].append(param["name"])

            body_schema = (
                method.get("requestBody", {})
                .get("content", {})
                .get("application/json", {})
                .get("schema", {})
            )

        # Construct the custom JSON schema
            custom_json_schema = {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "enum": [path_key]},
                    "method": {"type": "string", "enum": [method_key.upper()]},
                    "query_params": query_params,
                    "body": body_schema,
                },
                "required": ["path", "method", "query_params"],
                "additionalProperties": False,
            }
            
            schemas.append(custom_json_schema)

    
    final_schema = {
        "title": "",
        "description": "",
        "type": "object",
        "oneOf": schemas,
    }
    
    with open ("schema.json", "w") as f:
        f.write(json.dumps(final_schema, indent=4))
    
    return final_schema
    return json.dumps(final_schema, indent=4)


# Example usage
openapi_yaml = """
openapi: 3.0.3
info:
  title: Test API
  version: 1.0.0
paths:
  /api/test:
    post:
      summary: Test endpoint
      parameters:
        - name: number_of_dogs
          in: query
          required: true
          schema:
            type: integer
          description: The number of dogs.
        - name: pet_names
          in: query
          required: false
          schema:
            type: array
            items:
              type: string
          description: An optional list of pet names.
      requestBody:
        required: false
        content:
          application/json:
            schema:
              type: object
              properties:
                top_name:
                  type: string
                  description: The top name.
                details:
                  type: object
                  properties:
                    breed:
                      type: string
                      description: The breed of the pet.
                    fleas:
                      type: boolean
                      description: Indicates if the pet has fleas.
                    status:
                      type: string
                      enum: [walking, running, resting]
                      description: The status of the pet.
"""

# https://python.langchain.com/docs/how_to/structured_output/
if __name__ == "__main__":
    openapi_spec = yaml.safe_load(openapi_yaml)
    schema = (openapi_to_custom_json_schema(openapi_spec))
    model = ChatOllama(
        base_url="localhost:11434",
        model='qwen2.5:3b',
        temperature=0,
    ).with_structured_output(schema)
    prompt_template = PromptTemplate.from_template(
        """
        Turn the following user request into a REST API request:
        
        {query}
        """
    )
    chain = prompt_template | model | StrOutputParser()
    print(model.invoke("Write me a request to get info of dogs named Marlon with no fleas"))
    # print(chain.invoke({"query": "Write me a request to get info of dogs named Marlon with no fleas"}))
