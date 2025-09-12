import os
import duckdb
from fastmcp import FastMCP

class DeviceManager:
    def __init__(self, conn: duckdb.DuckDBPyConnection) -> None:
        self._conn = conn

    ...

    async def turn_on_device(self, device_name: str) -> str:
        """Turn on a device.

        Args:
            device_name (str):
                The name of the device to turn on.
        """
        try:
            device = await self._get_device(device_name)
        except DeviceNotFoundError as e:
            logger.exception(e)
            return f"Device {device_name} not found."

        await device.turn_on()
        return f"Device {device_name} turned on."

    async def turn_off_device(self, device_name: str) -> str:
        """Turn off a device.

        Args:
            device_name (str):
                The name of the device to turn off.
        """
        try:
            device = await self._get_device(device_name)
        except DeviceNotFoundError as e:
            logger.exception(e)
            return f"Device {device_name} not found."

        await device.turn_off()
        return f"Device {device_name} turned off."

    async def list_devices(self) -> list[str]:
        """List the available device names.

        Returns:
            list[str]:
                A list of device names.
        """
        results = self._conn.query("SELECT name FROM device").fetchall()

        return [result[0] for result in results]

def initialise_database(db_path:os.PathLike) -> duckdb.DuckDBPyConnection:
    """Get the database connection and create the tables if they don't exist."""
    conn = duckdb.connect(db_path)

    # initialise if not exists tables
    conn.execute(
        get_create_table_if_not_exists_query(get_device_table_schema())
    )

    return conn


def register_device_manager_tools(mcp_instance: FastMCP, device_manager: DeviceManager) -> FastMCP:
    """Register the methods defined in DeviceManager as tools for MCP server."""
    mcp_instance.tool(name_or_fn=device_manager.list_devices)
    mcp_instance.tool(name_or_fn=device_manager.turn_off_device)
    mcp_instance.tool(name_or_fn=device_manager.turn_on_device)
    return mcp_instance


async def populate_database(device_manager: DeviceManager):
    """Find all devices that are available and update the database.

    Discover all available devices and get their latest states.

    Note:
        Device names may have changed via the mobile app, thus this
        step is necessary when starting the server.
    """
    all_devices = await device_manager.discover_new_devices()
    upsert_coroutines = [device_manager._upsert_device(device) for device in all_devices.values()]
    await asyncio.gather(*upsert_coroutines)


