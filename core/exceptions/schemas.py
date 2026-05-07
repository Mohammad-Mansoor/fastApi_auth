from pydantic import BaseModel


from typing import Any, Optional

class ErrorResponse(BaseModel):
    success: bool = False
    statusCode: int
    message: str
    error: Optional[str] = None
    details: Optional[any] = None