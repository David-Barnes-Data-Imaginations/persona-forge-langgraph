@tool
def get_objective_analysis(session_id: str = "session_001") -> str:
    """
    Retrieve all objective analysis sections from QA pairs in a session.

    The objective analysis contains directly observable/measurable features in the text
    such as sentence count, word patterns, disfluencies, emphasis markers, and
    AI-derived affect metrics with confidence scores.

    Args:
        session_id: The session to retrieve objective analyses from (default: 'session_001')

    Returns:
        All objective analysis sections organized by QA pair
    """
    rag = get_rag_instance()

    cypher = """
    MATCH (s:Session {session_id: $session_id})-[:INCLUDES]->(qa:QA_Pair)
    WHERE qa.objective_analysis IS NOT NULL
    RETURN qa.id as qa_id,
           qa.question as question,
           qa.objective_analysis as objective_analysis
    ORDER BY qa.id
    """

    with rag.driver.session() as session:
        try:
            results = session.run(cypher, session_id=session_id)
            records = [dict(record) for record in results]

            if not records:
                return f"No objective analyses found for session: {session_id}"

            # Format output
            output_parts = [f"=== OBJECTIVE ANALYSES FOR {session_id.upper()} ===\n"]
            output_parts.append(f"Total QA Pairs: {len(records)}\n")

            for record in records:
                output_parts.append(f"QA PAIR: {record['qa_id']}")
                output_parts.append(f"Question: {record['question']}\n")
                output_parts.append(f"Objective Analysis:")
                output_parts.append(f"{record['objective_analysis']}\n")
                output_parts.append("-" * 60 + "\n")

            return "\n".join(output_parts)

        except Exception as e:
            return f"Error retrieving objective analyses: {str(e)}"
