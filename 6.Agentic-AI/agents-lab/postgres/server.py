import os
import psycopg
from mcp.server.fastmcp import FastMCP

# Create MCP server
mcp = FastMCP("Simple Postgres MCP Server")

# Postgres connection string (DSN) from environment variable
# Example:
#   export POSTGRES_DSN="postgresql://postgres:password@localhost:5432/mydb"
# POSTGRES_DSN = os.getenv("POSTGRES_DSN")
POSTGRES_DSN="postgresql+psycopg://postgres:pg1234@localhost:5432/srg"

# Allow SQLAlchemy-style: postgresql+psycopg://...
POSTGRES_DSN = POSTGRES_DSN.replace("postgresql+psycopg://", "postgresql://")

if not POSTGRES_DSN:
    raise RuntimeError("Please set POSTGRES_DSN env var (postgresql://user:pass@host:port/dbname)")


def run_select(sql: str):
    """Run a simple SELECT query and return rows."""
    with psycopg.connect(POSTGRES_DSN) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()

@mcp.tool()
def db_time():
    """Returns current time from the database."""
    rows = run_select("SELECT now()")
    return {"db_time": str(rows[0][0])}

@mcp.tool()
def list_tables():
    """Lists tables in the public schema."""
    rows = run_select("""
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public'
        ORDER BY tablename
    """)
    return {"tables": [r[0] for r in rows]}

@mcp.tool()
def select_top(table: str, limit: int = 5):
    """Shows first N rows from a table (beginner demo)."""
    # SUPER SIMPLE (demo only): assumes table name is safe
    rows = run_select(f"SELECT * FROM {table} LIMIT {limit}")
    return {"rows": rows}

if __name__ == "__main__":
    mcp.run()
