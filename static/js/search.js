// Search page JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    initializeSearch();
});

function initializeSearch() {
    const searchInput = document.querySelector('.search-input');
    const searchForm = document.querySelector('.search-form');
    
    // Focus on search input when page loads
    if (searchInput && !searchInput.value) {
        searchInput.focus();
    }
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K to focus search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            if (searchInput) {
                searchInput.focus();
                searchInput.select();
            }
        }
        
        // Enter key to submit form when focused on input
        if (e.key === 'Enter' && document.activeElement === searchInput) {
            e.preventDefault();
            searchForm.submit();
        }
    });
    
    // Add loading state to search button
    if (searchForm) {
        searchForm.addEventListener('submit', function() {
            const searchBtn = document.querySelector('.search-btn');
            if (searchBtn) {
                searchBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i><span>Searching...</span>';
                searchBtn.disabled = true;
            }
        });
    }
    
    // Add smooth scrolling to result sections
    const resultSections = document.querySelectorAll('.result-section');
    resultSections.forEach(section => {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, { threshold: 0.1 });
        
        section.style.opacity = '0';
        section.style.transform = 'translateY(20px)';
        section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        
        observer.observe(section);
    });
}

// Utility function to highlight search terms in results
function highlightSearchTerms() {
    const searchQuery = document.querySelector('.search-input')?.value?.trim();
    if (!searchQuery) return;
    
    const terms = searchQuery.split(' ').filter(term => term.length > 2);
    const textNodes = [];
    
    // Find all text nodes in result cards
    const resultCards = document.querySelectorAll('.result-card, .result-table');
    resultCards.forEach(card => {
        const walker = document.createTreeWalker(
            card,
            NodeFilter.SHOW_TEXT,
            null,
            false
        );
        
        let node;
        while (node = walker.nextNode()) {
            if (node.nodeValue.trim()) {
                textNodes.push(node);
            }
        }
    });
    
    // Highlight terms
    textNodes.forEach(node => {
        let content = node.nodeValue;
        terms.forEach(term => {
            const regex = new RegExp(`(${term})`, 'gi');
            content = content.replace(regex, '<mark>$1</mark>');
        });
        
        if (content !== node.nodeValue) {
            const span = document.createElement('span');
            span.innerHTML = content;
            node.parentNode.replaceChild(span, node);
        }
    });
}

// Call highlight function after DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(highlightSearchTerms, 100);
});
