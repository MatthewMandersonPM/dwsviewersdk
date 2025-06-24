#!/usr/bin/env python3
"""
Simple HTTP server to serve the SharePoint + Nutrient PoC
Fixes CORS and file:// protocol issues
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from urllib.parse import urlparse, parse_qs
import json

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()

    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        # Simple proxy for Nutrient DWS API calls
        if self.path.startswith('/api/nutrient/'):
            try:
                import requests
                
                # Extract the actual API path
                api_path = self.path.replace('/api/nutrient/', '')
                nutrient_url = f'https://api.nutrient.io/{api_path}'
                
                # Get the authorization header
                auth_header = self.headers.get('Authorization')
                
                # Read the request body
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                
                # Forward the request to Nutrient API
                headers = {}
                if auth_header:
                    headers['Authorization'] = auth_header
                
                response = requests.post(
                    nutrient_url,
                    data=post_data,
                    headers=headers,
                    timeout=30
                )
                
                # Send response back
                self.send_response(response.status_code)
                self.send_header('Content-Type', response.headers.get('Content-Type', 'application/json'))
                self.end_headers()
                self.wfile.write(response.content)
                return
                
            except ImportError:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b'{"error": "requests library not available"}')
                return
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f'{{"error": "{str(e)}"}}'.encode())
                return
        
        # Default POST handling
        super().do_POST()

def main():
    PORT = 8000
    
    # Change to the directory containing the HTML file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Check if the HTML file exists
    html_file = 'sharepoint-nutrient-poc.html'
    if not os.path.exists(html_file):
        print(f"Error: {html_file} not found in {script_dir}")
        sys.exit(1)
    
    try:
        with socketserver.TCPServer(("", PORT), CORSHTTPRequestHandler) as httpd:
            print(f"🚀 Starting server at http://localhost:{PORT}")
            print(f"📁 Serving files from: {script_dir}")
            print(f"🌐 PoC URL: http://localhost:{PORT}/{html_file}")
            print("\n✅ Benefits of using the server:")
            print("   • Fixes CORS issues with Nutrient DWS API")
            print("   • Enables proper license key validation")
            print("   • Allows real API calls instead of mocks")
            print("   • Better file handling and security")
            print("\n📋 Instructions:")
            print("   1. The PoC will open automatically in your browser")
            print("   2. Use your real Nutrient license keys")
            print("   3. Test both Web SDK and DWS functionality")
            print("   4. Press Ctrl+C to stop the server")
            
            # Try to open the browser automatically
            try:
                webbrowser.open(f'http://localhost:{PORT}/{html_file}')
                print(f"\n🌐 Opened {html_file} in your default browser")
            except:
                print(f"\n⚠️  Could not auto-open browser. Please visit: http://localhost:{PORT}/{html_file}")
            
            print(f"\n🔧 Server running on port {PORT}...")
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Port {PORT} is already in use. Try a different port or stop the existing server.")
        else:
            print(f"❌ Server error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()