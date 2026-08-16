from typer.testing import CliRunner
from openmesha.cli import app

runner = CliRunner()

def test_version():
    r = runner.invoke(app, ["version"])
    assert r.exit_code == 0
    assert "OpenMesha" in r.stdout

def test_help():
    r = runner.invoke(app, ["--help"])
    assert r.exit_code == 0
    assert "agents" in r.stdout
