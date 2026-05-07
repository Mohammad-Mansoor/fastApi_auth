from typing import Any, Optional


class AppException(Exception):
    """
    AppException is a custom exception used for consistent API error handling
    across the application.

    It helps standardize error responses by providing:
    - HTTP status code
    - Human-readable error message
    - Machine-readable error code
    - Optional extra details for debugging or validation
    """

    def __init__(
        self,
        status_code: int = 500,
        message: str = "Something went wrong",
        error: str = "INTERNAL_ERROR",
        details: Optional[Any] = None
    ) -> None:
        """
        Create a new AppException instance.

        Parameters:
            status_code (int):
                HTTP status code representing the error (e.g. 400, 404, 500)

            message (str):
                Human-readable description of the error

            error (str):
                Internal error code used for debugging or frontend handling
                Example: "VALIDATION_ERROR", "NOT_FOUND"

            details (Any, optional):
                Optional extra data about the error.
                Can be dict, list, or any object (e.g. validation errors)
        """
        super().__init__(message)

        self.status_code = status_code
        self.message = message
        self.error = error
        self.details = details