(function() {
    'use strict';
    
    // Configuration
    const config = {
        threshold: 300, // pixels from bottom to trigger load
        loadingClass: 'loading-more',
        errorRetryDelay: 3000
    };
    
    // State management
    let isLoading = false;
    let currentPage = 1;
    let hasMorePages = true;
    let loadingIndicator = null;
    
    // Helper function to parse page number from URL
    function getPageFromURL(url) {
        const match = url.match(/\/page\/(\d+)/);
        return match ? parseInt(match[1]) : 1;
    }
    
    // Initialize current page from URL
    function initCurrentPage() {
        currentPage = getPageFromURL(window.location.pathname);
    }
    
    // Create loading indicator
    function createLoadingIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'infinite-scroll-loader';
        indicator.innerHTML = `
            <div class="loader-content">
                <svg class="loader-spinner" width="40" height="40" viewBox="0 0 40 40">
                    <circle cx="20" cy="20" r="18" fill="none" stroke="currentColor" stroke-width="3" opacity="0.3"></circle>
                    <circle cx="20" cy="20" r="18" fill="none" stroke="currentColor" stroke-width="3" 
                            stroke-dasharray="90" stroke-dashoffset="30"
                            transform="rotate(-90 20 20)">
                        <animateTransform attributeName="transform" type="rotate" 
                                        from="0 20 20" to="360 20 20" dur="1s" repeatCount="indefinite"/>
                    </circle>
                </svg>
                <p>Loading more posts...</p>
            </div>
        `;
        indicator.style.cssText = `
            text-align: center;
            padding: 2rem;
            margin: 2rem auto;
            display: none;
        `;
        return indicator;
    }
    
    // Show/hide loading indicator
    function toggleLoading(show) {
        if (loadingIndicator) {
            loadingIndicator.style.display = show ? 'block' : 'none';
            if (show) {
                document.body.classList.add(config.loadingClass);
            } else {
                document.body.classList.remove(config.loadingClass);
            }
        }
    }
    
    // Check if we're on a page that should have infinite scroll
    function shouldEnableInfiniteScroll() {
        // Enable on homepage and archive/list pages
        const isHomePage = window.location.pathname === '/' || window.location.pathname === '/index.html';
        const isListPage = document.querySelector('.archive') !== null;
        const isPaginatedPage = window.location.pathname.includes('/page/');
        
        return isHomePage || isListPage || isPaginatedPage;
    }
    
    // Find the container for posts based on page type
    function getPostsContainer() {
        // For archive/list pages
        const archiveContainer = document.querySelector('.archive');
        if (archiveContainer) {
            return archiveContainer;
        }
        
        // For homepage - look for the main content wrapper
        const homeContainer = document.querySelector('.wrap.pt-2.mt-2');
        if (homeContainer) {
            return homeContainer;
        }
        
        // Fallback to main content area
        return document.querySelector('main .wrap');
    }
    
    // Find or hide the existing pager
    function handlePager() {
        const pager = document.querySelector('.pager');
        if (pager) {
            // Check if there's a next page link
            const nextLink = pager.querySelector('.pager_next[href]');
            if (nextLink) {
                hasMorePages = true;
            } else {
                hasMorePages = false;
            }
            // Hide the pager as we're using infinite scroll
            pager.style.display = 'none';
        }
    }
    
    // Load next page of posts
    async function loadNextPage() {
        if (isLoading || !hasMorePages) {
            return;
        }
        
        isLoading = true;
        toggleLoading(true);
        
        const nextPage = currentPage + 1;
        let nextPageURL;
        
        // Construct the URL for the next page
        if (window.location.pathname === '/' || window.location.pathname === '/index.html') {
            nextPageURL = `/page/${nextPage}/`;
        } else if (window.location.pathname.includes('/page/')) {
            nextPageURL = window.location.pathname.replace(/\/page\/\d+/, `/page/${nextPage}`);
        } else {
            // For other list pages
            nextPageURL = `${window.location.pathname}page/${nextPage}/`;
        }
        
        try {
            const response = await fetch(nextPageURL);
            
            if (!response.ok) {
                if (response.status === 404) {
                    hasMorePages = false;
                    console.log('No more pages to load');
                } else {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return;
            }
            
            const html = await response.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            
            // Find the posts container in the loaded page
            const container = getPostsContainer();
            if (!container) {
                console.error('Could not find posts container');
                return;
            }
            
            // Extract new posts based on page type
            let newPosts = [];
            
            if (document.querySelector('.archive')) {
                // Archive/list page - get archive items
                newPosts = doc.querySelectorAll('.archive_item');
            } else {
                // Homepage - get articles
                newPosts = doc.querySelectorAll('article.article');
            }
            
            if (newPosts.length > 0) {
                // Append new posts
                newPosts.forEach(post => {
                    // Clone the node to avoid moving it from the parsed document
                    const postClone = post.cloneNode(true);
                    
                    // Add fade-in animation
                    postClone.style.opacity = '0';
                    postClone.style.transform = 'translateY(20px)';
                    postClone.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                    
                    // Insert before the loading indicator or at the end
                    if (loadingIndicator && loadingIndicator.parentNode === container) {
                        container.insertBefore(postClone, loadingIndicator);
                    } else {
                        container.appendChild(postClone);
                    }
                    
                    // Trigger animation
                    setTimeout(() => {
                        postClone.style.opacity = '1';
                        postClone.style.transform = 'translateY(0)';
                    }, 50);
                });
                
                currentPage = nextPage;
                
                // Check if there are more pages
                const nextPager = doc.querySelector('.pager');
                if (nextPager) {
                    const nextLink = nextPager.querySelector('.pager_next[href]');
                    hasMorePages = !!nextLink;
                } else {
                    // If no pager found, assume no more pages
                    hasMorePages = false;
                }
                
                // Update URL without reload (optional)
                if (window.history && window.history.replaceState) {
                    window.history.replaceState(null, '', nextPageURL);
                }
            } else {
                hasMorePages = false;
                console.log('No posts found in the loaded page');
            }
            
        } catch (error) {
            console.error('Error loading next page:', error);
            
            // Retry after delay
            setTimeout(() => {
                isLoading = false;
            }, config.errorRetryDelay);
        } finally {
            isLoading = false;
            toggleLoading(false);
            
            if (!hasMorePages && loadingIndicator) {
                // Show end message
                loadingIndicator.innerHTML = '<p style="color: #666;">No more posts to load</p>';
                loadingIndicator.style.display = 'block';
                setTimeout(() => {
                    loadingIndicator.style.display = 'none';
                }, 3000);
            }
        }
    }
    
    // Check scroll position and load more if needed
    function checkScroll() {
        if (!hasMorePages || isLoading) {
            return;
        }
        
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const scrollHeight = document.documentElement.scrollHeight;
        const clientHeight = document.documentElement.clientHeight;
        
        if (scrollTop + clientHeight >= scrollHeight - config.threshold) {
            loadNextPage();
        }
    }
    
    // Debounce helper
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
    
    // Initialize infinite scroll
    function init() {
        if (!shouldEnableInfiniteScroll()) {
            console.log('Infinite scroll not enabled for this page');
            return;
        }
        
        const container = getPostsContainer();
        if (!container) {
            console.log('No suitable container found for infinite scroll');
            return;
        }
        
        // Initialize current page
        initCurrentPage();
        
        // Handle existing pager
        handlePager();
        
        // Create and append loading indicator
        loadingIndicator = createLoadingIndicator();
        
        // Find the best place to insert the loader
        const pagerWrap = document.querySelector('.wrap .pager')?.parentElement;
        if (pagerWrap) {
            pagerWrap.appendChild(loadingIndicator);
        } else {
            container.appendChild(loadingIndicator);
        }
        
        // Add scroll event listener with debouncing
        const debouncedCheckScroll = debounce(checkScroll, 100);
        window.addEventListener('scroll', debouncedCheckScroll);
        window.addEventListener('resize', debouncedCheckScroll);
        
        // Initial check in case the page is short
        setTimeout(checkScroll, 100);
        
        console.log('Infinite scroll initialized');
    }
    
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        // DOM is already ready
        init();
    }
    
    // Expose API for debugging
    window.infiniteScroll = {
        loadNextPage,
        getCurrentPage: () => currentPage,
        hasMore: () => hasMorePages,
        isLoading: () => isLoading
    };
})();
