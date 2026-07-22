from __future__ import annotations

from lawim_runtime.execution.failure import ErrorCategory, ExecutionFailure, FailureClassifier


class _CustomError(Exception):
    pass


class TestFailureClassifier:
    def test_classify_timeout_exception(self):
        classifier = FailureClassifier()
        failure = classifier.classify(TimeoutError("timed out"))
        assert failure.error_category == ErrorCategory.TIMEOUT_FAILURE
        assert failure.is_retryable is True

    def test_classify_value_error(self):
        classifier = FailureClassifier()
        failure = classifier.classify(ValueError("bad value"))
        assert failure.error_category == ErrorCategory.INTERNAL_BUG
        assert failure.is_retryable is False

    def test_classify_permission(self):
        classifier = FailureClassifier()
        failure = classifier.classify(PermissionError("access denied"))
        assert failure.error_category == ErrorCategory.AUTHORIZATION_FAILURE
        assert failure.is_retryable is False

    def test_classify_connection_error(self):
        classifier = FailureClassifier()
        failure = classifier.classify(ConnectionError("refused"))
        assert failure.error_category == ErrorCategory.DEPENDENCY_FAILURE
        assert failure.is_retryable is True

    def test_classify_custom_error(self):
        classifier = FailureClassifier()
        failure = classifier.classify(_CustomError("something"))
        assert failure.error_category == ErrorCategory.EXTERNAL_UNKNOWN
        assert failure.is_retryable is True

    def test_error_code_format(self):
        classifier = FailureClassifier()
        failure = classifier.classify(ValueError("test"))
        assert failure.error_code == "INTERNAL_BUG.ValueError"

    def test_extract_details(self):
        classifier = FailureClassifier()
        exc = ValueError("bad", "data")
        failure = classifier.classify(exc)
        assert failure.details["exception_type"] == "ValueError"
        assert "bad" in failure.details["args"]

    def test_find_cause(self):
        classifier = FailureClassifier()
        inner = ValueError("inner")
        outer = RuntimeError("outer")
        outer.__cause__ = inner
        failure = classifier.classify(outer)
        assert "inner" in failure.cause

    def test_unknown_error_retryable(self):
        classifier = FailureClassifier()
        failure = classifier.classify(_CustomError("weird"))
        assert failure.is_retryable is True

    def test_execution_failure_basic(self):
        failure = ExecutionFailure(
            execution_id="exec-1",
            error_category=ErrorCategory.BUSINESS_FAILURE,
            error_code="BUS-001",
            message="Business rule violated",
        )
        assert failure.failure_id
        assert failure.execution_id == "exec-1"
        assert failure.timestamp
