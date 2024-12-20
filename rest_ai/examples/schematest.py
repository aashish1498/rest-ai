schema = {
    "type": "object",
    "oneOf": [
        {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "enum": [
                        "/api/test"
                    ]
                },
                "method": {
                    "type": "string",
                    "enum": [
                        "POST"
                    ]
                },
                "query_params": {
                    "type": "object",
                    "properties": {
                        "number_of_dogs": {
                            "type": "integer"
                        },
                        "pet_names": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        }
                    },
                    "required": [
                        "number_of_dogs"
                    ],
                    "additionalProperties": false
                },
                "body": {
                    "type": "object",
                    "properties": {
                        "top_name": {
                            "type": "string",
                            "description": "The top name."
                        },
                        "details": {
                            "type": "object",
                            "properties": {
                                "breed": {
                                    "type": "string",
                                    "description": "The breed of the pet."
                                },
                                "fleas": {
                                    "type": "boolean",
                                    "description": "Indicates if the pet has fleas."
                                },
                                "status": {
                                    "type": "string",
                                    "enum": [
                                        "walking",
                                        "running",
                                        "resting"
                                    ],
                                    "description": "The status of the pet."
                                }
                            }
                        }
                    }
                }
            },
            "required": [
                "path",
                "method",
                "query_params"
            ],
            "additionalProperties": false
        }
    ]
}