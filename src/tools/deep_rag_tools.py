"""
Deep Agent RAG Tool Wrappers

This module provides wrappers around the hybrid_rag_tools that save results
to the deep agent's virtual file system. These are used by the deep agent workflow.

The original tools in hybrid_rag_tools.py are used directly by the chatbot workflow
without file saving.
"""

from datetime import datetime
from langchain_core.tools import tool
from typing import Annotated
from langgraph.prebuilt import InjectedState

from .hybrid_rag_tools import (
    search_psychological_insights,
    get_personality_summary,
    get_objective_statistics,
    get_extreme_values,
    get_qa_pair_details,
    retrieve_diagnosis,
    get_subjective_analysis,
    get_plan,
)
from ..agent_utils.state import DeepAgentState


def _save_to_virtual_fs(state: dict, filename: str, content: str) -> str:
    """Helper to save content to deep agent's virtual file system"""
    if "files" not in state:
        state["files"] = {}

    state["files"][filename] = content
    return f"Results saved to {filename}"


@tool
def deep_search_psychological_insights(
    query: str, k: int = 5, state: Annotated[dict, InjectedState] = None
) -> str:
    """Search the psychological knowledge graph and save results to a file.

    Use this to find psychological patterns, behavioral insights, and emotional
    indicators from the client's conversation history.

    Args:
        query: The search query describing what psychological insights to find
        k: Number of results to return (default 5)
        state: Deep agent state (auto-injected)

    Returns:
        Confirmation message with filename
    """
    # Call original tool
    results = search_psychological_insights.invoke({"query": query, "k": k})

    # Save to virtual file system
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"psych_search_{timestamp}.txt"

    if state:
        _save_to_virtual_fs(state, filename, results)
        return f"Search complete. {results[:200]}... [Full results saved to {filename}]"

    return results


@tool
def deep_get_personality_summary(
    client_id: str = "client_001", state: Annotated[dict, InjectedState] = None
) -> str:
    """Get comprehensive personality profile and save to a file.

    Retrieves averaged psychological metrics across all sessions including
    Big Five traits, emotional patterns, and behavioral indicators.

    Args:
        client_id: Client identifier (default: client_001)
        state: Deep agent state (auto-injected)

    Returns:
        Confirmation message with filename
    """
    # Call original tool
    results = get_personality_summary.invoke({"client_id": client_id})

    # Save to virtual file system
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"personality_summary_{timestamp}.txt"

    if state:
        _save_to_virtual_fs(state, filename, results)
        return f"Personality summary retrieved. [Saved to {filename}]"

    return results


@tool
def deep_get_graph_statistics(
    session_id: str = "session_001", state: Annotated[dict, InjectedState] = None
) -> str:
    """Get detailed graph statistics and save to a file.

    Returns comprehensive statistics about nodes, relationships, and metrics
    in the knowledge graph for a specific session.

    Args:
        session_id: Session identifier (default: session_001)
        state: Deep agent state (auto-injected)

    Returns:
        Confirmation message with filename
    """
    # Call original tool
    results = get_graph_statistics.invoke({"session_id": session_id})

    # Save to virtual file system
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"graph_stats_{timestamp}.txt"

    if state:
        _save_to_virtual_fs(state, filename, results)
        return f"Graph statistics retrieved. [Saved to {filename}]"

    return results


@tool
def deep_get_extreme_values(
    session_id: str = "session_001", state: Annotated[dict, InjectedState] = None
) -> str:
    """Find extreme psychological values and save to a file.

    Identifies the highest and lowest values across all psychological metrics
    for pattern analysis and risk assessment.

    Args:
        session_id: Session identifier (default: session_001)
        state: Deep agent state (auto-injected)

    Returns:
        Confirmation message with filename
    """
    # Call original tool
    results = get_extreme_values.invoke({"session_id": session_id})

    # Save to virtual file system
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"extreme_values_{timestamp}.txt"

    if state:
        _save_to_virtual_fs(state, filename, results)
        return f"Extreme values retrieved. [Saved to {filename}]"

    return results


