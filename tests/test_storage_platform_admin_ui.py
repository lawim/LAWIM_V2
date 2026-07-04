from __future__ import annotations

import pathlib
import unittest


class StoragePlatformAdminUITest(unittest.TestCase):
    def test_admin_pages_are_present_in_frontend_sources(self) -> None:
        root = pathlib.Path(__file__).resolve().parents[1]
        backup_center = root / 'frontend' / 'apps' / 'admin' / 'src' / 'BackupCenterPage.tsx'
        backup_manager = root / 'frontend' / 'apps' / 'admin' / 'src' / 'BackupManagerPage.tsx'
        setup_wizard = root / 'frontend' / 'apps' / 'admin' / 'src' / 'StorageSetupWizardPage.tsx'

        self.assertTrue(backup_center.exists())
        self.assertTrue(backup_manager.exists())
        self.assertTrue(setup_wizard.exists())

        backup_center_text = backup_center.read_text(encoding='utf-8')
        self.assertIn('Backup Center', backup_center_text)
        self.assertIn('Admin backup and storage control center', backup_center_text)


if __name__ == "__main__":
    unittest.main()
