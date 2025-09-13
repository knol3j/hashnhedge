// Hash & Hedge Monetization Tracking System
// Track affiliate clicks, newsletter signups, and premium conversions

(function() {
    'use strict';
    
    // Configuration
    const config = {
        affiliates: {
            binance: 'HASHNHEDGE',
            coinbase: 'HASHNHEDGE',
            kraken: 'HASHNHEDGE',
            bybit: 'HASHNHEDGE',
            ledger: 'hashnhedge',
            trezor: 'HASHNHEDGE',
            tradingview: 'hashnhedge',
            cointracking: 'HASHNHEDGE'
        },
        analytics: {
            gtag: 'G-4BD4Z2JKW3'
        }
    };
    
    // Track Affiliate Clicks
    function trackAffiliateClick(partner, product) {
        if (typeof gtag !== 'undefined') {
            gtag('event', 'affiliate_click', {
                'event_category': 'monetization',
                'event_label': partner,
                'value': product
            });
        }
        
        // Store in localStorage for attribution
        const clickData = {
            partner: partner,
            product: product,
            timestamp: new Date().toISOString(),
            page: window.location.pathname
        };
        
        let affiliateClicks = JSON.parse(localStorage.getItem('hh_affiliate_clicks') || '[]');
        affiliateClicks.push(clickData);
        localStorage.setItem('hh_affiliate_clicks', JSON.stringify(affiliateClicks));
    }
    
    // Track Newsletter Signups
    function trackNewsletterSignup(source) {
        if (typeof gtag !== 'undefined') {
            gtag('event', 'newsletter_signup', {
                'event_category': 'engagement',
                'event_label': source,
                'value': 1
            });
        }
    }
    
    // Track Premium Conversions
    function trackPremiumConversion(tier, price) {
        if (typeof gtag !== 'undefined') {
            gtag('event', 'purchase', {
                'currency': 'USD',
                'value': price,
                'items': [{
                    'item_id': 'premium_' + tier,
                    'item_name': 'Hash & Hedge Premium ' + tier,
                    'price': price,
                    'quantity': 1
                }]
            });
        }
    }
    
    // Auto-track affiliate links
    document.addEventListener('DOMContentLoaded', function() {
        // Find all affiliate links
        const affiliateLinks = document.querySelectorAll('a[href*="ref="], a[href*="invite?ref="], a[href*="join/"]');
        
        affiliateLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                const href = this.href;
                let partner = 'unknown';
                let product = 'general';
                
                // Identify partner
                if (href.includes('binance.com')) {
                    partner = 'binance';
                    product = 'exchange';
                } else if (href.includes('coinbase.com')) {
                    partner = 'coinbase';
                    product = 'exchange';
                } else if (href.includes('kraken.com')) {
                    partner = 'kraken';
                    product = 'exchange';
                } else if (href.includes('bybit.com')) {
                    partner = 'bybit';
                    product = 'derivatives';
                } else if (href.includes('ledger.com')) {
                    partner = 'ledger';
                    product = 'hardware_wallet';
                } else if (href.includes('trezor.io')) {
                    partner = 'trezor';
                    product = 'hardware_wallet';
                } else if (href.includes('tradingview.com')) {
                    partner = 'tradingview';
                    product = 'charting';
                } else if (href.includes('cointracking.info')) {
                    partner = 'cointracking';
                    product = 'tax_software';
                }
                
                trackAffiliateClick(partner, product);
            });
        });
        
        // Track newsletter form submissions
        const newsletterForms = document.querySelectorAll('.newsletter-form');
        newsletterForms.forEach(form => {
            form.addEventListener('submit', function(e) {
                const source = this.getAttribute('data-source') || 'sidebar';
                trackNewsletterSignup(source);
            });
        });
    });
    
    // Exit Intent Popup for Newsletter
    let exitIntentShown = false;
    document.addEventListener('mouseleave', function(e) {
        if (e.clientY <= 0 && !exitIntentShown && !localStorage.getItem('hh_exit_popup_shown')) {
            exitIntentShown = true;
            localStorage.setItem('hh_exit_popup_shown', 'true');
            showExitPopup();
        }
    });
    
    function showExitPopup() {
        const popup = document.createElement('div');
        popup.className = 'exit-popup';
        popup.innerHTML = `
            <div class="exit-popup-content">
                <button class="close-popup" onclick="this.parentElement.parentElement.remove()">×</button>
                <h2>Wait! Don't Miss Out on Free Crypto Alpha</h2>
                <p>Get our exclusive market analysis and trading signals:</p>
                <ul>
                    <li>✓ Daily profit opportunities</li>
                    <li>✓ DeFi yield strategies</li>
                    <li>✓ Early coin alerts</li>
                </ul>
                <form class="newsletter-form" data-source="exit_intent">
                    <input type="email" placeholder="Enter your email" required>
                    <button type="submit">Get Free Alpha</button>
                </form>
            </div>
        `;
        document.body.appendChild(popup);
    }
    
    // Expose functions globally
    window.HHMonetization = {
        trackAffiliateClick: trackAffiliateClick,
        trackNewsletterSignup: trackNewsletterSignup,
        trackPremiumConversion: trackPremiumConversion
    };
    
})();