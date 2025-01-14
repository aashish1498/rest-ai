import jsonref
from rest_ai.utilities.openapi_utils import format_openapi, remove_keys

def test_format_openapi_with_json_references():
    openapi_spec = {
        "paths": {
            "/example": {
                "$ref": "#/components/schemas/Example"
            }
        },
        "components": {
            "schemas": {
                "Example": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"}
                    }
                }
            }
        }
    }
    
    expected_result = {
        "paths": {
            "/example": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                }
            }
        }
    }
    
    result = format_openapi(openapi_spec)
    assert jsonref.loads(result) == expected_result

def test_format_openapi_removes_specified_keys():
    openapi_spec = {
        "paths": {
            "/example": {
                "get": {
                    "responses": {
                        "200": {"description": "OK"}
                    },
                    "operationId": "getExample"
                }
            }
        },
        "components": {
            "schemas": {
                "Example": {
                    "type": "object"
                }
            }
        }
    }
    
    expected_result = {
        "paths": {
            "/example": {
                "get": {}
            }
        }
    }
    
    result = format_openapi(openapi_spec)
    assert jsonref.loads(result) == expected_result

def test_remove_keys():
    input_data = {
        "paths": {
            "/example": {
                "get": {
                    "responses": {
                        "200": {"description": "OK"}
                    },
                    "operationId": "getExample",
                    "summary": "An example endpoint"
                }
            }
        },
        "components": {
            "schemas": {
                "Example": {
                    "type": "object"
                }
            }
        }
    }
    
    keys_to_remove = ["responses", "components", "operationId"]
    expected_output = {
        "paths": {
            "/example": {
                "get": {
                    "summary": "An example endpoint"
                }
            }
        }
    }
    
    result = remove_keys(input_data, keys_to_remove)
    assert result == expected_output
