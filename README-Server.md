# 🚀 Running the SharePoint + Nutrient PoC with Local Server

## Quick Start

Run this command to start the local server and fix CORS issues:

```bash
python3 server.py
```

The server will:
- ✅ **Fix CORS errors** with Nutrient DWS API
- ✅ **Enable proper license validation** (no more `file://` errors)
- ✅ **Proxy API calls** to avoid browser security restrictions
- ✅ **Auto-open your browser** to the PoC

## What This Fixes

### Before (File Protocol Issues):
```
❌ CORS policy: No 'Access-Control-Allow-Origin' header
❌ Invalid license key for 'file://'
❌ Direct API calls blocked by browser
❌ Mock interfaces only
```

### After (HTTP Server):
```
✅ CORS headers properly configured
✅ License keys work with http://localhost
✅ Real Nutrient DWS API calls via proxy
✅ Full functionality enabled
```

## Server Features

### CORS Proxy
- **Endpoint**: `/api/nutrient/*` → `https://api.nutrient.io/*`
- **Headers**: Forwards Authorization and other headers
- **Methods**: Supports POST requests for file uploads
- **Response**: Streams Nutrient API responses back to client

### Auto-Configuration
- **Port**: 8000 (auto-detects conflicts)
- **Directory**: Serves files from current directory
- **Browser**: Auto-opens the PoC in your default browser
- **Status**: Shows detailed startup information

## Usage Instructions

### 1. Start Server
```bash
cd /Users/matthew/Documents/Repos/ClaudeCode
python3 server.py
```

### 2. Expected Output
```
🚀 Starting server at http://localhost:8000
📁 Serving files from: /Users/matthew/Documents/Repos/ClaudeCode
🌐 PoC URL: http://localhost:8000/sharepoint-nutrient-poc.html

✅ Benefits of using the server:
   • Fixes CORS issues with Nutrient DWS API
   • Enables proper license key validation
   • Allows real API calls instead of mocks
   • Better file handling and security

🌐 Opened sharepoint-nutrient-poc.html in your default browser
🔧 Server running on port 8000...
```

### 3. Test the PoC
- **Small files**: Will use Nutrient Web SDK (< 50MB)
- **Large files**: Will use Nutrient DWS API (≥ 50MB)
- **Real authentication**: Your license keys will work properly
- **Full functionality**: No more mock interfaces

### 4. Stop Server
Press `Ctrl+C` to stop the server when done.

## Troubleshooting

### Port Already in Use
```bash
❌ Port 8000 is already in use
```
**Solution**: Stop other servers or modify PORT in server.py

### Missing Dependencies
```bash
❌ requests library not available
```
**Solution**: Install requests library
```bash
pip3 install requests
```

### License Key Issues
If you still get license errors, ensure:
- Using the correct Web SDK license key (not DWS API key)
- Accessing via `http://localhost:8000` not `file://`
- License key is properly formatted

## Alternative: Simple HTTP Server

If you don't need DWS API proxy, use Python's built-in server:

```bash
python3 -m http.server 8000
```

Then visit: `http://localhost:8000/sharepoint-nutrient-poc.html`

**Note**: This won't fix DWS CORS issues, but will enable Web SDK license validation.

## Production Deployment

For production, implement similar CORS proxy functionality in your backend:

### Node.js Example
```javascript
app.post('/api/nutrient/*', async (req, res) => {
  const nutrientUrl = `https://api.nutrient.io${req.path.replace('/api/nutrient', '')}`;
  const response = await fetch(nutrientUrl, {
    method: 'POST',
    headers: { 'Authorization': req.headers.authorization },
    body: req.body
  });
  res.json(await response.json());
});
```

### Benefits of Server Approach
- **Security**: API keys stay on server-side
- **Performance**: Better file handling and caching
- **Reliability**: Proper error handling and retries
- **Scalability**: Can handle multiple concurrent users

---

**Ready to test the full PoC functionality!** 🎉