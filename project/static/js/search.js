(function() {
    let searchData = null;
    let lunrIndexes = {};
    let isLoading = true;
    let currentQuery = '';
    const resultsPerPage = 10;
    const SITE_WEIGHTS = { 'Blue': 0.5, 'Red': 0.5, 'Purple': 1.8, 'Green': 1.4, 'Indigo': 1.4, 'Broomstick': 1.1 };
    let currentPage = 1;
    let currentResults = [];

    // Load the combined search index
    async function loadSearchIndex() {
        try {
            const response = await fetch('/static/search/index.json');
            searchData = await response.json();

            // Build Lunr indexes one site at a time, yielding between each
            // to keep the browser responsive while typing
            for (const site of searchData.sites) {
                if (site.docs) {
                    await new Promise(resolve => setTimeout(resolve, 0));
                    lunrIndexes[site.name] = lunr(function() {
                        this.ref('id');
                        this.field('title', { boost: 10 });
                        this.field('content');
                        site.docs.forEach(doc => this.add(doc));
                    });
                }
            }

            isLoading = false;
            console.log(`Loaded search index: ${searchData.metadata.total_sites} sites, ${searchData.metadata.total_documents} documents`);
            if (searchInput && searchInput.value.trim()) {
                performSearch(searchInput.value);
            }
        } catch (error) {
            console.error('Error loading search index:', error);
            displayError('Failed to load search index. Please try again later.');
            isLoading = false;
        }
    }

    // Perform search across all indices
    function performSearch(query) {
        if (isLoading) {
            displayError('Search index is still loading. Please wait...');
            return;
        }

        if (!searchData || !searchData.sites) {
            displayError('Search index not available.');
            return;
        }

        if (!query || query.trim().length === 0) {
            searchResults.innerHTML = '';
            searchPagination.innerHTML = '';
            return;
        }

        currentQuery = query;
        const searchTerms = query.toLowerCase().split(/\s+/).filter(t => t.length > 1);
        let allResults = [];
        const rawLunrResults = [];

        searchData.sites.forEach(site => {
            if (site.docs) {
                const index = lunrIndexes[site.name];
                if (!index) return;
                try {
                    index.search(query).forEach(r => rawLunrResults.push({site, r}));
                } catch(e) {}
            } else {
                allResults = allResults.concat(searchInIndex(site.index_data, searchTerms, site));
            }
        });

        if (rawLunrResults.length > 0) {
            const globalMax = Math.max(...rawLunrResults.map(({r}) => r.score));
            // [THRESHOLD] drop results below 5% of top Lunr score — to revert, replace filteredLunrResults with rawLunrResults on the line below
            const MIN_SCORE_FRACTION = 0.06;
            const filteredLunrResults = rawLunrResults.filter(({r}) => r.score / globalMax >= MIN_SCORE_FRACTION);
            filteredLunrResults.forEach(({site, r}) => {
                const doc = site.docs[parseInt(r.ref)];
                if (!doc) return;
                allResults.push({
                    title: doc.title,
                    url: doc.url,
                    content: doc.content,
                    site: site.name,
                    siteUrl: site.url,
                    score: (r.score / globalMax) * 10 * (SITE_WEIGHTS[site.name] || 1.0),
                });
            });
        }

        allResults.sort((a, b) => b.score - a.score);

        currentResults = allResults;
        currentPage = 1;
        displayResults();
    }

    // Search within a single Sphinx index (fallback for sites without local sources)
    function searchInIndex(indexData, searchTerms, site) {
        const results = [];
        const titles = indexData.titles || [];
        const docurls = indexData.docurls || [];
        const terms = indexData.terms || {};
        const titleterms = indexData.titleterms || {};

        const docScores = {};

        searchTerms.forEach(term => {
            if (terms[term]) {
                const docIndices = Array.isArray(terms[term]) ? terms[term] : [terms[term]];
                docIndices.forEach(docIndex => {
                    docScores[docIndex] = (docScores[docIndex] || 0) + 1;
                });
            }

            if (titleterms[term]) {
                const docIndices = Array.isArray(titleterms[term]) ? titleterms[term] : [titleterms[term]];
                docIndices.forEach(docIndex => {
                    docScores[docIndex] = (docScores[docIndex] || 0) + 5;
                });
            }

            Object.keys(terms).forEach(indexTerm => {
                if (indexTerm.startsWith(term) && indexTerm !== term) {
                    const docIndices = Array.isArray(terms[indexTerm]) ? terms[indexTerm] : [terms[indexTerm]];
                    docIndices.forEach(docIndex => {
                        docScores[docIndex] = (docScores[docIndex] || 0) + 0.5;
                    });
                }
            });

            titles.forEach((title, docIndex) => {
                if (title && title.toLowerCase().includes(term)) {
                    docScores[docIndex] = (docScores[docIndex] || 0) + 3;
                }
            });
        });

        Object.keys(docScores).forEach(docIndex => {
            const idx = parseInt(docIndex);
            if (titles[idx] && docurls[idx]) {
                results.push({
                    title: titles[idx],
                    url: `${site.url}/${docurls[idx]}`,
                    site: site.name,
                    siteUrl: site.url,
                    score: docScores[docIndex],
                });
            }
        });

        return results;
    }

    // Build a context snippet: 20 words either side of the first match, term highlighted
    function buildSnippet(content, query) {
        if (!content) return '';
        const terms = query.toLowerCase().split(/\s+/).filter(t => t.length > 1);
        if (terms.length === 0) return '';

        const lowerContent = content.toLowerCase();
        let bestPos = -1;
        terms.forEach(term => {
            const pos = lowerContent.indexOf(term);
            if (pos !== -1 && (bestPos === -1 || pos < bestPos)) bestPos = pos;
        });

        const words = content.split(/\s+/);
        let wordPos = 0;

        if (bestPos !== -1) {
            let charCount = 0;
            for (let i = 0; i < words.length; i++) {
                if (charCount + words[i].length >= bestPos) { wordPos = i; break; }
                charCount += words[i].length + 1;
            }
        }

        const start = Math.max(0, wordPos - 40);
        const end = Math.min(words.length, wordPos + 41);
        let excerpt = escapeHtml(words.slice(start, end).join(' '));

        terms.forEach(term => {
            const regex = new RegExp(`(${term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
            excerpt = excerpt.replace(regex, '<mark>$1</mark>');
        });

        return (start > 0 ? '...' : '') + excerpt + (end < words.length ? '...' : '');
    }

    // Display search results
    function displayResults() {
        if (currentResults.length === 0) {
            searchResults.innerHTML = '<p class="no-results">No results found. Try different search terms.</p>';
            searchPagination.innerHTML = '';
            return;
        }

        const totalPages = Math.ceil(currentResults.length / resultsPerPage);
        const startIndex = (currentPage - 1) * resultsPerPage;
        const endIndex = Math.min(startIndex + resultsPerPage, currentResults.length);
        const pageResults = currentResults.slice(startIndex, endIndex);

        const siteCount = searchData.metadata.total_sites;
        let html = `<p class="results-count">Found ${currentResults.length} result${currentResults.length !== 1 ? 's' : ''} across ${siteCount} source${siteCount !== 1 ? 's' : ''}</p>`;

        pageResults.forEach(result => {
            const snippet = buildSnippet(result.content, currentQuery);
            html += `
                <div class="search-result">
                    <span class="result-site-badge" data-site="${escapeHtml(result.site)}">${escapeHtml(result.site)}</span>
                    <h3 class="result-title">
                        <a href="${escapeHtml(result.url)}" target="_blank" rel="noopener noreferrer">
                            ${escapeHtml(result.title)}
                        </a>
                    </h3>
                    ${snippet ? `<p class="result-snippet">${snippet}</p>` : ''}
                    <a href="${escapeHtml(result.url)}" class="result-url" target="_blank" rel="noopener noreferrer">
                        ${escapeHtml(result.url)}
                    </a>
                </div>
            `;
        });

        searchResults.innerHTML = html;

        if (totalPages > 1) {
            displayPagination(totalPages);
        } else {
            searchPagination.innerHTML = '';
        }
    }

    // Display pagination controls
    function displayPagination(totalPages) {
        let html = '<div class="pagination-controls">';

        if (currentPage > 1) {
            html += `<button class="page-btn" data-page="${currentPage - 1}">← Previous</button>`;
        }

        const maxButtons = 7;
        let startPage = Math.max(1, currentPage - Math.floor(maxButtons / 2));
        let endPage = Math.min(totalPages, startPage + maxButtons - 1);

        if (endPage - startPage < maxButtons - 1) {
            startPage = Math.max(1, endPage - maxButtons + 1);
        }

        if (startPage > 1) {
            html += `<button class="page-btn" data-page="1">1</button>`;
            if (startPage > 2) html += '<span class="page-dots">...</span>';
        }

        for (let i = startPage; i <= endPage; i++) {
            html += `<button class="page-btn ${i === currentPage ? 'active' : ''}" data-page="${i}">${i}</button>`;
        }

        if (endPage < totalPages) {
            if (endPage < totalPages - 1) html += '<span class="page-dots">...</span>';
            html += `<button class="page-btn" data-page="${totalPages}">${totalPages}</button>`;
        }

        if (currentPage < totalPages) {
            html += `<button class="page-btn" data-page="${currentPage + 1}">Next →</button>`;
        }

        html += '</div>';
        searchPagination.innerHTML = html;

        document.querySelectorAll('.page-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                currentPage = parseInt(this.dataset.page);
                displayResults();
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
        });
    }

    function displayError(message) {
        searchResults.innerHTML = `<p class="search-error">${escapeHtml(message)}</p>`;
        searchPagination.innerHTML = '';
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    const searchPagination = document.getElementById('search-pagination');

    if (searchInput) {
        const debouncedSearch = debounce(function(e) {
            performSearch(e.target.value);
        }, 300);

        searchInput.addEventListener('input', debouncedSearch);
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                performSearch(this.value);
            }
        });

        searchInput.focus();
    }

    loadSearchIndex();
})();
