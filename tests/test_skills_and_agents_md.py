from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_agents_md():
    p = ROOT / "AGENTS.md"
    assert p.exists()
    text = p.read_text()
    assert "verify" in text.lower()
    assert "HOTL" in text or "fail closed" in text.lower() or "AgentFence" in text

def test_skills():
    expected = ["agentfence", "x402-payments", "multi-agent-workflow", "cost-control", "governance-hotl"]
    for name in expected:
        f = ROOT / "skills" / name / "SKILL.md"
        assert f.exists(), name
        text = f.read_text()
        assert text.startswith("---")
        assert f"name: {name}" in text or name in text
