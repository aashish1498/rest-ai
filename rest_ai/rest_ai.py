import logging

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import PromptTemplate
from requests import Response, request

from rest_ai.exceptions import QueryParsingException
from rest_ai.utilities.config import RETRY_COUNT
from rest_ai.utilities.openapi_utils import format_openapi
from rest_ai.utilities.types import RestRequest, validate_rest_request

from .langchain.prompt_templates import (
    rest_prompt_template,
    rest_prompt_template_with_error,
)


class RestAi:
    base_url: str
    openapi_spec: str
    base_model: BaseChatModel
    chain: any

    def __init__(self, base_url: str, openapi_spec: dict, base_model: BaseChatModel):
        self.base_url = base_url
        self.openapi_spec = format_openapi(openapi_spec)
        self.base_model = base_model

    def invoke(self, prompt: str) -> Response:
        rest_request = self.extract_request(
            rest_prompt_template, {"query": prompt, "openapi_spec": self.openapi_spec}
        )
        response = self.execute_request(rest_request)
        if response.ok:
            return response
        return self.retry_request_extraction(prompt, response, rest_request)

    def retry_request_extraction(
        self, prompt: str, previous_response: Response, previous_request: RestRequest
    ) -> Response:
        for i in range(RETRY_COUNT):
            logging.info(f"Retry Attempt: {str(i + 1)}")
            rest_request = self.extract_request(
                rest_prompt_template_with_error,
                {
                    "query": prompt,
                    "openapi_spec": self.openapi_spec,
                    "previous_request": previous_request.model_dump_json(),
                    "error": previous_response.text,
                },
            )
            response = self.execute_request(rest_request)
            if response.ok:
                return response
            previous_response = response
            previous_request = rest_request
        logging.error("Unable to successfully invoke query.")

    def extract_request(
        self, prompt_template: PromptTemplate, input: dict
    ) -> RestRequest:
        chain = prompt_template | self.base_model.with_structured_output(RestRequest)
        try:
            query = chain.invoke(input)
            if query is None:
                raise Exception("Parsed query is None.")
        except Exception as e:
            raise QueryParsingException(e)
        logging.info(f"Parsed query: {query}")
        return query

    def execute_request(self, rest_request: RestRequest) -> Response:
        rest_request = validate_rest_request(rest_request)
        response = request(
            method=rest_request.verb,
            url=f"{self.base_url}{rest_request.query_path}",
            params=rest_request.query_params,
            json=rest_request.body,
        )
        logging.info(f"Response: {response.text}")
        return response
