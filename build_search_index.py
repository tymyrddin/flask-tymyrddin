#!/usr/bin/env python3
import json
import re
import urllib.request
from pathlib import Path
import html

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


combined_index = {
    "sites": [],
    "metadata": {
        "total_sites": 0,
        "total_documents": 0,
        "generated": None
    }
}

total_docs = 0

for site in SUBDOMAINS:
    print(f"→ Fetching {site['name']} ({site['index']})")
    try:
        with urllib.request.urlopen(site['index']) as response:
            content = response.read().decode("utf-8")

        # Match the JSON inside Search.setIndex({...});
        match = re.search(
            r"Search\.setIndex\(\s*({.*})\s*\);?",
            content,
            re.DOTALL
        )
        if not match:
            print(f"  ! Could not extract JSON from {site['index']}")
            continue

        data = json.loads(match.group(1))

        # Unescape HTML entities in all data
        data = unescape_data(data)

        # Count documents
        doc_count = len(data.get('titles', []))
        total_docs += doc_count

        combined_index["sites"].append({
            "name": site["name"],
            "url": site["url"],
            "index_data": data,
            "document_count": doc_count
        })

        print(f"  ✓ Loaded {doc_count} documents from {site['name']}")

    except Exception as e:
        print(f"  ! Error fetching or parsing {site['index']}: {e}")

# Update metadata
from datetime import datetime, timezone

combined_index["metadata"]["total_sites"] = len(combined_index["sites"])
combined_index["metadata"]["total_documents"] = total_docs
combined_index["metadata"]["generated"] = datetime.now(timezone.utc).isoformat()

# Write combined index
try:
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(combined_index, f, ensure_ascii=False, indent=2)
    print(f"\n✓ Combined index written to {OUTPUT_FILE}")
    print(f"  Sites: {combined_index['metadata']['total_sites']}")
    print(f"  Total documents: {combined_index['metadata']['total_documents']}")
except Exception as e:
    print(f"! Could not write combined index: {e}")

