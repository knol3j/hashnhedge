(function(){
  var enabled = {{ if site.Params.consent_mode }}true{{ else }}false{{ end }};
  if(!enabled) return; // Consent disabled; theme loads AdSense directly

  var banner = document.getElementById('consent-banner');
  var ACCEPT='accepted', REJECT='rejected';

  function saveChoice(val){ try { localStorage.setItem('hh_consent', val); } catch(e){} }
  function getChoice(){ try { return localStorage.getItem('hh_consent'); } catch(e){ return null; } }

  function loadAds(){
    var publisher = '{{ site.Params.adsense_publisher_id }}';
    if(!publisher) return;
    if(document.getElementById('adsbygooglejs')) return;
    var s = document.createElement('script');
    s.id = 'adsbygooglejs';
    s.async = true;
    s.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client='+publisher;
    s.crossOrigin = 'anonymous';
    document.head.appendChild(s);
  }

  function init(){
    var choice = getChoice();
    if(choice === ACCEPT){ loadAds(); return; }
    if(choice === REJECT){ return; }
    if(banner) banner.style.display = 'block';
  }

  document.addEventListener('DOMContentLoaded', function(){
    init();
    var a = document.getElementById('consent-accept');
    var r = document.getElementById('consent-reject');
    if(a) a.addEventListener('click', function(){ saveChoice(ACCEPT); if(banner) banner.remove(); loadAds(); });
    if(r) r.addEventListener('click', function(){ saveChoice(REJECT); if(banner) banner.remove(); });
  });
})();

