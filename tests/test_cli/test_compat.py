"""Compatibility tests for the deprecated slate-pro wrapper."""

from __future__ import annotations

import importlib

from slate.cli import app as slate_app
from slate.evidence import build_evidence_bundle
from slate.panel import DEFAULT_PANEL_MODEL
from slate.panel.verdict import EnhancedVerdict
from typer.testing import CliRunner

import slate_pro
import slate_pro.cli as compat_cli
from slate_pro.evidence import build_evidence_bundle as compat_build_evidence_bundle
from slate_pro.panel import DEFAULT_PRO_MODEL
from slate_pro.panel.verdict import EnhancedVerdict as CompatEnhancedVerdict

runner = CliRunner()

COMPAT_MODULES = [
    "slate_pro.evidence.bundle",
    "slate_pro.panel.claude_client",
    "slate_pro.panel.ensemble",
    "slate_pro.panel.fusion",
    "slate_pro.panel.local_ollama_client",
    "slate_pro.panel.personas",
    "slate_pro.panel.personas.animator",
    "slate_pro.panel.personas.audience",
    "slate_pro.panel.personas.base",
    "slate_pro.panel.personas.color_grader",
    "slate_pro.panel.personas.director",
    "slate_pro.panel.prompts",
]


def test_console_script_delegates_to_slate_cli() -> None:
    assert compat_cli.app is slate_app
    result = runner.invoke(compat_cli.app, ["--version"])
    assert result.exit_code == 0
    assert "slate " in result.stdout


def test_import_shims_delegate_to_slate() -> None:
    assert DEFAULT_PRO_MODEL == DEFAULT_PANEL_MODEL
    assert CompatEnhancedVerdict is EnhancedVerdict
    assert compat_build_evidence_bundle is build_evidence_bundle
    assert slate_pro.__version__ == "0.1.0"


def test_all_compatibility_modules_import() -> None:
    for module_name in COMPAT_MODULES:
        module = importlib.import_module(module_name)
        exported = module.__all__
        assert exported
        for name in exported:
            assert hasattr(module, name)
