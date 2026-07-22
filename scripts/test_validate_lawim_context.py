#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "validate_lawim_context.py"

PASS_PREFIX = "[PASS]"
FAIL_PREFIX = "[FAIL]"


def run_validator(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(root)],
        capture_output=True,
        text=True,
    )


def test_valid_produces_pass() -> None:
    """Run the validator in the real project root — must pass."""
    project_root = Path(__file__).resolve().parents[1]
    result = run_validator(project_root)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    assert result.returncode == 0, f"Expected PASS (exit 0), got exit {result.returncode}"
    lines = result.stdout.strip().splitlines()
    assert any("[PASS]" in l for l in lines), "No [PASS] lines in output"
    print("test_valid_produces_pass PASSED")


def test_missing_file_produces_fail() -> None:
    """Run validator in a temp dir with missing files — must fail."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        scripts_dir = tmp / "scripts"
        scripts_dir.mkdir()
        reports_programs = tmp / "reports" / "programs"
        reports_programs.mkdir(parents=True)
        reports_arch = tmp / "reports" / "architecture"
        reports_arch.mkdir(parents=True)
        adr_dir = reports_arch / "adr"
        adr_dir.mkdir()

        # Create minimal lawim_program_status.yaml
        (tmp / "lawim_program_status.yaml").write_text(
            "project:\n  name: LAWIM\n  current_version: V2\n  target_version: V3\n"
            "  target_architecture: LROS\n  repository_status: active\n"
            "  head: 18de07d2\n  branch: test\n  origin: test\n"
            "architecture:\n  paradigm: test\n  source_of_truth: test\n"
            "  decision_authority: test\n  execution_authority: test\n"
            "  llm_business_decisions_allowed: false\n"
            "  channel_independent_runtime: true\n"
            "  v2_must_remain_operational: true\n"
            "  shadow_migration_required: true\n"
            "programs:\n"
            "  A:\n    name: A\n    status: complete\n    commit: cf633f5f\n"
            "  B:\n    name: B\n    status: complete\n    commit: 46fbbc49\n"
            "  C:\n    name: C\n    status: complete\n    commit: 86b449b9\n"
            "  C5:\n    name: C5\n    status: complete_with_baseline_verification_pending\n"
            "    commit: 18de07d2\n"
            "  D:\n    name: D\n    status: in_progress\n"
        )

        # Create AGENTS.md with required sections
        (tmp / "AGENTS.md").write_text(
            "## 2. Verification pre-modification\n\nsome content\n"
            "## 3. Perimetre LAWIM\n\nNe jamais rediriger spontanement\n"
            "## 4. Separation metier / LLM\n\nLe LLM peut extraire.\nLe LLM ne peut pas decider.\n"
        )

        # Create LAWIM_CONTEXT.md with canonical statements
        (tmp / "LAWIM_CONTEXT.md").write_text(
            "## Appendix: Canonical Statements\n\n"
            "- LAWIM n'est pas un chatbot. LAWIM est une plateforme immobiliere intelligente et operationnelle.\n"
            "- Une conversation ne constitue pas un projet. Un projet est une entite metier persistante.\n"
            "- Un message ne constitue pas une decision. La decision est prise par le moteur metier.\n"
            "- Une decision ne constitue pas une execution. L'execution est realisee par ActionExecutionEngine.\n"
            "- Une execution automatisee ne constitue pas necessairement une preuve reelle. La preuve reelle necessite un test de bout en bout sur canal reel.\n"
            "- Un test unitaire ne prouve pas une integration reelle. L'integration reelle necessite des tests cross-composant et cross-canal.\n"
            "- Un commit ne prouve pas un deploiement. Le deploiement necessite un environnement cible operationnel.\n"
            "- Un service sain ne prouve pas le fonctionnement du parcours metier. Le parcours metier necessite une validation de bout en bout.\n"
        )

        # Create only SOME report files (leave many missing to trigger FAIL)
        for rel in [
            "reports/programs/PROGRAM-A-SUMMARY.md",
            "reports/programs/PROGRAM-C-SUMMARY.md",
            "reports/programs/PROGRAM-C5-STATUS.md",
            "reports/architecture/LAWIM-GLOSSARY.md",
        ]:
            f = tmp / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text("placeholder\n")

        # Create ADR files (only some — ADR-009 missing)
        for i in range(1, 9):
            (adr_dir / f"ADR-{i:03d}-test.md").write_text("placeholder\n")

        # Create validator self-reference
        (scripts_dir / "validate_lawim_context.py").write_text("placeholder\n")

        result = run_validator(tmp)
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)

        assert result.returncode == 1, (
            f"Expected FAIL (exit 1) with missing files, got exit {result.returncode}"
        )
        lines = result.stdout.strip().splitlines()
        fail_lines = [l for l in lines if "[FAIL]" in l]
        assert len(fail_lines) > 0, "Expected [FAIL] lines for missing files"
        print("test_missing_file_produces_fail PASSED")


def test_invalid_commit_produces_fail() -> None:
    """If a commit does not match expected, the validator should fail."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        reports_programs = tmp / "reports" / "programs"
        reports_programs.mkdir(parents=True)
        reports_arch = tmp / "reports" / "architecture"
        reports_arch.mkdir(parents=True)
        adr_dir = reports_arch / "adr"
        adr_dir.mkdir()
        scripts_dir = tmp / "scripts"
        scripts_dir.mkdir()

        # LAWIM_CONTEXT.md
        (tmp / "LAWIM_CONTEXT.md").write_text(
            "## Appendix: Canonical Statements\n\n"
            "- LAWIM n'est pas un chatbot. LAWIM est une plateforme immobiliere intelligente et operationnelle.\n"
            "- Une conversation ne constitue pas un projet. Un projet est une entite metier persistante.\n"
            "- Un message ne constitue pas une decision. La decision est prise par le moteur metier.\n"
            "- Une decision ne constitue pas une execution. L'execution est realisee par ActionExecutionEngine.\n"
            "- Une execution automatisee ne constitue pas necessairement une preuve reelle. La preuve reelle necessite un test de bout en bout sur canal reel.\n"
            "- Un test unitaire ne prouve pas une integration reelle. L'integration reelle necessite des tests cross-composant et cross-canal.\n"
            "- Un commit ne prouve pas un deploiement. Le deploiement necessite un environnement cible operationnel.\n"
            "- Un service sain ne prouve pas le fonctionnement du parcours metier. Le parcours metier necessite une validation de bout en bout.\n"
        )
        (tmp / "AGENTS.md").write_text(
            "## 2. Verification pre-modification\n\n"
            "## 3. Perimetre LAWIM\n\nNe jamais rediriger spontanement\n"
            "## 4. Separation metier / LLM\n\nLe LLM peut extraire.\nLe LLM ne peut pas decider.\n"
        )

        # YAML with wrong commit for Program A
        (tmp / "lawim_program_status.yaml").write_text(
            "project:\n  name: LAWIM\n  current_version: V2\n  target_version: V3\n"
            "  target_architecture: LROS\n  repository_status: active\n"
            "  head: deadbeef\n  branch: test\n  origin: test\n"
            "architecture:\n  paradigm: test\n  source_of_truth: test\n"
            "  decision_authority: test\n  execution_authority: test\n"
            "  llm_business_decisions_allowed: false\n"
            "  channel_independent_runtime: true\n"
            "  v2_must_remain_operational: true\n"
            "  shadow_migration_required: true\n"
            "programs:\n"
            "  A:\n    name: A\n    status: complete\n    commit: WRONG123\n"
            "  B:\n    name: B\n    status: complete\n    commit: 46fbbc49\n"
            "  C:\n    name: C\n    status: complete\n    commit: 86b449b9\n"
            "  C5:\n    name: C5\n    status: complete_with_baseline_verification_pending\n"
            "    commit: 18de07d2\n"
            "  D:\n    name: D\n    status: in_progress\n"
        )

        for rel in [
            "reports/programs/PROGRAM-A-SUMMARY.md",
            "reports/programs/PROGRAM-B-SUMMARY.md",
            "reports/programs/PROGRAM-C-SUMMARY.md",
            "reports/programs/PROGRAM-C5-STATUS.md",
            "reports/programs/PROGRAM-D-SPECIFICATION.md",
            "reports/programs/ROADMAP-V3.md",
            "reports/programs/OPENCODE-SESSION-BOOTSTRAP.md",
            "reports/programs/AGENT-REVIEW-CHECKLIST.md",
            "reports/architecture/LAWIM-GLOSSARY.md",
            "reports/architecture/LAWIM-ARCHITECTURE-MAP.md",
            "reports/architecture/LAWIM-VALIDATION-LEVELS.md",
            "reports/architecture/LAWIM-CONTEXT-AUDIT.md",
        ]:
            f = tmp / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text("placeholder\n")

        for i in range(1, 10):
            (adr_dir / f"ADR-{i:03d}-test.md").write_text("placeholder\n")

        (scripts_dir / "validate_lawim_context.py").write_text("placeholder\n")

        result = run_validator(tmp)
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)

        assert result.returncode == 1, (
            f"Expected FAIL (exit 1) for wrong commit, got exit {result.returncode}"
        )
        assert "mismatch" in result.stdout or "WRONG123" in result.stdout
        print("test_invalid_commit_produces_fail PASSED")


