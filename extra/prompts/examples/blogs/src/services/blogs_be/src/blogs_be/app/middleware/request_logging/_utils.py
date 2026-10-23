import datetime
import hashlib
import logging
import socket

from django.utils.termcolors import colorize

MAX_BODY_LENGTH = 50000  # log no more than 3k bytes of content


def _chunked_to_max(msg):
    if len(msg) > MAX_BODY_LENGTH:
        return "{0}\n...\n".format(msg[0:MAX_BODY_LENGTH])
    else:
        return msg


def _log(msg, logger, level):
    for line in str(msg).split("\n"):
        line = (
            colorize(line, fg="magenta")
            if (level >= logging.ERROR)
            else colorize(line, fg="cyan")
        )
        logger.log(level, line)


def log_request(context, request_method, url, payload):
    chunked_response = _chunked_to_max(str(payload))

    msg = "{} {} {} {} {} {}".format(
        socket.gethostname(),
        datetime.datetime.now(),
        context,
        request_method,
        url,
        hashlib.md5(chunked_response.encode("utf-8")).hexdigest(),
    )
    _log(msg, logging.getLogger("django"), logging.INFO)
    _log(chunked_response, logging.getLogger("django"), logging.INFO)


def log_response(context, request_method, url, response_body, status_code):
    chunked_response = _chunked_to_max(str(response_body))
    msg = "{} {} {} {} {} {} {}".format(
        socket.gethostname(),
        datetime.datetime.now(),
        context,
        request_method,
        url,
        status_code,
        hashlib.md5(chunked_response.encode("utf-8")).hexdigest(),
    )
    _log(
        msg,
        logging.getLogger("django"),
        logging.ERROR if status_code in range(400, 600) else logging.INFO,
    )
    _log(chunked_response, logging.getLogger("django"), logging.INFO)
