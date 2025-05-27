"""
Custom exceptions for Dingo Marketing system.
"""

from typing import Optional, Dict, Any


class DingoException(Exception):
    """Base exception for Dingo Marketing system."""
    
    def __init__(self, message: str, code: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.code = code or self.__class__.__name__
        self.details = details or {}


class ValidationError(DingoException):
    """Raised when data validation fails."""
    pass


class APIError(DingoException):
    """Raised when external API calls fail."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, response_data: Optional[Dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class ConfigurationError(DingoException):
    """Raised when configuration is invalid or missing."""
    pass


class GitHubAPIError(APIError):
    """Raised when GitHub API calls fail."""
    pass


class OpenAIAPIError(APIError):
    """Raised when OpenAI API calls fail."""
    pass


class RateLimitError(APIError):
    """Raised when API rate limits are exceeded."""
    pass


class AuthenticationError(DingoException):
    """Raised when authentication fails."""
    pass


class NotFoundError(DingoException):
    """Raised when requested resource is not found."""
    pass 