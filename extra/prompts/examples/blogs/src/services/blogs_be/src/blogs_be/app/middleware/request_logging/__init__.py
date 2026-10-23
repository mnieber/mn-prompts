import re

from ._utils import log_request, log_response


def request_logging_middleware(get_response):
    def _log_response(request, response):
        if re.match("^application/json", response.get("Content-Type", ""), re.I):
            log_response(
                "RSP",
                request.method,
                request.get_full_path(),
                response.content,
                response.status_code,
            )

    def middleware(request):
        if request.body:
            log_request("REQ", request.method, request.get_full_path(), request.body)

        response = get_response(request)

        _log_response(request, response)

        return response

    return middleware
