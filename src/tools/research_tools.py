"""Research Tools.

This module provides search and content processing utilities for the research agent,
including web search capabilities, PubMed academic search, and content summarization tools.
"""

import os
from datetime import datetime
import uuid, base64
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional

import httpx
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import InjectedToolArg, InjectedToolCallId, tool
from langgraph.prebuilt import InjectedState
from langgraph.types import Command
from markdownify import markdownify
from pydantic import BaseModel, Field
from tavily import TavilyClient
from typing_extensions import Annotated, Literal
from langchain_ollama import ChatOllama
from ..prompts.deep_prompts import SUMMARIZE_WEB_SEARCH
from ..agent_utils.state import DeepAgentState

# Import Gemini for summarization
from langchain_google_genai import ChatGoogleGenerativeAI

from ..io_py.edge.config import LLMConfigArchitect

"""
# Summarization model - using local Ollama instead of OpenAI
summarization_model = ChatOllama(
    model=LLMConfigArchitect.model_name,
    temperature=LLMConfigArchitect.temperature,
    reasoning=LLMConfigArchitect.reasoning,
)"""

gemini_model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    temperature=0.3,
    api_key=os.environ.get("GEMINI_API_KEY"),
)

tavily_client = TavilyClient()


class Summary(BaseModel):
    """Schema for webpage content summarization."""

    filename: str = Field(description="Name of the file to store.")
    summary: str = Field(description="Key learnings from the webpage.")


def get_today_str() -> str:
    """Get current date in a human-readable format."""
    return datetime.now().strftime("%a %b %-d, %Y")


def run_tavily_search(
    search_query: str,
    max_results: int = 1,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = True,
) -> dict:
    """Perform search using Tavily API for a single query.

    Args:
        search_query: Search query to execute
        max_results: Maximum number of results per query
        topic: Topic filter for search results
        include_raw_content: Whether to include raw webpage content

    Returns:
        Search results dictionary
    """
    result = tavily_client.search(
        search_query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )

    return result


def summarize_webpage_content(webpage_content: str) -> Summary:
    """Summarize webpage content using the configured summarization model.

    Args:
        webpage_content: Raw webpage content to summarize

    Returns:
        Summary object with filename and summary
    """
    try:
        # Set up structured output model for summarization
        structured_model = summarization_model.with_structured_output(Summary)

        # Generate summary
        summary_and_filename = structured_model.invoke(
            [
                HumanMessage(
                    content=SUMMARIZE_WEB_SEARCH.format(
                        webpage_content=webpage_content, date=get_today_str()
                    )
                )
            ]
        )

        return summary_and_filename

    except Exception:
        # Return a basic summary object on failure
        return Summary(
            filename="search_result.md",
            summary=(
                webpage_content[:1000] + "..."
                if len(webpage_content) > 1000
                else webpage_content
            ),
        )


def summarize_pubmed_abstract(abstract: str, title: str) -> str:
    """Summarize a PubMed abstract using Gemini to save local model context.

    Args:
        abstract: The full abstract text
        title: The article title for context

    Returns:
        Concise summary of key findings and relevance
    """
    try:
        # Use Gemini for summarization (save Claude credits for complex tasks)
        from langchain_google_genai import ChatGoogleGenerativeAI

        gemini_model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp", temperature=0.3
        )

        summarization_prompt = f"""Summarize this PubMed abstract concisely for a research agent.

Article Title: {title}

Abstract: {abstract}

Provide a brief summary (2-3 sentences) covering:
1. Main findings or conclusions
2. Key methods or approach
3. Clinical relevance (if applicable)

Summary:"""

        summary_response = gemini_model.invoke(
            [HumanMessage(content=summarization_prompt)]
        )
        return summary_response.content

    except Exception as e:
        # Fallback to truncated abstract
        print(f"Gemini summarization failed: {e}, using truncated abstract")
        return abstract[:300] + "..." if len(abstract) > 300 else abstract


