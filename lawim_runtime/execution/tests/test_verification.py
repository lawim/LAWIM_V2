from __future__ import annotations

from lawim_runtime.execution.verification import ExecutionVerifier, VerificationStatus


class TestExecutionVerifier:
    def test_empty_output_inconclusive(self):
        verifier = ExecutionVerifier()
        result = verifier.verify("test", {})
        assert result.status == VerificationStatus.INCONCLUSIVE

    def test_pass_without_expected(self):
        verifier = ExecutionVerifier()
        result = verifier.verify("test", {"key": "val"})
        assert result.status == VerificationStatus.PASSED

    def test_pass_with_matching_expected(self):
        verifier = ExecutionVerifier()
        result = verifier.verify("test", {"key": "val"}, expected={"key": "val"})
        assert result.status == VerificationStatus.PASSED

    def test_fail_with_mismatch(self):
        verifier = ExecutionVerifier()
        result = verifier.verify("test", {"key": "wrong"}, expected={"key": "val"})
        assert result.status == VerificationStatus.FAILED
