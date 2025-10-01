#!/usr/bin/env python3
"""
Quick test script for the PubMed search tool

This demonstrates the PubMed tool functionality without needing to run the full agent.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.tools.research_tools import search_pubmed, fetch_pubmed_details


def test_pubmed_search():
    """Test PubMed search and article retrieval"""

    print("=" * 70)
    print("Testing PubMed Search Tool")
    print("=" * 70)

    # Test query
    query = "schema therapy emotional regulation"
    max_results = 3

    print(f"\n📚 Searching PubMed for: '{query}'")
    print(f"   Fetching up to {max_results} results from 2020-present...\n")

    # Search for article IDs
    pmids = search_pubmed(query, max_results=max_results, min_year=2020)

    if not pmids:
        print("❌ No articles found")
        return

    print(f"✅ Found {len(pmids)} article(s)")
    print(f"   PMIDs: {', '.join(pmids)}\n")

    # Fetch full details
    print("📥 Fetching article details...\n")
    articles = fetch_pubmed_details(pmids)

    if not articles:
        print("❌ Could not retrieve article details")
        return

    # Display results
    print("=" * 70)
    print("RESULTS")
    print("=" * 70)

    for i, article in enumerate(articles, 1):
        print(f"\n{i}. {article.title}")
        print(f"   Authors: {', '.join(article.authors[:3])}")
        if len(article.authors) > 3:
            print(f"           et al.")
        print(f"   Journal: {article.journal}")
        print(f"   Published: {article.pub_date}")
        print(f"   PMID: {article.pmid}")
        if article.doi:
            print(f"   DOI: {article.doi}")
        print(f"   URL: {article.url}")
        print(f"\n   Abstract Preview:")
        abstract_preview = article.abstract[:300] + "..." if len(article.abstract) > 300 else article.abstract
        print(f"   {abstract_preview}")
        print("\n" + "-" * 70)

    print("\n✅ PubMed tool is working correctly!")
    print("\nNote: The actual tool saves these as markdown files in the agent's state.")


if __name__ == "__main__":
    try:
        test_pubmed_search()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)