def process_search_results(results: dict) -> list[dict]:
    """Process search results by summarizing content where available.

    Args:
        results: Tavily search results dictionary

    Returns:
        List of processed results with summaries
    """
    processed_results = []

    # Create a client for HTTP requests
    HTTPX_CLIENT = httpx.Client()

    for result in results.get("results", []):

        # Get url
        url = result["url"]

        # Skip PDFs and other binary files
        if url.lower().endswith(
            (".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx")
        ):
            # Use Tavily's generated summary for binary files
            raw_content = result.get("content", "")  # Use Tavily's summary as content
            summary_obj = Summary(
                filename="binary_file_summary.md",
                summary=result.get(
                    "content", "Binary file detected. Using Tavily's summary."
                ),
            )
        else:
            # Read url
            response = HTTPX_CLIENT.get(url)

            if response.status_code == 200:
                # Check content-type to avoid binary data
                content_type = response.headers.get("content-type", "").lower()
                if "pdf" in content_type or "octet-stream" in content_type:
                    # Binary file - use Tavily's summary
                    raw_content = result.get("content", "")
                    summary_obj = Summary(
                        filename="binary_file_summary.md",
                        summary=result.get(
                            "content", "Binary file detected. Using Tavily's summary."
                        ),
                    )
                else:
                    # Convert HTML to markdown
                    raw_content = markdownify(response.text)
                    summary_obj = summarize_webpage_content(raw_content)
            else:
                # Use Tavily's generated summary
                raw_content = result.get("raw_content", "")
                summary_obj = Summary(
                    filename="URL_error.md",
                    summary=result.get(
                        "content", "Error reading URL; try another search."
                    ),
                )

        # uniquify file names
        uid = (
            base64.urlsafe_b64encode(uuid.uuid4().bytes)
            .rstrip(b"=")
            .decode("ascii")[:8]
        )
        name, ext = os.path.splitext(summary_obj.filename)
        summary_obj.filename = f"{name}_{uid}{ext}"

        processed_results.append(
            {
                "url": result["url"],
                "title": result["title"],
                "summary": summary_obj.summary,
                "filename": summary_obj.filename,
                "raw_content": raw_content,
            }
        )

    return processed_results


