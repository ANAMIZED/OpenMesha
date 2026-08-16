from openmesha.mcp.server import MCP_TOOLS, create_agent, list_agents, create_workflow, list_available_tools

def test_mcp_tools_registered():
    required = {"create_agent", "run_task", "list_agents", "get_cost_ledger", "get_audit_log", "create_workflow", "list_available_tools", "x402_payment_quote"}
    assert required.issubset(set(MCP_TOOLS.keys()))

def test_mcp_create_list():
    a = create_agent(name="mcp-a", intent="Answer under budget", budget_usd=0.2, capabilities=["web_search"])
    assert "id" in a
    agents = list_agents()
    assert any(x["id"] == a["id"] for x in agents)

def test_mcp_tools_list():
    tools = list_available_tools()
    assert "web_search" in tools

def test_mcp_workflow():
    r = create_workflow(name="mcp-wf", goal="Summarize agentic OS", agents=["planner", "worker"], budget_usd=0.5)
    assert r["workflow"]["status"] == "completed"
