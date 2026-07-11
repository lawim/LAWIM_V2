#!/usr/bin/env bash
# LAWIM V2 — Run All Tests
set -euo pipefail

cd "$(dirname "$0")/../.."
echo "=== LAWIM V2 Test Suite ==="

# Backend tests
echo "--- Backend tests ---"
PYTHONPATH=code python3 -m pytest code/lawim_v2/brain/tests.py -v 2>/dev/null || \
PYTHONPATH=code python3 -c "
import sys; sys.path.insert(0,'code')
import unittest
from lawim_v2.brain.tests import *
loader = unittest.TestLoader()
suite = unittest.TestSuite()
for cls in [TestIntentEngine, TestProgressionEngine, TestResumeEngine,
            TestAccompanimentEngine, TestScenarioSimulations,
            TestRelationEngine, TestReadinessCheck]:
    suite.addTests(loader.loadTestsFromTestCase(cls))
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
"

echo "--- Frontend tests ---"
(cd frontend && npm test -- --run)

echo "=== All tests passed ==="
