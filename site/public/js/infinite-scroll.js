/**
 * Infinite Scroll Implementation for Hash & Hedge
 * Loads 20 posts at a time with smooth scrolling experience
 */

class InfiniteScroll {
    constructor() {
        this.currentPage = 1;
        this.totalPages = 1;
        this.loading = false;
        this.hasNextPage = true;
        this.baseURL = '';
        
        this.init();
    }

    init() {
        this.postsContainer = document.getElementById('posts-container');
        this.loadingIndicator = document.getElementById('loading-indicator');
        
        if (!this.postsContainer) {
            console.warn('Posts container not found');
            return;
        }

        this.setupScrollListener();
        this.setupLoadingIndicator();
        
        // Get initial page info from data attributes
        const initialPageData = this.postsContainer.dataset;
        if (initialPageData.currentPage) {
            this.currentPage = parseInt(initialPageData.currentPage);
        }
        if (initialPageData.totalPages) {
            this.totalPages = parseInt(initialPageData.totalPages);
        }
        if (initialPageData.hasNext) {
            this.hasNextPage = initialPageData.hasNext === 'true';
        }
    }

    setupLoadingIndicator() {
        if (!this.loadingIndicator) {
            this.loadingIndicator = document.createElement('div');
            this.loadingIndicator.id = 'loading-indicator';
            this.loadingIndicator.className = 'loading-indicator hidden';
            this.loadingIndicator.innerHTML = `
                <div class="loading-spinner">
                    <div class="spinner"></div>
                    <p>Loading more stories...</p>
                </div>
            `;
            document.body.appendChild(this.loadingIndicator);
        }
    }

    setupScrollListener() {
        let throttleTimeout = null;
        
        window.addEventListener('scroll', () => {
            if (throttleTimeout) return;
            
            throttleTimeout = setTimeout(() => {
                throttleTimeout = null;
                this.handleScroll();
            }, 100);
        });
    }

    handleScroll() {
        if (this.loading || !this.hasNextPage) return;

        const scrollHeight = document.documentElement.scrollHeight;
        const scrollTop = document.documentElement.scrollTop;
        const clientHeight = document.documentElement.clientHeight;
        
        // Load more when user is 200px from bottom
        if (scrollTop + clientHeight >= scrollHeight - 200) {
            this.loadMorePosts();
        }
    }

    async loadMorePosts() {
        if (this.loading || !this.hasNextPage) return;
        
        this.loading = true;
        this.showLoading();
        
        try {
            const nextPage = this.currentPage + 1;
            const response = await fetch(`/page/${nextPage}/index.json`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.posts && data.posts.length > 0) {
                this.renderPosts(data.posts);
                this.currentPage = data.page;
                this.hasNextPage = data.hasNext;
                this.totalPages = data.totalPages;
            } else {
                this.hasNextPage = false;
            }
            
        } catch (error) {
            console.error('Error loading more posts:', error);
            this.showError();
        } finally {
            this.loading = false;
            this.hideLoading();
        }
    }

    renderPosts(posts) {
        const fragment = document.createDocumentFragment();
        
        posts.forEach(post => {
            const postElement = this.createPostElement(post);
            fragment.appendChild(postElement);
        });
        
        this.postsContainer.appendChild(fragment);
        
        // Fade in animation
        const newPosts = this.postsContainer.querySelectorAll('.post-item:not(.loaded)');
        newPosts.forEach((post, index) => {
            setTimeout(() => {
                post.classList.add('loaded');
            }, index * 50);
        });
    }

    createPostElement(post) {
        const article = document.createElement('article');
        article.className = 'post-item';
        
        const readingTime = post.readingTime > 1 ? `${post.readingTime} min read` : '1 min read';
        const postDate = new Date(post.date).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
        
        article.innerHTML = `
            <div class="post-card">
                <div class="post-image">
                    <img src="${post.image}" alt="${post.title}" loading="lazy">
                    <div class="post-category">${post.category}</div>
                </div>
                <div class="post-content">
                    <h2 class="post-title">
                        <a href="${post.url}">${post.title}</a>
                    </h2>
                    <p class="post-summary">${post.summary}</p>
                    <div class="post-meta">
                        <span class="post-date">${postDate}</span>
                        <span class="post-reading-time">${readingTime}</span>
                    </div>
                </div>
            </div>
        `;
        
        return article;
    }

    showLoading() {
        if (this.loadingIndicator) {
            this.loadingIndicator.classList.remove('hidden');
        }
    }

    hideLoading() {
        if (this.loadingIndicator) {
            this.loadingIndicator.classList.add('hidden');
        }
    }

    showError() {
        const errorMsg = document.createElement('div');
        errorMsg.className = 'load-error';
        errorMsg.innerHTML = `
            <p>Unable to load more posts. <button onclick="location.reload()">Refresh page</button></p>
        `;
        this.postsContainer.appendChild(errorMsg);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new InfiniteScroll();
});

// Add CSS for loading animations
const style = document.createElement('style');
style.textContent = `
    .loading-indicator {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(0, 0, 0, 0.8);
        color: white;
        padding: 15px 25px;
        border-radius: 25px;
        z-index: 1000;
        transition: opacity 0.3s ease;
    }
    
    .loading-indicator.hidden {
        opacity: 0;
        pointer-events: none;
    }
    
    .loading-spinner {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .spinner {
        width: 20px;
        height: 20px;
        border: 2px solid #ffffff33;
        border-top: 2px solid #ffffff;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .post-item {
        opacity: 0;
        transform: translateY(20px);
        transition: all 0.5s ease;
    }
    
    .post-item.loaded {
        opacity: 1;
        transform: translateY(0);
    }
    
    .load-error {
        text-align: center;
        padding: 20px;
        background: #f8f9fa;
        margin: 20px 0;
        border-radius: 8px;
    }
    
    .load-error button {
        background: #007bff;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        cursor: pointer;
        margin-left: 10px;
    }
`;
document.head.appendChild(style);