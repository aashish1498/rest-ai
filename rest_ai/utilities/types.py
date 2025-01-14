import logging

from pydantic import BaseModel, Field

_valid_verbs = {"GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"}


class RestRequest(BaseModel):
    verb: str = Field(
        description="HTTP verb to use for the request",
        examples=["GET", "POST", "PUT"],
        default="GET",
    )
    query_path: str = Field(
        description="Path to use for the REST request", examples=["/api/v1/users"]
    )
    body: dict | None = Field(
        description="A set of key values to send in the body of the request taken from the openapi spec. Set to None if not applicable",
        default={},
    )
    query_params: dict | None = Field(
        description="A set of key-values to send in the query taken from the openapi spec. Set to None if not applicable.",
        default={},
    )


def validate_rest_request(rest_request: RestRequest) -> RestRequest:
    return RestRequest(
        verb=validate_rest_verb(rest_request.verb),
        query_path=add_preceding_slash(rest_request.query_path),
        body=rest_request.body,
        query_params=rest_request.query_params,
    )


def validate_rest_verb(verb: str) -> str:
    verb = verb.upper().strip()
    if verb not in _valid_verbs:
        logging.warning(f"Invalid verb provided: {verb}. Defaulting to GET.")
        verb = "GET"
    return verb


def add_preceding_slash(path: str) -> str:
    if not path.startswith("/"):
        return "/" + path
    return path
