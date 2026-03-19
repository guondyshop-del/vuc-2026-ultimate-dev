# Google OAuth 2.0 Configuration Guide for VUC-2026

## 🚨 PROBLEM IDENTIFIED
The redirect URI mismatch error occurs because Google Cloud Console has `http://localhost:8080` registered, but your app runs on port 8002.

## 🔧 SOLUTION STEPS

### Step 1: Update Google Cloud Console
1. Go to: https://console.cloud.google.com/
2. Select project: `karacocuk`
3. Navigate to: APIs & Services → Credentials
4. Find your OAuth 2.0 Client ID: `[YOUR_CLIENT_ID]`
5. Click to edit the client ID
6. In "Authorized redirect URIs", add these URIs:
   - `http://127.0.0.1:8002/auth/callback`
   - `http://localhost:8002/auth/callback`
   - `http://127.0.0.1:8002/oauth/callback`
   - `http://localhost:8002/oauth/callback`
7. Remove or update any incorrect URIs (like `http://localhost:8080`)
8. Save the changes

### Step 2: Verify Environment Variables
Your `.env` file should contain:

```env
GOOGLE_CLIENT_ID=[YOUR_CLIENT_ID]
GOOGLE_CLIENT_SECRET=[YOUR_CLIENT_SECRET]
GOOGLE_REDIRECT_URI=http://127.0.0.1:8002/auth/callback
```

### Step 3: Test the OAuth Flow
1. Start your backend server: `python backend/vuc2026_complete.py`
2. Visit: `http://127.0.0.1:8002/auth/login`
3. You should be redirected to Google's OAuth consent screen
4. After authorization, you'll be redirected back to: `http://127.0.0.1:8002/auth/callback`

## 🛡️ TROUBLESHOOTING

### Common Issues
- **Redirect URI mismatch**: Ensure the URI in Google Console matches your app
- **Client ID/Secret invalid**: Double-check your credentials
- **Scope insufficient**: Make sure required scopes are authorized

### Debug Tips
- Check browser console for JavaScript errors
- Monitor backend logs for OAuth flow details
- Verify environment variables are loaded correctly

## 📝 NOTES
- Keep your client secret secure and never commit it to version control
- Use environment variables for all sensitive configuration
- Test OAuth flow in both development and production environments
