"""
Custom exception handlers for DRF.
"""

from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF.
    Formats error responses in a consistent structure:
    {
        "status": "error",
        "error": "error_code",
        "message": "Human readable message",
        "details": {...}
    }
    """
    response = exception_handler(exc, context)

    if response is not None:
        details = response.data
        if (
            isinstance(details, dict)
            and "detail" in details
            and isinstance(details["detail"], str)
        ):
            message = details["detail"]
        elif isinstance(details, list) and details:
            message = " ".join(str(item) for item in details)
        else:
            message = "Request failed."

        response.data = {
            "status": "error",
            "error": exc.__class__.__name__,
            "message": message,
            "details": details,
        }
    return response