@tool(parse_docstring=True)
def tavily_search(
    query: str,
    state: Annotated[DeepAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
    max_results: Annotated[int, InjectedToolArg] = 1,
    topic: Annotated[
        Literal["general", "news", "finance"], InjectedToolArg
    ] = "general",
) -> Command:
    """Search web and save detailed results to files while returning minimal context.

    Performs web search and saves full content to files for context offloading.
    Returns only essential information to help the agent decide on next steps.

    Args:
        query: Search query to execute
        state: Injected agent state for file storage
        tool_call_id: Injected tool call identifier
        max_results: Maximum number of results to return (default: 1)
        topic: Topic filter - 'general', 'news', or 'finance' (default: 'general')

    Returns:
        Command that saves full results to files and provides minimal summary
    """
    # Execute search
    search_results = run_tavily_search(
        query,
        max_results=max_results,
        topic=topic,
        include_raw_content=True,
    )

    # Process and summarize results
    processed_results = process_search_results(search_results)

    # Save each result to a file and prepare summary
    files = state.get("files", {})
    saved_files = []
    summaries = []

    for i, result in enumerate(processed_results):
        # Use the AI-generated filename from summarization
        filename = result["filename"]

        # Create file content with full details
        file_content = f"""# Search Result: {result['title']}

**URL:** {result['url']}
**Query:** {query}
**Date:** {get_today_str()}

## Summary
{result['summary']}

## Raw Content
{result['raw_content'] if result['raw_content'] else 'No raw content available'}
"""

        files[filename] = file_content
        saved_files.append(filename)
        summaries.append(f"- {filename}: {result['summary']}...")

    # Create minimal summary for tool message - focus on what was collected
    summary_text = f"""🔍 Found {len(processed_results)} result(s) for '{query}':

{chr(10).join(summaries)}

Files: {', '.join(saved_files)}
💡 Use read_file() to access full details when needed."""

    return Command(
        update={
            "files": files,
            "messages": [ToolMessage(summary_text, tool_call_id=tool_call_id)],
        }
    )


# ========================== PubMed Search Tool ==========================


class PubMedArticle(BaseModel):
    """Schema for PubMed article information."""

    pmid: str = Field(description="PubMed ID")
    title: str = Field(description="Article title")
    authors: List[str] = Field(description="List of authors")
    journal: str = Field(description="Journal name")
    pub_date: str = Field(description="Publication date")
    abstract: str = Field(description="Article abstract")
    doi: Optional[str] = Field(default=None, description="DOI if available")
    url: str = Field(description="PubMed URL")


def search_pubmed(
    query: str, max_results: int = 5, min_year: Optional[int] = None
) -> List[str]:
    """
    Search PubMed for article IDs matching the query.

    Args:
        query: Search query string
        max_results: Maximum number of results to return
        min_year: Minimum publication year (e.g., 2020 for recent studies)

    Returns:
        List of PubMed IDs (PMIDs)
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

    # Build the query with year filter if specified
    full_query = query
    if min_year:
        full_query = f"{query} AND {min_year}[PDAT]:3000[PDAT]"

    params = {
        "db": "pubmed",
        "term": full_query,
        "retmax": max_results,
        "retmode": "xml",
        "sort": "relevance",
    }

    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(base_url, params=params)
            response.raise_for_status()

            # Parse XML response
            root = ET.fromstring(response.text)
            id_list = root.find("IdList")

            if id_list is not None:
                return [id_elem.text for id_elem in id_list.findall("Id")]

            return []

    except Exception as e:
        print(f"Error searching PubMed: {e}")
        return []


def fetch_pubmed_details(pmids: List[str]) -> List[PubMedArticle]:
    """
    Fetch detailed information for PubMed articles.

    Args:
        pmids: List of PubMed IDs

    Returns:
        List of PubMedArticle objects with full details
    """
    if not pmids:
        return []

    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml",
    }

    articles = []

    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(base_url, params=params)
            response.raise_for_status()

            # Parse XML response
            root = ET.fromstring(response.text)

            for article_elem in root.findall(".//PubmedArticle"):
                try:
                    # Extract PMID
                    pmid_elem = article_elem.find(".//PMID")
                    pmid = pmid_elem.text if pmid_elem is not None else "Unknown"

                    # Extract title
                    title_elem = article_elem.find(".//ArticleTitle")
                    title = title_elem.text if title_elem is not None else "No title"

                    # Extract authors
                    authors = []
                    author_list = article_elem.find(".//AuthorList")
                    if author_list is not None:
                        for author_elem in author_list.findall("Author"):
                            last_name = author_elem.find("LastName")
                            fore_name = author_elem.find("ForeName")
                            if last_name is not None:
                                author_name = last_name.text
                                if fore_name is not None:
                                    author_name = f"{fore_name.text} {author_name}"
                                authors.append(author_name)

                    # Extract journal
                    journal_elem = article_elem.find(".//Journal/Title")
                    journal = (
                        journal_elem.text
                        if journal_elem is not None
                        else "Unknown Journal"
                    )

                    # Extract publication date
                    pub_date_elem = article_elem.find(".//PubDate")
                    pub_date = "Unknown"
                    if pub_date_elem is not None:
                        year = pub_date_elem.find("Year")
                        month = pub_date_elem.find("Month")
                        if year is not None:
                            pub_date = year.text
                            if month is not None:
                                pub_date = f"{month.text} {pub_date}"

                    # Extract abstract
                    abstract_texts = []
                    abstract_elem = article_elem.find(".//Abstract")
                    if abstract_elem is not None:
                        for text_elem in abstract_elem.findall(".//AbstractText"):
                            # Handle structured abstracts with labels
                            label = text_elem.get("Label")
                            text = text_elem.text or ""
                            if label:
                                abstract_texts.append(f"{label}: {text}")
                            else:
                                abstract_texts.append(text)

                    abstract = (
                        " ".join(abstract_texts)
                        if abstract_texts
                        else "No abstract available"
                    )

                    # Extract DOI
                    doi = None
                    article_id_list = article_elem.find(".//ArticleIdList")
                    if article_id_list is not None:
                        for article_id in article_id_list.findall("ArticleId"):
                            if article_id.get("IdType") == "doi":
                                doi = article_id.text
                                break

                    # Build PubMed URL
                    url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"

                    # Create article object
                    article = PubMedArticle(
                        pmid=pmid,
                        title=title,
                        authors=authors[:5],  # Limit to first 5 authors
                        journal=journal,
                        pub_date=pub_date,
                        abstract=abstract,
                        doi=doi,
                        url=url,
                    )

                    articles.append(article)

                except Exception as e:
                    print(f"Error parsing article: {e}")
                    continue

            return articles

    except Exception as e:
        print(f"Error fetching PubMed details: {e}")
        return []


@tool(parse_docstring=True)
def pubmed_search(
    query: str,
    state: Annotated[DeepAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
    max_results: Annotated[int, InjectedToolArg] = 5,
    recent_only: Annotated[bool, InjectedToolArg] = True,
) -> Command:
    """Search PubMed for academic research articles and save detailed results.

    Searches the PubMed database for peer-reviewed articles matching the query.
    Saves full article details (title, authors, abstract, journal, DOI) to files
    and returns a summary to help guide research decisions.

    Perfect for finding:
    - Recent studies on psychological interventions
    - Evidence-based treatment approaches
    - Clinical research on mental health conditions
    - Meta-analyses and systematic reviews

    Args:
        query: Search query (e.g., "schema therapy emotional inhibition")
        state: Injected agent state for file storage
        tool_call_id: Injected tool call identifier
        max_results: Maximum number of articles to retrieve (default: 5)
        recent_only: If True, only search articles from 2020 onwards (default: True)

    Returns:
        Command that saves article details to files and provides summary
    """
    # Determine year filter
    min_year = 2020 if recent_only else None

    # Search PubMed for article IDs
    pmids = search_pubmed(query, max_results=max_results, min_year=min_year)

    if not pmids:
        return Command(
            update={
                "messages": [
                    ToolMessage(
                        f"⚠️ No PubMed articles found for query: '{query}'",
                        tool_call_id=tool_call_id,
                    )
                ]
            }
        )

    # Fetch full article details
    articles = fetch_pubmed_details(pmids)

    if not articles:
        return Command(
            update={
                "messages": [
                    ToolMessage(
                        f"⚠️ Found {len(pmids)} articles but could not retrieve details",
                        tool_call_id=tool_call_id,
                    )
                ]
            }
        )

    # Save articles to files and build summary
    files = state.get("files", {})
    saved_files = []
    summaries = []

    for i, article in enumerate(articles, 1):
        # Generate filename
        safe_title = "".join(
            c if c.isalnum() or c in (" ", "-", "_") else "" for c in article.title
        )
        safe_title = safe_title[:50].strip().replace(" ", "_")
        uid = (
            base64.urlsafe_b64encode(uuid.uuid4().bytes)
            .rstrip(b"=")
            .decode("ascii")[:8]
        )
        filename = f"pubmed_{safe_title}_{uid}.md"

        # Generate Gemini summary of the abstract
        gemini_summary = summarize_pubmed_abstract(article.abstract, article.title)

        # Create file content
        authors_str = ", ".join(article.authors)
        if len(article.authors) > 5:
            authors_str += " et al."

        doi_str = f"**DOI:** {article.doi}\n" if article.doi else ""

        file_content = f"""# {article.title}

**Authors:** {authors_str}
**Journal:** {article.journal}
**Published:** {article.pub_date}
{doi_str}**PubMed ID:** {article.pmid}
**URL:** {article.url}

---

## AI Summary (Gemini)

{gemini_summary}

---

## Full Abstract

{article.abstract}

---

**Retrieved:** {get_today_str()}
**Query:** {query}
"""

        files[filename] = file_content
        saved_files.append(filename)

        # Use Gemini summary for tool response instead of truncated abstract
        summaries.append(
            f"**{i}. {article.title[:80]}{'...' if len(article.title) > 80 else ''}**\n   ({article.pub_date}) - {gemini_summary[:150]}{'...' if len(gemini_summary) > 150 else ''}"
        )

    # Build summary response
    year_filter = " (2020-present)" if recent_only else ""
    summary_text = f"""📚 Found {len(articles)} PubMed article(s) for '{query}'{year_filter}:

{chr(10).join(summaries)}

**Files saved:** {', '.join(saved_files)}
💡 Use read_file() to access full abstracts and citation details."""

    return Command(
        update={
            "files": files,
            "messages": [ToolMessage(summary_text, tool_call_id=tool_call_id)],
        }
    )


@tool(parse_docstring=True)
def think_tool(reflection: str) -> str:
    """Tool for strategic reflection on workflow progress and decision-making.

    Use this tool after each search to analyze results and plan next steps systematically.
    This creates a deliberate pause in the research workflow for quality decision-making.

    When to use:
    - After receiving search results: What key information did I find?
    - Before deciding next steps: Do I have enough to answer comprehensively?
    - When assessing research gaps: What specific information am I still missing?
    - Before concluding research: Can I provide a complete answer now?
    - How complex is the question: Have I reached the number of search limits?

    Reflection should address:
    1. Analysis of current findings - What concrete information have I gathered?
    2. Gap assessment - What crucial information is still missing?
    3. Quality evaluation - Do I have sufficient evidence/examples for a good answer?
    4. Strategic decision - Should I continue searching or provide my answer?

    Args:
        reflection: Your detailed reflection on research progress, findings, gaps, and next steps

    Returns:
        Confirmation that reflection was recorded for decision-making
    """
    return f"Reflection recorded: {reflection}"
