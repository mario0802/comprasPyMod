from __future__ import annotations

from typing import Any

from flask import jsonify
from flask.wrappers import Response


def success_response(
    data: Any = None,
    *,
    message: str = "OK",
    status_code: int = 200,
    meta: dict[str, Any] | None = None,
) -> tuple[Response, int]:
    body: dict[str, Any] = {
        "success": True,
        "message": message,
        "data": data,
    }
    if meta:
        body["meta"] = meta
    return jsonify(body), status_code


def error_response(
    *,
    message: str,
    error_code: str,
    status_code: int = 500,
    details: dict[str, Any] | None = None,
) -> tuple[Response, int]:
    body: dict[str, Any] = {
        "success": False,
        "error_code": error_code,
        "message": message,
    }
    if details:
        body["details"] = details
    return jsonify(body), status_code