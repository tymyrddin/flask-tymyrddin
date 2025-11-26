(function() {
    let searchData = null;
    let isLoading = true;
    const resultsPerPage = 10;
    let currentPage = 1;
    let currentResults = [];

    // Load the combined search index
    async function loadSearchIndex() {
        try {
            const response = await fetch('/static/search/index.json');
            searchData = await response.json();
            isLoading = false;
            console.log(`Loaded search index: ${searchData.metadata.total_sites} sites, ${searchData.metadata.total_documents} documents`);
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

        const searchTerms = query.toLowerCase().split(/\s+/).filter(t => t.length > 1);
        let allResults = [];

        searchData.sites.forEach(site => {
            const siteResults = searchInIndex(site.index_data, searchTerms, site);
            allResults = allResults.concat(siteResults);
        });

        // Sort by relevance score
        allResults.sort((a, b) => b.score - a.score);

        currentResults = allResults;
        currentPage = 1;
        displayResults();
    }

    // Search within a single Sphinx index
    function searchInIndex(indexData, searchTerms, site) {
        const results = [];
        const titles = indexData.titles || [];
        const docurls = indexData.docurls || [];
        const terms = indexData.terms || {};
        const titleterms = indexData.titleterms || {};

        // Create a map of document scores
        const docScores = {};

        searchTerms.forEach(term => {
            // Search in content terms
            if (terms[term]) {
                const docIndices = Array.isArray(terms[term]) ? terms[term] : [terms[term]];
                docIndices.forEach(docIndex => {
                    docScores[docIndex] = (docScores[docIndex] || 0) + 1;
                });
            }

            // Search in title terms (higher weight)
            if (titleterms[term]) {
                const docIndices = Array.isArray(titleterms[term]) ? titleterms[term] : [titleterms[term]];
                docIndices.forEach(docIndex => {
                    docScores[docIndex] = (docScores[docIndex] || 0) + 5;
                });
            }

            // Partial matches in terms (for stemming/prefix matching)
            Object.keys(terms).forEach(indexTerm => {
                if (indexTerm.startsWith(term) && indexTerm !== term) {
                    const docIndices = Array.isArray(terms[indexTerm]) ? terms[indexTerm] : [terms[indexTerm]];
                    docIndices.forEach(docIndex => {
                        docScores[docIndex] = (docScores[docIndex] || 0) + 0.5;
                    });
                }
            });

            // Partial matches in titles
            titles.forEach((title, docIndex) => {
                if (title && title.toLowerCase().includes(term)) {
                    docScores[docIndex] = (docScores[docIndex] || 0) + 3;
                }
            });
        });

        // Convert to results array
        Object.keys(docScores).forEach(docIndex => {
            const idx = parseInt(docIndex);
            if (titles[idx] && docurls[idx]) {
                const docurl = docurls[idx];
                // docurls already contain the full path, just prepend site URL
                const url = `${site.url}/${docurl}`;

                results.push({
                    title: titles[idx],
                    docurl: docurl,
                    url: url,
                    site: site.name,
                    siteUrl: site.url,
                    score: docScores[docIndex]
                });
            }
        });

        return results;
    }

    // Display search results
    function displayResults() {
        if (currentResults.length === 0) {
            searchResults.innerHTML = '<p class="no-results">No results found. Try different search terms.</p>';
            searchPagination.innerHTML = '';
            return;
        }

        // Calculate pagination
        const totalPages = Math.ceil(currentResults.length / resultsPerPage);
        const startIndex = (currentPage - 1) * resultsPerPage;
        const endIndex = Math.min(startIndex + resultsPerPage, currentResults.length);
        const pageResults = currentResults.slice(startIndex, endIndex);

        // Display results
        const siteCount = searchData.metadata.total_sites;
        let html = `<p class="results-count">Found ${currentResults.length} result${currentResults.length !== 1 ? 's' : ''} across ${siteCount} documentation site${siteCount !== 1 ? 's' : ''}</p>`;

        pageResults.forEach(result => {
            html += `
                <div class="search-result">
                    <span class="result-site-badge" data-site="${escapeHtml(result.site)}">${escapeHtml(result.site)}</span>
                    <h3 class="result-title">
                        <a href="${escapeHtml(result.url)}" target="_blank" rel="noopener noreferrer">
                            ${escapeHtml(result.title)}
                        </a>
                    </h3>
                    <a href="${escapeHtml(result.url)}" class="result-url" target="_blank" rel="noopener noreferrer">
                        ${escapeHtml(result.url)}
                    </a>
                </div>
            `;
        });

        searchResults.innerHTML = html;

        // Display pagination
        if (totalPages > 1) {
            displayPagination(totalPages);
        } else {
            searchPagination.innerHTML = '';
        }
    }

    // Display pagination controls
    function displayPagination(totalPages) {
        let html = '<div class="pagination-controls">';

        // Previous button
        if (currentPage > 1) {
            html += `<button class="page-btn" data-page="${currentPage - 1}">← Previous</button>`;
        }

        // Page numbers
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

        // Next button
        if (currentPage < totalPages) {
            html += `<button class="page-btn" data-page="${currentPage + 1}">Next →</button>`;
        }

        html += '</div>';
        searchPagination.innerHTML = html;

        // Add click handlers to pagination buttons
        document.querySelectorAll('.page-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                currentPage = parseInt(this.dataset.page);
                displayResults();
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
        });
    }

    // Display error message
    function displayError(message) {
        searchResults.innerHTML = `<p class="search-error">${escapeHtml(message)}</p>`;
        searchPagination.innerHTML = '';
    }

    // Escape HTML to prevent XSS
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Debounce function
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

    // Get DOM elements
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    const searchPagination = document.getElementById('search-pagination');

    // Event listeners
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

        // Auto-focus search input
        searchInput.focus();
    }

    // Initialize - load the combined search index
    loadSearchIndex();
})();
