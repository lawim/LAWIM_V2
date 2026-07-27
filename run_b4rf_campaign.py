#!/usr/bin/env python3
"""Wrapper to run B.4R-F campaign with proper PYTHONPATH."""
import os
import sys

base = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base)
sys.path.insert(0, os.path.join(base, "lawim_runtime"))
sys.path.insert(0, os.path.join(base, "code"))
os.environ["LAWIM_VAULT_KEY"] = "test-key-123"

# Run the campaign
campaign = os.path.join(base, "tests/gold_corpus/certification/campaigns/run_b4rf_idempotence_restart.py")
with open(campaign) as f:
    exec(f.read(), {"__name__": "__main__", "__file__": campaign})
