from __future__ import annotations

from http import HTTPStatus


class RepositoryError(ValueError):
    status = HTTPStatus.INTERNAL_SERVER_ERROR
    code = "repository_error"


class NotFoundError(RepositoryError):
    status = HTTPStatus.NOT_FOUND
    code = "not_found"


class ConflictError(RepositoryError):
    status = HTTPStatus.CONFLICT
    code = "conflict"


class ValidationError(RepositoryError):
    status = HTTPStatus.BAD_REQUEST
    code = "invalid_state"
