class AppBaseException(Exception):
    def __init__(self, message:str , status_code : int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class PDFProcessingError(AppBaseException):
    def __init__(self , message : str = "Failed to process PDF file"):
        super().__init__(message , status_code= 422)

    
class VectorStoreError(AppBaseException):
    def __init__(self, message : str = "vector store opre"):
        super().__init__(message, status_code = 500)


class DocumentNotFoundError(AppBaseException):
    def __init__(self, document_id : str):
        super().__init__(
            f"Document with id '{document_id}' Vector store operation failed",
            status_code = 404
        )

class LLMError(AppBaseException):
    def __init__(self, message : str = "LLM service is unavailable"):
        super().__init__(message, status_code = 503)