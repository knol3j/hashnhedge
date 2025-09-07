/**
 * Secure Storage Utility for Hash & Hedge
 * Implements encrypted session-based storage with secure cookie handling
 * Follows security best practices for sensitive data protection
 */

class SecureStorage {
    constructor() {
        this.sessionPrefix = 'hh_session_';
        this.encryptionKey = this.generateSessionKey();
        this.maxAge = 24 * 60 * 60 * 1000; // 24 hours
        this.secureCookieOptions = {
            secure: true,           // HTTPS only
            httpOnly: false,        // Allow JS access for client-side operations
            sameSite: 'Strict',     // CSRF protection
            path: '/',
            maxAge: this.maxAge
        };
    }

    /**
     * Generate a cryptographically secure session key
     * @returns {string} Base64 encoded key
     */
    generateSessionKey() {
        const array = new Uint8Array(32);
        crypto.getRandomValues(array);
        return btoa(String.fromCharCode.apply(null, array));
    }

    /**
     * Simple XOR encryption for sensitive data
     * Note: For production use, consider implementing AES-GCM
     * @param {string} data - Data to encrypt
     * @param {string} key - Encryption key
     * @returns {string} Encrypted data
     */
    encrypt(data, key) {
        if (!data || !key) return '';
        
        const keyBytes = atob(key);
        let encrypted = '';
        
        for (let i = 0; i < data.length; i++) {
            const keyByte = keyBytes.charCodeAt(i % keyBytes.length);
            const dataByte = data.charCodeAt(i);
            encrypted += String.fromCharCode(dataByte ^ keyByte);
        }
        
        return btoa(encrypted);
    }

    /**
     * Decrypt data using XOR
     * @param {string} encryptedData - Encrypted data to decrypt
     * @param {string} key - Decryption key
     * @returns {string} Decrypted data
     */
    decrypt(encryptedData, key) {
        if (!encryptedData || !key) return '';
        
        try {
            const encrypted = atob(encryptedData);
            const keyBytes = atob(key);
            let decrypted = '';
            
            for (let i = 0; i < encrypted.length; i++) {
                const keyByte = keyBytes.charCodeAt(i % keyBytes.length);
                const encryptedByte = encrypted.charCodeAt(i);
                decrypted += String.fromCharCode(encryptedByte ^ keyByte);
            }
            
            return decrypted;
        } catch (e) {
            console.warn('Decryption failed:', e);
            return '';
        }
    }

    /**
     * Set secure cookie with only a session key
     * Sensitive data is stored encrypted in sessionStorage
     * @param {string} name - Cookie name
     * @param {*} sensitiveData - Sensitive data to store securely
     * @param {Object} options - Additional cookie options
     */
    setSecureData(name, sensitiveData, options = {}) {
        try {
            // Generate unique session ID for this data
            const sessionId = this.generateSessionId();
            const sessionKey = `${this.sessionPrefix}${name}_${sessionId}`;
            
            // Encrypt sensitive data
            const encryptedData = this.encrypt(JSON.stringify(sensitiveData), this.encryptionKey);
            
            // Store encrypted data in sessionStorage
            sessionStorage.setItem(sessionKey, encryptedData);
            
            // Only store the session key in cookie (not the sensitive data)
            this.setSecureCookie(name, sessionKey, options);
            
            console.info(`Secure data stored for: ${name}`);
        } catch (error) {
            console.error('Failed to store secure data:', error);
        }
    }

    /**
     * Retrieve sensitive data using session key from cookie
     * @param {string} name - Cookie name
     * @returns {*} Decrypted sensitive data or null
     */
    getSecureData(name) {
        try {
            // Get session key from cookie
            const sessionKey = this.getCookie(name);
            if (!sessionKey) return null;
            
            // Retrieve encrypted data from sessionStorage
            const encryptedData = sessionStorage.getItem(sessionKey);
            if (!encryptedData) return null;
            
            // Decrypt and parse data
            const decryptedData = this.decrypt(encryptedData, this.encryptionKey);
            return decryptedData ? JSON.parse(decryptedData) : null;
            
        } catch (error) {
            console.error('Failed to retrieve secure data:', error);
            return null;
        }
    }

