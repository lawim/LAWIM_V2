from __future__ import annotations

import json
import unittest

from lawim_v2 import (
    CredentialAuditLogger,
    CredentialEncryptor,
    CredentialMasker,
    CredentialScanner,
    CredentialStatus,
    CredentialValidator,
    CredentialVault,
    GitSecretGuard,
    SecretScanner,
    StorageResourceRegistry,
    StorageSetupWizard,
    build_default_credential_vault,
)


class CredentialVaultAAGTest(unittest.TestCase):
    def test_vault_bootstraps_ten_drive_credentials_with_masked_snapshots(self) -> None:
        registry = StorageResourceRegistry.default()
        vault = registry.credential_vault
        snapshot = vault.snapshot()
        first_record = snapshot["records"][0]

        self.assertEqual(snapshot["summary"]["record_count"], 10)
        self.assertEqual(snapshot["summary"]["active_count"], 10)
        self.assertEqual(first_record["credential_id"], "cred-drive-1")
        self.assertEqual(first_record["role"], "Videos A")
        self.assertEqual(first_record["masked_secret"], "***")
        self.assertTrue(snapshot["monitoring"]["activeCredentials"] >= 1)
        self.assertNotIn("drive.google.com", json.dumps(snapshot))
        self.assertNotIn("client_secret", json.dumps(snapshot))
        self.assertNotIn("refresh_token", json.dumps(snapshot))
        self.assertNotIn("access_token", json.dumps(snapshot))

    def test_encryptor_masker_and_validator_round_trip(self) -> None:
        encryptor = CredentialEncryptor()
        masker = CredentialMasker()
        validator = CredentialValidator()
        vault = build_default_credential_vault()
        record = vault.record_for("cred-drive-1")
        secret = "super-secret-value"
        encrypted = encryptor.encrypt(secret, credential_id="cred-drive-1")
        decrypted = encryptor.decrypt(encrypted, credential_id="cred-drive-1")
        masked = masker.mask_text(f"secret={secret} https://drive.google.com/file/d/abc")
        issues = validator.validate_record(record)

        self.assertEqual(decrypted, secret)
        self.assertNotIn(secret, masked)
        self.assertNotIn("drive.google.com", masked)
        self.assertEqual(issues, [])

    def test_rotation_manager_marks_due_credentials_active_again(self) -> None:
        vault = build_default_credential_vault()
        record = vault.record_for("cred-drive-1")
        record.rotation_due_at = "2026-01-01T00:00:00Z"
        queue = vault.rotation_manager.rotation_queue(vault, now="2026-07-05T10:00:00Z")
        rotated = vault.rotate("cred-drive-1", secret="vault://cred-drive-1/rotated")

        self.assertIn("cred-drive-1", queue)
        self.assertEqual(rotated.rotation_count, 1)
        self.assertEqual(rotated.status, CredentialStatus.ACTIVE)
        self.assertEqual(vault.validator.validate_vault(vault)["valid"], True)

    def test_google_drive_binding_uses_credential_reference_and_vault_counts(self) -> None:
        registry = StorageResourceRegistry.default()
        connector = registry.connector_for("drive-5")
        connection = connector.connect()
        monitoring = connector.monitoring_snapshot()

        self.assertEqual(connector.credential_reference.credential_id, registry.get("drive-5").credential_id)
        self.assertEqual(connector.credential_reference.role, "Conversation Registry")
        self.assertEqual(connection["credential_id"], "cred-drive-5")
        self.assertEqual(monitoring["credentialMonitor"]["recordCount"], 10)
        self.assertIn("credential_vault", registry.google_drive_admin_snapshot())

    def test_secret_scanner_git_guard_and_setup_wizard(self) -> None:
        scanner = SecretScanner()
        git_guard = GitSecretGuard()
        credential_scanner = CredentialScanner()
        registry = StorageResourceRegistry.default()
        wizard = StorageSetupWizard()
        plan = wizard.build_activation_plan(registry)

        findings = scanner.scan_text("client_secret=abc123")
        self.assertGreater(len(findings), 0)
        self.assertFalse(git_guard.is_clean("refresh_token=abc123"))
        with self.assertRaises(ValueError):
            git_guard.assert_clean("secret=abc123")
        self.assertEqual(credential_scanner.scan_vault(registry.credential_vault), [])
        self.assertTrue(plan["activation_ready"])
        self.assertEqual(plan["credential_vault"]["summary"]["record_count"], 10)


if __name__ == "__main__":
    unittest.main()
