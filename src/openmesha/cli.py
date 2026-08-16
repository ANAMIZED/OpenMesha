"""OpenMesha CLI — operator surface for humans and scripts."""
from __future__ import annotations
import json
import typer
from rich import print as rprint
from rich.table import Table
from openmesha import __version__
from openmesha.kernel.models import AgentCreate, WorkflowCreate
from openmesha.sdk.client import OpenMeshaClient

app = typer.Typer(name="openmesha", help="OpenMesha — Open Agentic Operations Mesh CLI", no_args_is_help=True)
agents_app = typer.Typer(help="Manage agent processes")
app.add_typer(agents_app, name="agents")

def _client(base: str) -> OpenMeshaClient:
    return OpenMeshaClient(base)

@app.command()
def version():
    rprint(f"OpenMesha {__version__}")

@app.command()
def status(base_url: str = typer.Option("http://localhost:8080", "--url", "-u")):
    try:
        with _client(base_url) as c:
            h = c.health()
            m = c.metrics()
            rprint(f"[green]OK[/green]  {h}")
            table = Table(title="Metrics")
            table.add_column("Metric"); table.add_column("Value")
            for k, v in m.items():
                table.add_row(k, str(v))
            rprint(table)
    except Exception as e:
        rprint(f"[red]Cannot reach OpenMesha at {base_url}: {e}[/red]")
        raise typer.Exit(1)

@agents_app.command("list")
def agents_list(base_url: str = typer.Option("http://localhost:8080", "--url", "-u")):
    with _client(base_url) as c:
        agents = c.list_agents()
        if not agents:
            rprint("No agents."); return
        table = Table(title="Agent Processes")
        table.add_column("ID"); table.add_column("Name"); table.add_column("Status")
        table.add_column("Spend / Budget"); table.add_column("Capabilities")
        for a in agents:
            table.add_row(a.id, a.name, str(a.status.value if hasattr(a.status, "value") else a.status),
                          f"${a.spent_usd:.4f} / ${a.budget_usd:.2f}", ", ".join(a.capabilities))
        rprint(table)

@agents_app.command("create")
def agents_create(
    name: str = typer.Argument(...),
    intent: str = typer.Option(..., "--intent", "-i"),
    budget: float = typer.Option(0.5, "--budget", "-b"),
    capabilities: str = typer.Option("web_search,memory_read,memory_write", "--caps", "-c"),
    model: str = typer.Option("mock-gpt", "--model", "-m"),
    base_url: str = typer.Option("http://localhost:8080", "--url", "-u"),
):
    caps = [x.strip() for x in capabilities.split(",") if x.strip()]
    body = AgentCreate(name=name, intent=intent, budget_usd=budget, model=model, capabilities=caps)
    with _client(base_url) as c:
        agent = c.create_agent(body)
        rprint(f"[green]Created[/green] {agent.id}  ({agent.name})")

@agents_app.command("run")
def agents_run(agent_id: str = typer.Argument(...), goal: str = typer.Argument(...),
               base_url: str = typer.Option("http://localhost:8080", "--url", "-u")):
    with _client(base_url) as c:
        task = c.run_task(agent_id, goal)
        rprint(f"Status: {task.status}")
        if task.result: rprint(f"Result: {task.result}")
        if task.error: rprint(f"[red]Error: {task.error}[/red]")

@app.command()
def ledger(base_url: str = typer.Option("http://localhost:8080", "--url", "-u")):
    with _client(base_url) as c:
        rprint(json.dumps(c.cost_ledger(), indent=2))

@app.command()
def audit(base_url: str = typer.Option("http://localhost:8080", "--url", "-u")):
    with _client(base_url) as c:
        rprint(json.dumps(c.audit_log(), indent=2))

@app.command()
def workflow(
    name: str = typer.Option("cli-wf", "--name"),
    goal: str = typer.Option(..., "--goal", "-g"),
    agents: str = typer.Option("planner,researcher", "--agents", "-a"),
    budget: float = typer.Option(1.0, "--budget", "-b"),
    base_url: str = typer.Option("http://localhost:8080", "--url", "-u"),
):
    roles = [x.strip() for x in agents.split(",") if x.strip()]
    body = WorkflowCreate(name=name, agents=roles, goal=goal, budget_usd=budget)
    with _client(base_url) as c:
        result = c.create_workflow(body)
        rprint(json.dumps(result, indent=2, default=str))

if __name__ == "__main__":
    app()
