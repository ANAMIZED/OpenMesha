"""python -m openmesha.mcp — Glama stdio entry."""

from openmesha.mcp.server import mcp


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
