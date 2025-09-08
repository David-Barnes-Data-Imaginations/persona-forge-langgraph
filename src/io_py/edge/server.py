import asyncio
import os
import typer
from fastmcp import FastMCP
from langchain_mcp_adapters.client import MultiServerMCPClient
from src.io_py.edge.db import register_device_manager_tools, initialise_database, DeviceManager, populate_database
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

app = typer.Typer()
console = Console()
root_dir = ROOT_DIR

def initialise_server(db_path: os.PathLike) -> FastMCP:
    """Initialise the server.

    Args:
        db_path (os.PathLike):
            The path to the duckdb database which
            stores the server information.
    Returns:
        FastMCP: The FastMCP server.
    """
    conn = initialise_database(db_path)
    device_manager = DeviceManager(conn)

    # find all devices that are available and update the database
    asyncio.run(populate_database(device_manager))

    mcp = FastMCP(
        name="smarthome-mcp-server",
        instructions="This server is for finding and controlling smarthome devices.",
    )

    register_device_manager_tools(mcp, device_manager)
    return mcp

def get_new_mcp_client() -> MultiServerMCPClient
    return MultiServerMCPClient(
        {
            "smarthome-mcp-server": {
                "command": "smarthome_mcp_server",
                "args": [],
                "transport": "stdio",
            }
        }
    )

def get_mcp_server_tools():
    mcp_client = get_new_mcp_client()
    tools = await mcp_client.get_tools()
    return tools

@app.command()
def main():
    config = load_config()

    # set up server data directory
    root_dir = platformdirs.user_data_path(
        appname="smarthome-mcp-server",
        ensure_exists=True
    )
    db_path = Path(root_dir) / config.database.path
    db_path.parent.mkdir(parents=True, exist_ok=True)
    logger.info("Server data directory: %s", db_path)

    # init and run
    mcp_instance = initialise_server(db_path)
    asyncio.run(mcp_instance.run_stdio_async())

    mcp_client = get_new_mcp_client()
    tools = await mcp_client.get_tools()

if __name__ == "__main__":
    app()