#!/usr/bin/env python3
import json
import re
import urllib.request
import urllib.error
import socket
from html.parser import HTMLParser
from pathlib import Path
import html
from datetime import datetime, timezone
import time

# List of Sphinx subdomain search indexes with friendly names
SUBDOMAINS = [
    {"name": "Blue", "url": "https://blue.tymyrddin.dev", "index": "https://blue.tymyrddin.dev/searchindex.js", "sources": "/home/nina/Development/github/blue/build/html/_sources"},
    {"name": "Green", "url": "https://green.tymyrddin.dev", "index": "https://green.tymyrddin.dev/searchindex.js", "sources": "/home/nina/Development/github/green/build/html/_sources"},
    {"name": "Purple", "url": "https://purple.tymyrddin.dev", "index": "https://purple.tymyrddin.dev/searchindex.js", "sources": "/home/nina/Development/github/purple/build/html/_sources"},
    {"name": "Red", "url": "https://red.tymyrddin.dev", "index": "https://red.tymyrddin.dev/searchindex.js", "sources": "/home/nina/Development/github/red/build/html/_sources"},
    {"name": "Indigo", "url": "https://indigo.tymyrddin.dev", "index": "https://indigo.tymyrddin.dev/searchindex.js", "sources": "/home/nina/Development/gitlab/roadmaps/build/html/_sources"},
]

# Blog sites with Hugo-style index.json
BLOG_SITES = [
    {"name": "Broomstick", "url": "https://broomstick.tymyrddin.dev", "index": "https://broomstick.tymyrddin.dev/index.json"},
]

# Output path
OUTPUT_FILE = Path("project/static/search/index.json")

# Configuration
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
TIMEOUT = 10  # seconds



CONTENT_LIMIT = 5000  # characters of body text stored per document


def extract_title_from_source(text, stem):
    """Pull the first heading from RST or Markdown source text."""
    m = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    lines = [l for l in text.split('\n') if l.strip()]
    for i, line in enumerate(lines[:-1]):
        if re.match(r'^[=\-~^"\'`#*+]{3,}$', lines[i + 1].strip()):
            return line.strip()
    return stem.replace('-', ' ').replace('_', ' ').title()


class _SphinxTextExtractor(HTMLParser):
    """Extract plain text from Sphinx HTML, skipping navigation and toctree blocks."""

    _SKIP_CLASSES = frozenset({
        'toctree-wrapper', 'sphinxsidebar', 'sphinxsidebarwrapper',
        'related', 'footer-relations', 'navigation', 'headerlink', 'highlight',
    })
    _SKIP_TAGS = frozenset({'script', 'style', 'nav', 'footer', 'title', 'pre'})

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self._skip_tag = None
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if self._skip_depth:
            if tag == self._skip_tag:
                self._skip_depth += 1
            return
        classes = set(dict(attrs).get('class', '').split())
        if tag in self._SKIP_TAGS or classes & self._SKIP_CLASSES:
            self._skip_tag = tag
            self._skip_depth = 1

    def handle_endtag(self, tag):
        if self._skip_depth and tag == self._skip_tag:
            self._skip_depth -= 1
            if not self._skip_depth:
                self._skip_tag = None

    def handle_data(self, data):
        if not self._skip_depth:
            self.parts.append(data)

    def get_text(self):
        text = ' '.join(self.parts)
        text = text.replace('­', '')  # soft hyphens
        text = re.sub(r'\bSkip to (?:main )?content\b', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\bBack to top\b', '', text, flags=re.IGNORECASE)
        return re.sub(r'\s+', ' ', text).strip()


def extract_from_html(html_content):
    """Extract plain text from a Sphinx-built HTML file, skipping navigation blocks."""
    extractor = _SphinxTextExtractor()
    extractor.feed(html_content)
    return extractor.get_text()


def read_sources(sources_path, site_url):
    """Walk _sources/, pair each file with its built HTML, return flat docs list."""
    sources_root = Path(sources_path)
    if not sources_root.exists():
        return None

    html_root = sources_root.parent  # build/html/_sources → build/html

    files = sorted(
        list(sources_root.rglob("*.md.txt")) +
        list(sources_root.rglob("*.rst.txt"))
    )

    docs = []
    for i, src_file in enumerate(files):
        try:
            rel = str(src_file.relative_to(sources_root)).replace('.md.txt', '').replace('.rst.txt', '')
            html_file = html_root / (rel + '.html')
            url = f"{site_url}/{rel}"

            src_text = src_file.read_text(encoding="utf-8", errors="replace")
            title = extract_title_from_source(src_text, src_file.stem)

            if html_file.exists():
                content = extract_from_html(html_file.read_text(encoding="utf-8", errors="replace"))
            else:
                continue  # skip source files with no built HTML counterpart

            if len(content) < 150:
                continue  # skip near-empty toctree index pages

            docs.append({
                "id": len(docs),  # must equal array index — never use enumerate's i when continue statements exist
                "title": html.unescape(title),
                "url": url,
                "content": content[:CONTENT_LIMIT],
            })
        except Exception as e:
            print(f"  ⚠ Could not read {src_file}: {e}")

    return docs


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

        match = re.search(
            r"Search\.setIndex\(\s*({.*})\s*\);?",
            content,
            re.DOTALL
        )

        if not match:
            print(f"  ✗ Could not extract JSON from {site['index']}")
            return None

        data = json.loads(match.group(1))
        data = unescape_data(data)
        doc_count = len(data.get('titles', []))

        # Use local sources for full-content Lunr indexing if available
        sources_path = site.get("sources")
        if sources_path:
            docs = read_sources(sources_path, site["url"])
            if docs:
                print(f"  ✓ Loaded {len(docs)} documents from {site['name']} (with content)")
                return {
                    "name": site["name"],
                    "url": site["url"],
                    "type": "sphinx",
                    "docs": docs,
                    "document_count": len(docs),
                }

        # Fallback: term-map only from searchindex.js
        print(f"  ✓ Loaded {doc_count} documents from {site['name']}")
        return {
            "name": site["name"],
            "url": site["url"],
            "index_data": data,
            "document_count": doc_count,
        }

    except Exception as e:
        print(f"  ✗ Error processing {site['index']}: {e}")
        return None


def process_blog_site(site):
    """Process a Hugo blog site with a flat index.json array."""
    print(f"→ Fetching {site['name']} ({site['index']})")
    try:
        content = fetch_with_retry(site['index'])
        posts = json.loads(content)

        # Keep only actual posts, not taxonomy/index pages
        posts = [p for p in posts if '/posts/' in p.get('permalink', '')]

        docs = []
        for i, post in enumerate(posts):
            docs.append({
                "id": i,
                "title": html.unescape(post.get('title', '')),
                "url": post.get('permalink', ''),
                "content": html.unescape(post.get('content', '')),
            })

        print(f"  ✓ Loaded {len(docs)} posts from {site['name']}")
        return {
            "name": site["name"],
            "url": site["url"],
            "type": "blog",
            "docs": docs,
            "document_count": len(docs),
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

    # Process blog sites
    for site in BLOG_SITES:
        site_data = process_blog_site(site)

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
