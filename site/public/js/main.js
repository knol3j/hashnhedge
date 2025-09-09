
// Hash & Hedge - Optimized JavaScript
(function() {
  'use strict';

  // Performance timing
  const perfData = {
    navigationStart: performance.timing.navigationStart,
    loadComplete: 0,
    firstPaint: 0,
    firstContentfulPaint: 0
  };

  // Lazy loading for images
  function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
      const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src;
            img.classList.add('loaded');
            img.removeAttribute('data-src');
            observer.unobserve(img);
          }
        });
      }, {
        rootMargin: '50px 0px'
      });
      
      images.forEach(img => imageObserver.observe(img));
    } else {
      // Fallback for older browsers
      images.forEach(img => {
        img.src = img.dataset.src;
        img.classList.add('loaded');
        img.removeAttribute('data-src');
      });
    }
  }

  // Service Worker registration
  function registerServiceWorker() {
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
          .then(registration => {
            console.log('SW registered: ', registration);
          })
          .catch(registrationError => {
            console.log('SW registration failed: ', registrationError);
          });
      });
    }
  }

  // Critical resource hints
  function addResourceHints() {
    const head = document.head;
    
    // Preconnect to important domains
    const preconnects = [
      'https://www.googletagmanager.com',
      'https://pagead2.googlesyndication.com',
      'https://fonts.googleapis.com',
      'https://fonts.gstatic.com'
    ];
    
    preconnects.forEach(url => {
      const link = document.createElement('link');
      link.rel = 'preconnect';
      link.href = url;
      if (url.includes('gstatic')) link.crossOrigin = 'anonymous';
      head.appendChild(link);
    });
  }

  // Analytics optimization
  function initAnalytics() {
    // Delay analytics to not block rendering
    setTimeout(() => {
      if (window.gtag) {
        gtag('event', 'page_view', {
          page_title: document.title,
          page_location: window.location.href,
          custom_map: {
            dimension1: 'page_load_time'
          }
        });
      }
    }, 1000);
  }

  // Performance monitoring
  function trackPerformance() {
    if ('PerformanceObserver' in window) {
      // Track Core Web Vitals
      const observer = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          if (entry.entryType === 'paint') {
            perfData[entry.name.replace('-', '_')] = entry.startTime;
          }
          
          if (entry.entryType === 'largest-contentful-paint') {
            if (window.gtag) {
              gtag('event', 'lcp', {
                value: Math.round(entry.startTime),
                event_category: 'Web Vitals'
              });
            }
          }
          
          if (entry.entryType === 'layout-shift') {
            if (!entry.hadRecentInput && window.gtag) {
              gtag('event', 'cls', {
                value: entry.value,
                event_category: 'Web Vitals'
              });
            }
          }
        }
      });
      
      observer.observe({entryTypes: ['paint', 'largest-contentful-paint', 'layout-shift']});
    }
    
    // Track load complete time
    window.addEventListener('load', () => {
      perfData.loadComplete = performance.now();
      
      if (window.gtag) {
        gtag('event', 'page_load_time', {
          value: Math.round(perfData.loadComplete),
          event_category: 'Performance'
        });
      }
    });
  }

  // Smooth scrolling for anchor links
  function initSmoothScrolling() {
    document.addEventListener('click', (e) => {
      if (e.target.matches('a[href^="#"]')) {
        e.preventDefault();
        const target = document.querySelector(e.target.getAttribute('href'));
        if (target) {
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      }
    });
  }

  // Search functionality (if needed)
  function initSearch() {
    const searchInput = document.getElementById('search');
    if (searchInput) {
      let searchTimeout;
      
      searchInput.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
          const query = e.target.value.toLowerCase();
          // Implement search logic here
          console.log('Search query:', query);
        }, 300);
      });
    }
  }

  // Theme toggler (dark/light mode)
  function initThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
      const currentTheme = localStorage.getItem('theme') || 'dark';
      document.documentElement.setAttribute('data-theme', currentTheme);
      
      themeToggle.addEventListener('click', () => {
        const theme = document.documentElement.getAttribute('data-theme');
        const newTheme = theme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
      });
    }
  }

  // Initialize everything when DOM is ready
  function init() {
    initLazyLoading();
    registerServiceWorker();
    addResourceHints();
    initAnalytics();
    trackPerformance();
    initSmoothScrolling();
    initSearch();
    initThemeToggle();
    
    // Mark content as loaded
    document.body.classList.add('loaded');
  }

  // Run initialization
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
