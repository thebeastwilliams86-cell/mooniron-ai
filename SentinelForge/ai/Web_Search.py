import requests
from openai import OpenAI
from dotenv import load_dotenv
import urllib3

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

# Initialize OpenAI client
client = OpenAI()

# DuckDuckGo Instant Answer API endpoint
DDG_API = "https://api.duckduckgo.com/"

def web_search(query: str, num_results: int = 5):
    """
    Perform a web search using DuckDuckGo Instant Answer API.
    """
    params = {
        "q": query,
        "format": "json",
        "no_html": 1,
        "skip_disambig": 1
    }
    try:
        resp = requests.get(DDG_API, params=params, verify=False, timeout=10)
        data = resp.json()
        
        results = []
        # Check multiple data sources
        if "RelatedTopics" in data and data["RelatedTopics"]:
            for item in data["RelatedTopics"][:num_results]:
                if isinstance(item, dict) and "Text" in item and "FirstURL" in item:
                    results.append({"title": item["Text"], "url": item["FirstURL"]})
        
        # If no RelatedTopics, check Abstract
        if not results and "Abstract" in data and data["Abstract"]:
            results.append({"title": data["Abstract"], "url": data.get("AbstractURL", query)})
            
        return results
    except Exception as e:
        print(f"❌ Search failed: {e}")
        return []

def summarize_results(query: str, results: list):
    """
    Use OpenAI to summarize search results.
    """
    context = "\n".join([f"- {r['title']} ({r['url']})" for r in results])

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # you can use gpt-5-mini if available
        messages=[
            {"role": "system", "content": "You are a helpful search assistant."},
            {"role": "user", "content": f"Search query: {query}\n\nResults:\n{context}\n\nSummarize these results clearly."}
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    print("🌐 Web Search Assistant Ready!")
    while True:
        query = input("\n🔍 Enter your search query (type 'exit' to quit): ")
        if query.lower() == 'exit':
            print("👋 Goodbye!")
            break
            
        print(f"\n🔍 Searching for: {query}\n")
        results = web_search(query)
        
        if results:
            for r in results:
                print(f"- {r['title']} ({r['url']})")

            print("\n📌 Summary:")
            summary = summarize_results(query, results)
            print(summary)
        else:
            print("❌ No results found or search failed.")
        
        print("─" * 50)
