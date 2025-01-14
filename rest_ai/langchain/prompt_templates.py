from langchain_core.prompts import PromptTemplate

rest_prompt_template = PromptTemplate.from_template(
    """
        Create a valid REST API request based on the user's query. Use the openapi_spec provided to provide the method, query, body and parameters.
        
        query: {query}
        
        openapi_spec: {openapi_spec}
        """
)

rest_prompt_template_with_error = PromptTemplate.from_template(
    """
        Create a valid REST API request based on the user's query. Use the openapi_spec. A previous request was made and it resulted in an error. Use the error message to correct the request.
        
        query: {query}
        
        previous request: {previous_request}
        
        previous_error: {error}
        
        openapi_spec: {openapi_spec}
        """
)
