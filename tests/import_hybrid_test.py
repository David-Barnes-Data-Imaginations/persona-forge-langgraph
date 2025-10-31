import os, sys

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, repo_root)

from src.tools import hybrid_rag_tools as h

print("Imported hybrid_rag_tools OK")
rag = h.get_rag_instance()
print("RAG instance driver:", rag.driver)
# Try a simple run to check session works
with rag.driver.session() as s:
    r = s.run('RETURN "ok" as v').single()
    print("Query returned:", r["v"])

# Cleanup
h.cleanup_rag_connection()
print("Cleaned up connection")
