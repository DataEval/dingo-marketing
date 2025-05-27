"""
Core module for Dingo Marketing system.
Provides base functionality, exceptions, logging, and utilities.
"""

from .exceptions import *
from .logging import setup_logging
from .utils import *

__all__ = [
    'DingoException',
    'ValidationError', 
    'APIError',
    'ConfigurationError',
    'setup_logging',
    'get_logger',
    'format_datetime',
    'safe_json_loads',
    'retry_async',
] 