from rest_framework import status
from rest_framework.response import Response


def success_response(data=None, message="", http_status=status.HTTP_200_OK):
    payload = {"status": "success"}
    if message:
        payload["message"] = message
    if data is not None:
        payload["data"] = data
    return Response(payload, status=http_status)


def error_response(
    message,
    *,
    details=None,
    error_code="validation_error",
    http_status=status.HTTP_400_BAD_REQUEST,
):
    payload = {
        "status": "error",
        "error": error_code,
        "message": message,
    }
    if details is not None:
        payload["details"] = details
    return Response(payload, status=http_status)
