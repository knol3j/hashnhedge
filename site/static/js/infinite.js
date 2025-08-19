// Basic infinite scroll: fetch next page and append articles
(function(){
  function $(sel){ return document.querySelector(sel); }
  var grid = $('#post-grid');
  var nextLink = $('#next-link');
  var loadMoreBtn = $('#load-more');
  if(!grid || !nextLink) return;

  var loading = false;
  var done = false;

  async function loadNext(){
    if(loading || done) return;
    loading = true;
    try{
      var url = nextLink.getAttribute('href');
      if(!url){ done = true; return; }
      var res = await fetch(url, { credentials: 'same-origin' });
      if(!res.ok){ done = true; return; }
      var html = await res.text();
      var tmp = document.createElement('div');
      tmp.innerHTML = html;
      var newGrid = tmp.querySelector('#post-grid');
      var newNext = tmp.querySelector('#next-link');
      if(newGrid){
        newGrid.querySelectorAll('article.card').forEach(function(card){ grid.appendChild(card); });
      }
      if(newNext){
        nextLink.setAttribute('href', newNext.getAttribute('href'));
      } else {
        done = true;
      }
      if(loadMoreBtn){ loadMoreBtn.style.display = done ? 'none' : 'inline-block'; }
    }catch(e){ done = true; }
    finally{ loading = false; }
  }

  // Show fallback button if there is a next page
  if(loadMoreBtn){
    loadMoreBtn.addEventListener('click', function(){ loadNext(); });
  }

  // Infinite scroll via IntersectionObserver; fallback to button only if unsupported
  if('IntersectionObserver' in window){
    var sentinel = document.createElement('div');
    sentinel.id = 'infinite-sentinel';
    sentinel.style.height = '1px';
    document.body.appendChild(sentinel);

    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        if(entry.isIntersecting){ loadNext(); }
      });
    });
    io.observe(sentinel);
  }

  // Initialize button visibility
  if(loadMoreBtn){ loadMoreBtn.style.display = nextLink.getAttribute('href') ? 'inline-block' : 'none'; }
})();

