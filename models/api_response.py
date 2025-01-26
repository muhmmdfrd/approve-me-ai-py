from dataclasses import dataclass
from typing import Generic, TypeVar, Optional

T = TypeVar('T')

@dataclass
class ApiResponse(Generic[T]):
    message: str
    success: bool
    data: Optional[T] = None