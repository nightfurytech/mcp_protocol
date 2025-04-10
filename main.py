import psycopg2
from mcp.server.fastmcp import FastMCP
from mcp.types import Tool
import os

# Initialize the MCP server
mcp = FastMCP("PostgresMCPServer")

db_config = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
}


# Database connection function
def get_db_connection():
    return psycopg2.connect(**db_config)


# Define a tool to fetch recent sales data
@mcp.tool()
def fetch_recent_sales(limit: int = 10) -> list:
    """Fetch the most recent sales records."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sales ORDER BY sale_date DESC LIMIT %s;", (limit,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


# Start the MCP server
if __name__ == "__main__":
    mcp.run()
