# Google OAuth Setup

The application implements a real Google OAuth 2.0 authorization-code flow. No client IDs, client secrets, tokens, or credentials are stored in this repository. Google sign-in is disabled until every required server-side value is configured.

## 1. Create the Google Cloud credentials

1. In Google Cloud Console, select or create the project used for this deployment.
2. Configure the OAuth consent screen. Use the production brand/domain, add the required scopes (`openid`, `email`, `profile`), and add test users while the app is in testing.
3. Create credentials → **OAuth client ID** → **Web application**.
4. Add the exact frontend origin under **Authorized JavaScript origins**, for example `https://prep.example.com`.
5. Add the exact backend callback under **Authorized redirect URIs**, for example `https://api.example.com/api/auth/google/callback`. The path must be `/api/auth/google/callback`; query strings and wildcards are not accepted.

## 2. Configure server-side environment variables

Set these only in the backend deployment secret manager or process environment. Never put the client secret in frontend code, a committed file, or an API response.

```text
GOOGLE_CLIENT_ID=<OAuth client ID from Google Cloud Console>
GOOGLE_CLIENT_SECRET=<OAuth client secret from Google Cloud Console>
GOOGLE_REDIRECT_URI=https://api.example.com/api/auth/google/callback
GOOGLE_SUCCESS_REDIRECT_URL=https://prep.example.com/auth/google/complete
GOOGLE_COOKIE_SECURE=true
GOOGLE_COOKIE_SAMESITE=none
```

Requirements:

- All three of `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, and `GOOGLE_REDIRECT_URI` must be set together; partial configuration is rejected in production.
- `GOOGLE_REDIRECT_URI` must be an exact HTTPS URL with no query or fragment and must match Google Cloud Console character-for-character.
- `GOOGLE_SUCCESS_REDIRECT_URL` must be an exact HTTPS frontend URL pointing to the SPA callback page.
- Cross-origin production deployments require `GOOGLE_COOKIE_SECURE=true` and `GOOGLE_COOKIE_SAMESITE=none`.
- The frontend origin must also be listed exactly in `CORS_ORIGINS`.

## 3. How the flow works

1. The frontend calls `GET /api/auth/google/start`.
2. The backend creates single-use state, nonce, and PKCE verifier rows, sets an HttpOnly SameSite OAuth cookie bound to that browser, and returns only the Google authorization URL.
3. Google redirects to `GET /api/auth/google/callback?code=...&state=...`.
4. The backend validates the state and cookie, consumes the state once, exchanges the code with its server-side client secret and PKCE verifier, fetches Google's JWKS, and verifies the ID token's signature, issuer, audience, expiry, nonce, verified-email claim, and stable `sub`.
5. The backend redirects to the SPA with a short-lived opaque exchange code. No access token, ID token, email, or client secret is placed in the URL.
6. The SPA callback page posts the opaque code to `POST /api/auth/google/exchange` with browser credentials. The backend consumes the code once, checks the browser binding again, issues the normal revocable session token, and clears the OAuth cookie.

Identity behavior:

- A new verified Google `sub` with no matching account creates a no-password account.
- A returning linked `sub` signs in to the same user ID.
- A verified Google email matching an existing email/password account links the Google identity to that account; no duplicate user or ID change occurs.
- Unverified emails, disabled accounts, replayed state/codes, mismatched cookies, invalid nonces, and invalid issuer/audience/signature are rejected.

## 4. Verification before enabling for users

1. Restart the API with the configuration above and confirm `GET /api/auth/google/start` returns an authorization URL.
2. Complete sign-in with an authorized test user in a clean browser session.
3. Confirm the final URL contains only the opaque `code`, not tokens or email addresses.
4. Confirm `/api/auth/me` succeeds with the issued session and that the returned user has the expected ID and `has_password`.
5. Replay the callback and exchange code; both must fail.
6. Test that an existing email/password account is linked rather than duplicated.
7. Confirm logout revokes the session.

If any required value is missing, the frontend shows a safe configuration error and Google sign-in remains unavailable. This is expected; do not claim Google sign-in is operational until the end-to-end verification above succeeds.

## 5. Password recovery

Google verified-email sign-in is an alternative when no email provider is configured. With `EMAIL_PROVIDER=none`, password setup requests explicitly report that email delivery is not configured. To enable recovery links, configure SMTP server-side and set `PASSWORD_RESET_URL` to the exact HTTPS frontend reset route. Reset tokens remain hashed, single-use, and short-lived.