    /**
     * Set secure cookie with recommended security settings
     * @param {string} name - Cookie name
     * @param {string} value - Cookie value (should be non-sensitive session key)
     * @param {Object} options - Cookie options
     */
    setSecureCookie(name, value, options = {}) {
        const cookieOptions = { ...this.secureCookieOptions, ...options };
        
        let cookieString = `${encodeURIComponent(name)}=${encodeURIComponent(value)}`;
        
        if (cookieOptions.maxAge) {
            cookieString += `; Max-Age=${cookieOptions.maxAge}`;
        }
        
        if (cookieOptions.path) {
            cookieString += `; Path=${cookieOptions.path}`;
        }
        
        if (cookieOptions.secure) {
            cookieString += `; Secure`;
        }
        
        if (cookieOptions.sameSite) {
            cookieString += `; SameSite=${cookieOptions.sameSite}`;
        }
        
        // Note: HttpOnly cannot be set from JavaScript
        // For truly HttpOnly cookies, set them server-side
        
        document.cookie = cookieString;
    }

    /**
     * Get cookie value by name
     * @param {string} name - Cookie name
     * @returns {string|null} Cookie value or null
     */
    getCookie(name) {
        const nameEQ = encodeURIComponent(name) + "=";
        const ca = document.cookie.split(';');
        
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) === 0) {
                return decodeURIComponent(c.substring(nameEQ.length, c.length));
            }
        }
        return null;
    }

    /**
     * Delete cookie and associated session data
     * @param {string} name - Cookie name
     */
    deleteSecureData(name) {
        try {
            // Get session key from cookie before deleting
            const sessionKey = this.getCookie(name);
            
            // Remove session data
            if (sessionKey) {
                sessionStorage.removeItem(sessionKey);
            }
            
            // Delete cookie
            document.cookie = `${encodeURIComponent(name)}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/`;
            
            console.info(`Secure data deleted for: ${name}`);
        } catch (error) {
            console.error('Failed to delete secure data:', error);
        }
    }

    /**
     * Generate a unique session ID
     * @returns {string} Session ID
     */
    generateSessionId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }

    /**
     * Clear all session data (for logout scenarios)
     */
    clearAllSessions() {
        try {
            // Remove all session storage items with our prefix
            Object.keys(sessionStorage).forEach(key => {
                if (key.startsWith(this.sessionPrefix)) {
                    sessionStorage.removeItem(key);
                }
            });
            
            // Clear all cookies (be careful with this in production)
            document.cookie.split(";").forEach(cookie => {
                const eqPos = cookie.indexOf("=");
                const name = eqPos > -1 ? cookie.substr(0, eqPos).trim() : cookie.trim();
                if (name) {
                    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/`;
                }
            });
            
            console.info('All sessions cleared');
        } catch (error) {
            console.error('Failed to clear sessions:', error);
        }
    }

    /**
     * Security health check
     * @returns {Object} Security status report
     */
    securityHealthCheck() {
        const report = {
            https: location.protocol === 'https:',
            sessionStorage: typeof sessionStorage !== 'undefined',
            cryptoApi: typeof crypto !== 'undefined' && typeof crypto.getRandomValues === 'function',
            cookieSupport: navigator.cookieEnabled,
            recommendations: []
        };

        if (!report.https) {
            report.recommendations.push('Enable HTTPS for secure cookie transmission');
        }

        if (!report.cryptoApi) {
            report.recommendations.push('Crypto API not available - encryption may be weak');
        }

        if (!report.cookieSupport) {
            report.recommendations.push('Cookies disabled - session management unavailable');
        }

        return report;
    }
}

// Initialize secure storage instance
window.secureStorage = new SecureStorage();

// Example usage and migration helper for existing localStorage
(function migrateExistingData() {
    const colorMode = localStorage.getItem('colorMode');
    if (colorMode) {
        // Migrate existing color preference securely
        window.secureStorage.setSecureData('userPreferences', { colorMode }, { maxAge: 365 * 24 * 60 * 60 * 1000 }); // 1 year for preferences
        localStorage.removeItem('colorMode');
        console.info('Color mode preference migrated to secure storage');
    }
})();

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SecureStorage;
}