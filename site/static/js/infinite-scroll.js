/**
 * Hash & Hedge Infinite Scroll
 * Smoothly loads more posts as user scrolls
 */

class HashHedgeInfiniteScroll {
  constructor() {
    this.config = window.hashHedgeInfiniteScroll || {};
    this.postsContainer = document.getElementById('posts-container');
    this.loadingIndicator = document.getElementById('loading-indicator');
    this.endIndicator = document.getElementById('end-indicator');
    
    this.currentPage = this.config.currentPage || 1;
    this.postsPerPage = this.config.postsPerPage || 12;
    this.totalPosts = this.config.totalPosts || 0;
    this.allPosts = this.config.allPostsData || [];
    this.loading = false;
    
    this.init();
  }
  
  init() {
    // Set up scroll listener
    window.addEventListener('scroll', this.throttle(this.handleScroll.bind(this), 250));
    
    // Set up intersection observer for better performance
    this.setupIntersectionObserver();
    
    console.log(`🚀 Hash & Hedge Infinite Scroll initialized with ${this.totalPosts} posts`);
  }
  
  setupIntersectionObserver() {
    // Create a sentinel element to trigger loading
    this.sentinel = document.createElement('div');
    this.sentinel.id = 'scroll-sentinel';
    this.sentinel.style.height = '10px';
    this.sentinel.style.margin = '0';
    
    // Insert sentinel before loading indicator
    this.loadingIndicator.parentNode.insertBefore(this.sentinel, this.loadingIndicator);
    
    // Set up intersection observer
    this.observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !this.loading) {
          this.loadMorePosts();
        }
      });
    }, {
      rootMargin: '100px' // Trigger 100px before the sentinel comes into view
    });
    
    this.observer.observe(this.sentinel);
  }
  
  handleScroll() {
    // Fallback scroll handler (in case intersection observer isn't supported)
    if (this.loading) return;
    
    const scrollTop = window.pageYOffset;
    const windowHeight = window.innerHeight;
    const documentHeight = document.documentElement.scrollHeight;
    
    // Trigger when user is 200px from bottom
    if (scrollTop + windowHeight >= documentHeight - 200) {
      this.loadMorePosts();
    }
  }
  
  async loadMorePosts() {
    if (this.loading) return;
    
    const startIndex = this.currentPage * this.postsPerPage;
    const endIndex = startIndex + this.postsPerPage;
    
    // Check if we have more posts to load
    if (startIndex >= this.totalPosts) {
      this.showEndIndicator();
      return;
    }
    
    this.loading = true;
    this.showLoadingIndicator();
    
    try {
      // Get next batch of posts
      const nextPosts = this.allPosts.slice(startIndex, endIndex);
      
      // Simulate network delay for smooth UX (remove in production if desired)
      await this.delay(300);
      
      // Render new posts
      this.renderPosts(nextPosts, startIndex);
      
      // Update state
      this.currentPage++;
      
      console.log(`📚 Loaded page ${this.currentPage}, showing ${endIndex} of ${this.totalPosts} posts`);
      
    } catch (error) {
      console.error('❌ Error loading posts:', error);
      this.showErrorMessage();
    } finally {
      this.loading = false;
      this.hideLoadingIndicator();
    }
  }
  
  renderPosts(posts, startIndex) {
    const fragment = document.createDocumentFragment();
    
    posts.forEach((post, index) => {
      const postElement = this.createPostElement(post, startIndex + index);
      fragment.appendChild(postElement);
    });
    
    // Add posts to container with staggered animation
    this.postsContainer.appendChild(fragment);
    
    // Trigger animations
    setTimeout(() => {
      const newPosts = this.postsContainer.querySelectorAll('.article.new-post');
      newPosts.forEach((post, index) => {
        post.style.setProperty('--post-index', index);
        post.classList.add('animate');
      });
    }, 50);
  }
  
  createPostElement(post, index) {
    const article = document.createElement('article');
    article.className = 'article mb-2 new-post';
    article.setAttribute('data-post-id', index);
    
    article.innerHTML = `
      <a href="${post.permalink}">
        <div class="article_thumb" style="background-image: url(${post.image})"></div>
        <div class="article_meta">
          <time class="post_date">${post.date}</time>
          <h3 class="article_title">${post.title}</h3>
          <div class="article_excerpt">
            <p>${post.summary}</p>
          </div>
        </div>
      </a>
    `;
    
    return article;
  }
  
  showLoadingIndicator() {
    this.loadingIndicator.style.display = 'block';
  }
  
  hideLoadingIndicator() {
    this.loadingIndicator.style.display = 'none';
  }
  
  showEndIndicator() {
    this.hideLoadingIndicator();
    this.endIndicator.style.display = 'block';
    
    // Update end indicator text with final count
    const endText = this.endIndicator.querySelector('p');
    if (endText) {
      endText.innerHTML = `🎉 You've explored all ${this.totalPosts} stories! Thanks for reading Hash & Hedge.`;
    }
    
    // Disconnect observer since we're done
    if (this.observer) {
      this.observer.disconnect();
    }
  }
  
  showErrorMessage() {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.style.cssText = 'text-align: center; padding: 2rem; color: #e74c3c;';
    errorDiv.innerHTML = `
      <p>❌ Oops! Something went wrong loading more posts.</p>
      <button onclick="location.reload()" style="background: #663399; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer;">
        Try Again
      </button>
    `;
    
    this.loadingIndicator.parentNode.insertBefore(errorDiv, this.loadingIndicator);
  }
  
  // Utility functions
  throttle(func, limit) {
    let inThrottle;
    return function() {
      const args = arguments;
      const context = this;
      if (!inThrottle) {
        func.apply(context, args);
        inThrottle = true;
        setTimeout(() => inThrottle = false, limit);
      }
    }
  }
  
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  new HashHedgeInfiniteScroll();
});

// Add smooth scroll behavior for better UX
document.documentElement.style.scrollBehavior = 'smooth';