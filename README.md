# SharePoint + Nutrient SDK PoC

A proof-of-concept web application that demonstrates intelligent file checkout from SharePoint libraries with dual-engine document viewing using Nutrient Web SDK and DWS API, featuring automatic engine selection based on file size and comprehensive performance benchmarking.

## 🎯 Overview

This PoC solves the challenge of efficiently viewing documents of varying sizes by automatically selecting the optimal rendering engine:
- **Small files (< 50MB)**: Uses Nutrient Web SDK for fast client-side processing
- **Large files (≥ 50MB)**: Uses Nutrient DWS API for cloud-based processing with better performance
- **Manual override**: Allows forcing either engine for testing purposes

## ✨ Key Features

### 📁 SharePoint Integration
- **File Checkout/Checkin**: Full REST API integration for document lifecycle management
- **Authentication**: Token-based authentication with SharePoint Online/On-premise
- **Mock Mode**: Demonstration mode when credentials aren't available

### 🔧 Dual Engine Architecture
- **Nutrient Web SDK**: Client-side WebAssembly processing for optimal small file performance
- **Nutrient DWS API**: Cloud-based processing for large files with server-side rendering
- **Smart Selection**: Automatic engine choice based on configurable file size threshold (default: 50MB)

### 🎮 Engine Mode Controls
- **Auto Mode**: Intelligent size-based engine selection
- **Force Web SDK**: Override to use client-side processing regardless of file size
- **Force DWS API**: Override to use cloud processing regardless of file size

### 📊 Performance Benchmarking
Real-time performance metrics including:
- File size analysis
- Engine selection tracking
- SharePoint checkout timing
- Document load timing
- Total processing time
- Memory usage monitoring

### 🎨 User Interface
- Clean, responsive design optimized for desktop and mobile
- Configuration panel for credentials and API keys
- Real-time status updates with loading indicators
- Visual performance dashboard
- Error handling with clear messaging

## 🚀 Quick Start

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- SharePoint site access (Online or On-premise)
- Nutrient SDK credentials (trial or licensed)

### Setup
1. **Download the PoC**:
   ```bash
   # Clone or download the HTML file
   curl -O https://path-to-your-file/sharepoint-nutrient-poc.html
   ```

2. **Open in Browser**:
   ```bash
   # Open directly in browser
   open sharepoint-nutrient-poc.html
   # OR serve from local web server
   python -m http.server 8000
   # Then visit: http://localhost:8000/sharepoint-nutrient-poc.html
   ```

3. **Configure Credentials**:
   - **SharePoint Site URL**: Your SharePoint site (e.g., `https://company.sharepoint.com/sites/docs`)
   - **SharePoint Access Token**: Bearer token for API authentication
   - **Nutrient Web SDK Key**: License key for client-side processing
   - **Nutrient DWS API Key**: API key for cloud processing

## 🔧 Configuration Guide

### SharePoint Setup

#### Getting SharePoint Access Token
For SharePoint Online (Office 365):
```javascript
// Register Azure AD app with SharePoint permissions
// Use OAuth 2.0 flow to get access token
// Required permissions: Sites.ReadWrite.All or Files.ReadWrite
```

For SharePoint On-premise:
```javascript
// Use NTLM or Forms authentication
// Generate access token via SharePoint REST API
```

#### SharePoint Site URL Format
```
https://[tenant].sharepoint.com/sites/[sitename]
# Example: https://contoso.sharepoint.com/sites/documents
```

### Nutrient SDK Setup

