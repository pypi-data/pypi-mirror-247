"""
Initializing the Python package
"""

from .auth import detect_type, auth, token
from .users import get


__version__ = '0.10'

__all__ = (
    '__version__',
    'detect_type',
    'auth',
    'token',
    'get',
)
