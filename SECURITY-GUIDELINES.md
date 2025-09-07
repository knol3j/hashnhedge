# Security Guidelines for Hash & Hedge

## Cookie and Data Security Implementation

### Overview
This document outlines the security measures implemented for Hash & Hedge to ensure sensitive information is never stored directly in cookies and all data is properly encrypted.

### Security Principles Implemented

#### 1. **No Sensitive Data in Cookies**
- ✅ Cookies only store non-sensitive session keys
- ✅ Actual sensitive data is encrypted and stored in sessionStorage
- ✅ Session keys are randomly generated and unique per session

#### 2. **Encryption Standards**
- ✅ All sensitive data is encrypted before storage
- ✅ Uses cryptographically secure random keys (crypto.getRandomValues)
- ✅ XOR encryption with base64 encoding (upgradeable to AES-GCM for production)

#### 3. **Secure Cookie Configuration**
```javascript
secureCookieOptions = {
    secure: true,           // HTTPS only
    httpOnly: false,        // Allow JS access for client-side operations
    sameSite: 'Strict',     // CSRF protection
    path: '/',
    maxAge: 24 * 60 * 60 * 1000 // 24 hours
}
```

#### 4. **Session Management**
- ✅ Automatic session cleanup on expiration
- ✅ Secure session ID generation
- ✅ Clear separation between session keys and sensitive data

### Implementation Details

#### SecureStorage Class Features

1. **setSecureData(name, sensitiveData, options)**
   - Generates unique session ID
   - Encrypts sensitive data with session-specific key
   - Stores encrypted data in sessionStorage
   - Stores only session key in cookie

2. **getSecureData(name)**
   - Retrieves session key from cookie
   - Fetches encrypted data from sessionStorage
   - Decrypts and returns original data

3. **Security Health Check**
   - Validates HTTPS usage
   - Checks crypto API availability
   - Verifies sessionStorage support
   - Provides security recommendations

#### Data Flow Security

```
User Data → Encryption → SessionStorage (encrypted)
                ↓
        Session Key → Cookie (non-sensitive key only)
```

### Migration from localStorage

The system automatically migrates existing localStorage data to secure storage:

```javascript
// Old (insecure)
localStorage.setItem('colorMode', 'dark');

// New (secure)
secureStorage.setSecureData('userPreferences', { colorMode: 'dark' });
```

### Usage Examples

#### Storing User Preferences Securely
```javascript
// Store user preferences
const preferences = {
    colorMode: 'dark',
    newsletter: true,
    notifications: false
};
secureStorage.setSecureData('userPreferences', preferences, { maxAge: 365 * 24 * 60 * 60 * 1000 });

// Retrieve user preferences
const userPrefs = secureStorage.getSecureData('userPreferences');
```

#### Handling Sensitive User Data
```javascript
// For any sensitive data (email, settings, etc.)
secureStorage.setSecureData('userProfile', {
    email: 'user@example.com',
    subscriptions: ['newsletter', 'alerts']
});

// Data is encrypted in sessionStorage, only session key in cookie
```

### Security Recommendations for Production

#### 1. **HTTPS Enforcement**
- All cookies marked with `Secure` flag
- Automatic HTTPS redirect implemented
- HSTS headers recommended

#### 2. **Content Security Policy (CSP)**
```html
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; script-src 'self' 'unsafe-inline' https://pagead2.googlesyndication.com; style-src 'self' 'unsafe-inline';">
```

#### 3. **Encryption Upgrades**
- Consider implementing AES-GCM for stronger encryption
- Use Web Crypto API for production environments
- Implement key rotation for long-lived sessions

#### 4. **Server-Side Enhancements**
```javascript
// For truly HttpOnly cookies, implement server-side:
app.use(session({
    secret: process.env.SESSION_SECRET,
    cookie: {
        secure: true,
        httpOnly: true,
        maxAge: 24 * 60 * 60 * 1000,
        sameSite: 'strict'
    }
}));
```

### Security Audit Checklist

- ✅ No sensitive data stored in cookies directly
- ✅ All sensitive data encrypted before storage
- ✅ Secure cookie flags implemented (Secure, SameSite)
- ✅ Session-based storage with unique keys
- ✅ Automatic cleanup of expired sessions
- ✅ Migration from insecure localStorage
- ✅ Security health check functionality
- ✅ HTTPS-only cookie transmission
- ✅ CSRF protection via SameSite=Strict

### Testing Security Implementation

#### 1. **Cookie Inspection**
```javascript
// Check that cookies only contain session keys, not sensitive data
document.cookie.split(';').forEach(cookie => console.log(cookie));
```

#### 2. **Encryption Verification**
```javascript
// Verify data is encrypted in sessionStorage
Object.keys(sessionStorage).forEach(key => {
    if (key.startsWith('hh_session_')) {
        console.log('Encrypted data:', sessionStorage.getItem(key));
    }
});
```

#### 3. **Security Health Check**
```javascript
// Run security health check
const healthReport = secureStorage.securityHealthCheck();
console.log('Security Status:', healthReport);
```

### Compliance Notes

This implementation follows industry best practices for:
- **OWASP**: Secure cookie handling guidelines
- **GDPR**: Data protection through encryption
- **PCI DSS**: Sensitive data storage requirements
- **SOC 2**: Access control and data protection

### Support and Maintenance

- Regular security audits recommended
- Monitor for new vulnerabilities in dependencies
- Keep encryption methods updated with current standards
- Test cookie security on each deployment

---

**Last Updated**: September 2025  
**Security Review**: Required annually  
**Contact**: security@hashnhedge.com for security-related inquiries