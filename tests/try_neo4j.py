from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

# Ensure .env from repository root is loaded (tests may be run from other cwd)
try:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    env_path = os.path.join(repo_root, ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path)
    else:
        load_dotenv()
except Exception:
    load_dotenv()

uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USER")
pwd = (
    os.getenv("NEO4JP")
    or os.getenv("NEO4J_PASSWORD")
    or os.getenv("NEO4J_PASS")
    or os.getenv("NEO4J_PWD")
)

print(f"Trying to connect to {uri!r} as {user!r}")

try:
    driver = GraphDatabase.driver(uri, auth=(user, pwd))
    with driver.session() as s:
        rec = s.run("RETURN 1 as result").single()
        print("Query result:", rec["result"])
    driver.close()
    print("Neo4j connection successful")
except Exception as e:
    import traceback

    print("Neo4j connection failed:")
    traceback.print_exc()
    raise
