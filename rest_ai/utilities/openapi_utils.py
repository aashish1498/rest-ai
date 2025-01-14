import json
import jsonref


def format_openapi(openapi_spec: dict) -> str:
    expanded_openapi = jsonref.loads(json.dumps(openapi_spec), proxies=False)
    simplified = remove_keys(
        expanded_openapi, ["responses", "components", "operationId"]
    )
    return json.dumps(simplified)


def remove_keys(obj: dict | list, keys_to_remove: list[str]):
    if isinstance(obj, dict):
        for key in keys_to_remove:
            if key in obj:
                del obj[key]
        for _, value in obj.items():
            remove_keys(value, keys_to_remove)
    elif isinstance(obj, list):
        for item in obj:
            remove_keys(item, keys_to_remove)
    return obj
