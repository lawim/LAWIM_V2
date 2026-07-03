from __future__ import annotations

import os
from unittest import TestCase
from unittest.mock import MagicMock, patch

from lawim_v2.security.credentials import PBKDF2_ITERATIONS, TEST_PBKDF2_ITERATIONS, hash_password


class SecurityCredentialsTest(TestCase):
    @patch("lawim_v2.security.credentials.hashlib.pbkdf2_hmac")
    def test_hash_password_uses_production_iterations_by_default(self, pbkdf2_hmac: MagicMock) -> None:
        pbkdf2_hmac.return_value = b"\x00" * 32
        with patch.dict(os.environ, {}, clear=True):
            hash_password("lawim-demo", salt=b"0123456789abcdef")
        self.assertEqual(pbkdf2_hmac.call_args.args[3], PBKDF2_ITERATIONS)

    @patch("lawim_v2.security.credentials.hashlib.pbkdf2_hmac")
    def test_hash_password_uses_test_iterations_when_enabled(self, pbkdf2_hmac: MagicMock) -> None:
        pbkdf2_hmac.return_value = b"\x00" * 32
        with patch.dict(os.environ, {"LAWIM_TEST_MODE": "1"}, clear=True):
            hash_password("lawim-demo", salt=b"0123456789abcdef")
        self.assertEqual(pbkdf2_hmac.call_args.args[3], TEST_PBKDF2_ITERATIONS)
