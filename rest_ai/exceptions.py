class QueryParsingException(Exception):
    """Exception raised when a query cannot be parsed into a Rest Request."""

    def __init__(self, message: str):
        self.message = f"""
Unable to parse query into a Rest Request.

Potential reasons:
    - Provided ChatModel is too small or does not support structured outputs`
    - Provided OpenAPI is too vague or large
    
Error message: {message}
"""
        super().__init__(self.message)