#### Web SDK License Key
1. Sign up at [Nutrient.io](https://www.nutrient.io)
2. Get trial or purchase license
3. Copy license key from dashboard

#### DWS API Key
1. Access Nutrient DWS dashboard
2. Create new API key
3. Configure permissions for document processing

## 🎯 Usage Instructions

### Basic Workflow
1. **Configure Credentials**: Fill in all required fields in the configuration section
2. **Select File**: Choose document from your local system
3. **Choose Engine Mode**: 
   - Auto (recommended)
   - Force Web SDK
   - Force DWS API
4. **Checkout & View**: Click to start the process
5. **Review Performance**: Check benchmarking metrics
6. **Checkin**: Return file to SharePoint when done

### Supported File Types
- **PDF**: `.pdf`
- **Microsoft Office**: `.docx`, `.xlsx`, `.pptx`
- **Images**: `.png`, `.jpg`, `.jpeg`, `.tiff`

### Engine Selection Logic
```javascript
// Automatic mode decision tree
if (fileSize < 50MB) {
    engine = "Web SDK";  // Client-side processing
} else {
    engine = "DWS API";  // Cloud processing
}
```

## 📈 Benchmarking Features

### Metrics Tracked
- **File Size**: Original document size analysis
- **Engine Used**: Which processing engine was selected
- **Checkout Time**: SharePoint API response time
- **Load Time**: Document rendering duration
- **Total Time**: End-to-end processing time
- **Memory Usage**: JavaScript heap usage (when available)

### Performance Analysis
Use the benchmarking data to:
- Compare Web SDK vs DWS API performance
- Identify optimal file size thresholds
- Monitor SharePoint API responsiveness
- Track memory consumption patterns

## 🏗️ Technical Architecture

### Single-File Design
- **Zero Dependencies**: No build process or external frameworks
- **Self-Contained**: All HTML, CSS, and JavaScript in one file
- **CDN Integration**: Nutrient SDKs loaded via CDN
- **Cross-Browser**: Compatible with all modern browsers

### API Integration Patterns
```javascript
// SharePoint REST API
POST /_api/web/GetFileByServerRelativeUrl('/file')/CheckOut()
POST /_api/web/GetFileByServerRelativeUrl('/file')/CheckIn()

// Nutrient Web SDK
NutrientWebSDK.load({
    container: element,
    document: fileUrl,
    licenseKey: key
});

// Nutrient DWS API
POST /documents (file upload)
POST /viewer-sessions (create session)
```

### Error Handling
- **Graceful Degradation**: Mock mode when APIs unavailable
- **User Feedback**: Clear error messages and status updates
- **Recovery Options**: Reset functionality and retry mechanisms

## 🔍 Mock Mode

When credentials aren't provided, the PoC runs in demonstration mode:
- **SharePoint Operations**: Simulated with delays
- **Nutrient Rendering**: Mock viewers with file information
- **Full UI**: All interface elements remain functional
- **Benchmarking**: Timing data still collected

This allows full evaluation of the interface and workflow without requiring actual service credentials.

## 🔐 Security Considerations

### Credential Storage
- **Client-Side Only**: No server-side credential storage
- **Session-Based**: Credentials cleared on page refresh
- **Input Masking**: Password fields for sensitive data

### Best Practices
- Use least-privilege SharePoint tokens
- Implement token refresh for long sessions
- Consider HTTPS-only deployment for production
- Validate file types before processing

## 🚨 Troubleshooting

### Common Issues

#### SharePoint Authentication Errors
```
Error: SharePoint checkout failed: 401 Unauthorized
```
**Solution**: Verify access token and permissions

#### Nutrient SDK Loading Issues
```
Error: Nutrient Web SDK not loaded
```
**Solution**: Check internet connection and license key

#### CORS Issues
```
Error: Cross-origin request blocked
```
**Solution**: Configure SharePoint CORS settings or use proxy server

#### File Size Errors
```
Error: File too large for Web SDK
```
**Solution**: Use DWS API mode or increase size threshold

### Debug Mode
Press `Escape` key to reset the demo and clear all state.

## 🔄 Customization Options

### File Size Threshold
```javascript
// Modify in the CONFIG object
const CONFIG = {
    FILE_SIZE_THRESHOLD: 50 * 1024 * 1024  // Change to desired size
};
```

### Supported File Types
```javascript
// Update file input accept attribute
accept=".pdf,.docx,.xlsx,.pptx,.png,.jpg,.jpeg,.tiff,.your-type"
```

### UI Styling
All CSS is contained in the `<style>` section and can be modified for branding or layout preferences.

## 📚 API Reference

### SharePoint REST Endpoints
- `GET /_api/web/GetFileByServerRelativeUrl('/file')` - Get file info
- `POST /_api/web/GetFileByServerRelativeUrl('/file')/CheckOut()` - Checkout file
- `POST /_api/web/GetFileByServerRelativeUrl('/file')/CheckIn()` - Checkin file

### Nutrient Web SDK Methods
- `NutrientWebSDK.load(options)` - Initialize viewer
- `instance.destroy()` - Cleanup viewer
- `instance.addEventListener()` - Handle events

### Nutrient DWS API Endpoints
- `POST /documents` - Upload document
- `POST /viewer-sessions` - Create viewer session
- `GET /viewer-sessions/{id}` - Get session info

## 🤝 Contributing

This PoC demonstrates the core concepts and can be extended with:
- **User Management**: Multi-user support with permissions
- **File History**: Version tracking and rollback
- **Collaboration**: Real-time co-editing features
- **Advanced Analytics**: Detailed usage reporting
- **Integration Testing**: Automated test suites

## 📄 License

This proof-of-concept is provided as-is for demonstration purposes. Nutrient SDK usage requires appropriate licensing from Nutrient.io.

## 🆘 Support

For technical support:
- **SharePoint Issues**: Microsoft SharePoint documentation
- **Nutrient SDK**: [Nutrient Support](https://www.nutrient.io/support)
- **PoC Questions**: Check the troubleshooting section above

---

**Built with**: Vanilla JavaScript, HTML5, CSS3  
**Compatible with**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+  
**File Size**: ~25KB (single HTML file)  
**Dependencies**: None (CDN-based SDK loading)