#!/usr/bin/env python3
import json
import re
import urllib.request
import urllib.error
import socket
from pathlib import Path
import html
from datetime import datetime, timezone
import time

# List of Sphinx subdomain search indexes with friendly names
SUBDOMAINS = [
    {"name": "Blue", "url": "https://blue.tymyrddin.dev", "index": "https://blue.tymyrddin.dev/searchindex.js"},
    {"name": "Green", "url": "https://green.tymyrddin.dev", "index": "https://green.tymyrddin.dev/searchindex.js"},
    {"name": "Purple", "url": "https://purple.tymyrddin.dev", "index": "https://purple.tymyrddin.dev/searchindex.js"},
    {"name": "Red", "url": "https://red.tymyrddin.dev", "index": "https://red.tymyrddin.dev/searchindex.js"},
    {"name": "Indigo", "url": "https://indigo.tymyrddin.dev", "index": "https://indigo.tymyrddin.dev/searchindex.js"},
]

# Output path
OUTPUT_FILE = Path("project/static/search/index.json")

# Configuration
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
TIMEOUT = 10  # seconds


def fetch_with_retry(url, max_retries=MAX_RETRIES):
    """Fetch URL with retry logic and timeout."""
    for attempt in range(max_retries):
        try:
            # Create request with headers to mimic a browser
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (compatible; SearchIndexBot/1.0)',
                    'Accept': 'application/javascript, */*;q=0.8'
                }
            )

            with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
                return response.read().decode("utf-8")

        except (urllib.error.URLError, socket.error, socket.timeout) as e:
            if attempt < max_retries - 1:
                print(f"  ⚠ Attempt {attempt + 1} failed: {e}. Retrying in {RETRY_DELAY}s...")
                time.sleep(RETRY_DELAY)
            else:
                raise e

    return None  # Should never reach here


def unescape_data(data):
    """Recursively unescape HTML entities in the data structure."""
    if isinstance(data, str):
        return html.unescape(data)
    elif isinstance(data, list):
        return [unescape_data(item) for item in data]
    elif isinstance(data, dict):
        return {key: unescape_data(value) for key, value in data.items()}
    else:
        return data


def process_site(site):
    """Process a single site and return its data or None if failed."""
    print(f"→ Fetching {site['name']} ({site['index']})")

    try:
        content = fetch_with_retry(site['index'])

        # Match the JSON inside Search.setIndex({...});
        match = re.search(
            r"Search\.setIndex\(\s*({.*})\s*\);?",
            content,
            re.DOTALL
        )

        if not match:
            print(f"  ✗ Could not extract JSON from {site['index']}")
            return None

        data = json.loads(match.group(1))

        # Unescape HTML entities in all data
        data = unescape_data(data)

        # Count documents
        doc_count = len(data.get('titles', []))

        print(f"  ✓ Loaded {doc_count} documents from {site['name']}")

        return {
            "name": site["name"],
            "url": site["url"],
            "index_data": data,
            "document_count": doc_count
        }

    except Exception as e:
        print(f"  ✗ Error processing {site['index']}: {e}")
        return None


def main():
    combined_index = {
        "sites": [],
        "metadata": {
            "total_sites": 0,
            "total_documents": 0,
            "generated": None,
            "failed_sites": []
        }
    }

    total_docs = 0
    failed_sites = []

    # Process each site
    for site in SUBDOMAINS:
        site_data = process_site(site)

        if site_data:
            combined_index["sites"].append(site_data)
            total_docs += site_data["document_count"]
        else:
            failed_sites.append(site["name"])
            print(f"  ✗ Failed to process {site['name']}")

    # Update metadata
    combined_index["metadata"]["total_sites"] = len(combined_index["sites"])
    combined_index["metadata"]["total_documents"] = total_docs
    combined_index["metadata"]["generated"] = datetime.now(timezone.utc).isoformat()
    combined_index["metadata"]["failed_sites"] = failed_sites

    # Write combined index
    try:
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(combined_index, f, ensure_ascii=False, indent=2)

        print(f"\n✓ Combined index written to {OUTPUT_FILE}")
        print(f"  Sites successfully processed: {combined_index['metadata']['total_sites']}")
        print(f"  Total documents: {combined_index['metadata']['total_documents']}")

        if failed_sites:
            print(f"  ⚠ Failed sites: {', '.join(failed_sites)}")
            print(f"  Consider running the script again for complete coverage.")

    except Exception as e:
        print(f"! Could not write combined index: {e}")
        return 1

    return 0 if not failed_sites else 1


if __name__ == "__main__":
    exit(main())