def test_invalid_status_produces_fail() -> None:
    """If a program has an invalid status, validator should fail."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        reports_programs = tmp / "reports" / "programs"
        reports_programs.mkdir(parents=True)
        reports_arch = tmp / "reports" / "architecture"
        reports_arch.mkdir(parents=True)
        adr_dir = reports_arch / "adr"
        adr_dir.mkdir()
        scripts_dir = tmp / "scripts"
        scripts_dir.mkdir()

        (tmp / "LAWIM_CONTEXT.md").write_text(
            "## Appendix: Canonical Statements\n\n"
            "- LAWIM n'est pas un chatbot. LAWIM est une plateforme immobiliere intelligente et operationnelle.\n"
            "- Une conversation ne constitue pas un projet. Un projet est une entite metier persistante.\n"
            "- Un message ne constitue pas une decision. La decision est prise par le moteur metier.\n"
            "- Une decision ne constitue pas une execution. L'execution est realisee par ActionExecutionEngine.\n"
            "- Une execution automatisee ne constitue pas necessairement une preuve reelle. La preuve reelle necessite un test de bout en bout sur canal reel.\n"
            "- Un test unitaire ne prouve pas une integration reelle. L'integration reelle necessite des tests cross-composant et cross-canal.\n"
            "- Un commit ne prouve pas un deploiement. Le deploiement necessite un environnement cible operationnel.\n"
            "- Un service sain ne prouve pas le fonctionnement du parcours metier. Le parcours metier necessite une validation de bout en bout.\n"
        )
        (tmp / "AGENTS.md").write_text(
            "## 2. Verification pre-modification\n\n"
            "## 3. Perimetre LAWIM\n\nNe jamais rediriger spontanement\n"
            "## 4. Separation metier / LLM\n\nLe LLM peut extraire.\nLe LLM ne peut pas decider.\n"
        )

        # YAML with invalid status (COMPLETE vs complete)
        (tmp / "lawim_program_status.yaml").write_text(
            "project:\n  name: LAWIM\n  current_version: V2\n  target_version: V3\n"
            "  target_architecture: LROS\n  repository_status: active\n"
            "  head: deadbeef\n  branch: test\n  origin: test\n"
            "architecture:\n  paradigm: test\n  source_of_truth: test\n"
            "  decision_authority: test\n  execution_authority: test\n"
            "  llm_business_decisions_allowed: false\n"
            "  channel_independent_runtime: true\n"
            "  v2_must_remain_operational: true\n"
            "  shadow_migration_required: true\n"
            "programs:\n"
            "  A:\n    name: A\n    status: COMPLETE\n    commit: cf633f5f\n"
            "  B:\n    name: B\n    status: complete\n    commit: 46fbbc49\n"
            "  C:\n    name: C\n    status: complete\n    commit: 86b449b9\n"
            "  C5:\n    name: C5\n    status: complete_with_baseline_verification_pending\n"
            "    commit: 18de07d2\n"
            "  D:\n    name: D\n    status: in_progress\n"
        )

        for rel in [
            "reports/programs/PROGRAM-A-SUMMARY.md",
            "reports/programs/PROGRAM-B-SUMMARY.md",
            "reports/programs/PROGRAM-C-SUMMARY.md",
            "reports/programs/PROGRAM-C5-STATUS.md",
            "reports/programs/PROGRAM-D-SPECIFICATION.md",
            "reports/programs/ROADMAP-V3.md",
            "reports/programs/OPENCODE-SESSION-BOOTSTRAP.md",
            "reports/programs/AGENT-REVIEW-CHECKLIST.md",
            "reports/architecture/LAWIM-GLOSSARY.md",
            "reports/architecture/LAWIM-ARCHITECTURE-MAP.md",
            "reports/architecture/LAWIM-VALIDATION-LEVELS.md",
            "reports/architecture/LAWIM-CONTEXT-AUDIT.md",
        ]:
            f = tmp / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text("placeholder\n")

        for i in range(1, 10):
            (adr_dir / f"ADR-{i:03d}-test.md").write_text("placeholder\n")

        (scripts_dir / "validate_lawim_context.py").write_text("placeholder\n")

        result = run_validator(tmp)
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)

        assert result.returncode == 1, (
            f"Expected FAIL (exit 1) for invalid status, got exit {result.returncode}"
        )
        assert "COMPLETE" in result.stdout
        print("test_invalid_status_produces_fail PASSED")


if __name__ == "__main__":
    tests = [
        ("valid_produces_pass", test_valid_produces_pass),
        ("missing_file_produces_fail", test_missing_file_produces_fail),
        ("invalid_commit_produces_fail", test_invalid_commit_produces_fail),
        ("invalid_status_produces_fail", test_invalid_status_produces_fail),
    ]
    failed = 0
    for name, fn in tests:
        print(f"\n--- {name} ---")
        try:
            fn()
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"[FAIL] {name}: {e}")
            failed += 1
    if failed:
        print(f"\n{len(tests) - failed}/{len(tests)} passed, {failed} failed")
        sys.exit(1)
    else:
        print(f"\nAll {len(tests)} tests PASSED")