@tool
def deep_get_qa_pair_details(
    qa_id: str, state: Annotated[dict, InjectedState] = None
) -> str:
    """Get complete details for a QA pair and save to a file.

    Retrieves the full SOAP analysis (Subjective, Objective, Assessment, Plan)
    for a specific question-answer pair.

    Args:
        qa_id: QA pair identifier (e.g., "qa_001")
        state: Deep agent state (auto-injected)

    Returns:
        Confirmation message with filename
    """
    # Call original tool
    results = get_qa_pair_details.invoke({"qa_id": qa_id})

    # Save to virtual file system
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"qa_details_{qa_id}_{timestamp}.txt"

    if state:
        _save_to_virtual_fs(state, filename, results)
        return f"QA pair details retrieved. [Saved to {filename}]"

    return results


@tool
def deep_retrieve_diagnosis(
    client_id: str = "client_001", state: Annotated[dict, InjectedState] = None
) -> str:
    """Retrieve client diagnosis and medical history, save to a file.

    Gets complete medical history, diagnoses, previous treatments,
    family history, and risk factors from the knowledge graph.

    Args:
        client_id: Client identifier (default: client_001)
        state: Deep agent state (auto-injected)

    Returns:
        Confirmation message with filename
    """
    # Call original tool
    results = retrieve_diagnosis.invoke({"client_id": client_id})

    # Save to virtual file system
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"diagnosis_{timestamp}.txt"

    if state:
        _save_to_virtual_fs(state, filename, results)
        return f"Diagnosis retrieved. [Saved to {filename}]"

    return results


@tool
def deep_get_subjective_analysis(
    session_id: str = "session_001", state: Annotated[dict, InjectedState] = None
) -> str:
    """Get all subjective analysis sections and save to a file.

    Retrieves client-reported experiences, feelings, perceptions, and symptoms
    from all QA pairs in a session.

    Args:
        session_id: Session identifier (default: session_001)
        state: Deep agent state (auto-injected)

    Returns:
        Confirmation message with filename
    """
    # Call original tool
    results = get_subjective_analysis.invoke({"session_id": session_id})

    # Save to virtual file system
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"subjective_analysis_{timestamp}.txt"

    if state:
        _save_to_virtual_fs(state, filename, results)
        return f"Subjective analysis retrieved. [Saved to {filename}]"

    return results


@tool
def deep_get_objective_analysis(
    session_id: str = "session_001", state: Annotated[dict, InjectedState] = None
) -> str:
    """Get all objective analysis sections and save to a file.

    Retrieves observable patterns, measurable text features, and statistical
    metrics from all QA pairs in a session.

    Args:
        session_id: Session identifier (default: session_001)
        state: Deep agent state (auto-injected)

    Returns:
        Confirmation message with filename
    """
    # Call original tool
    results = get_objective_statistics.invoke({"session_id": session_id})

    # Save to virtual file system
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"objective_analysis_{timestamp}.txt"

    if state:
        _save_to_virtual_fs(state, filename, results)
        return f"Objective analysis retrieved. [Saved to {filename}]"

    return results


@tool
def deep_get_plan(
    session_id: str = "session_001", state: Annotated[dict, InjectedState] = None
) -> str:
    """Get all treatment plan sections and save to a file.

    Retrieves interventions, monitoring strategies, and therapeutic homework
    from all QA pairs in a session.

    Args:
        session_id: Session identifier (default: session_001)
        state: Deep agent state (auto-injected)

    Returns:
        Confirmation message with filename
    """
    # Call original tool
    results = get_plan.invoke({"session_id": session_id})

    # Save to virtual file system
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"treatment_plan_{timestamp}.txt"

    if state:
        _save_to_virtual_fs(state, filename, results)
        return f"Treatment plan retrieved. [Saved to {filename}]"

    return results


# Tool list for deep agent workflow (with file saving)
DEEP_PERSONA_FORGE_TOOLS = [
    deep_search_psychological_insights,
    deep_get_personality_summary,
    deep_get_graph_statistics,
    deep_get_extreme_values,
    deep_get_qa_pair_details,
    deep_retrieve_diagnosis,
    deep_get_subjective_analysis,
    deep_get_objective_analysis,
    deep_get_plan,
]
