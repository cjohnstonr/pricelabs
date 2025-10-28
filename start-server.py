#!/usr/bin/env python3

import http.server
import socketserver
import socket
import os
import sys
import glob
from pathlib import Path

PORT = 8089

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

def get_local_ip():
    """Get the local IP address for network access"""
    try:
        # Create a socket to determine the local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return None

def find_html_files():
    """Find all HTML files in the current directory and subdirectories"""
    html_files = []
    for pattern in ['*.html', '**/*.html']:
        html_files.extend(glob.glob(pattern, recursive=True))
    return sorted(set(html_files))

def main():
    # Change to the directory containing this script
    os.chdir(os.path.dirname(os.path.abspath(__file__)) or '.')
    
    print('\n🌐 Local server is running!\n')
    print(f'📱 Access from this computer: http://localhost:{PORT}')
    
    local_ip = get_local_ip()
    if local_ip:
        print('📱 Access from other devices on the same network:')
        print(f'   http://{local_ip}:{PORT}')
    
    html_files = find_html_files()
    if html_files:
        print('\n📁 Your HTML files:')
        for file in html_files[:10]:  # Show first 10 files
            print(f'   http://localhost:{PORT}/{file}')
        if len(html_files) > 10:
            print(f'   ... and {len(html_files) - 10} more files')
    
    print('\n⚡ Press Ctrl+C to stop the server\n')
    
    try:
        with socketserver.TCPServer(("", PORT), CORSHTTPRequestHandler) as httpd:
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f'❌ Port {PORT} is already in use. Please close other servers or use a different port.')
        else:
            print(f'❌ Server error: {e}')
        sys.exit(1)
    except KeyboardInterrupt:
        print('\n\n👋 Server stopped gracefully')
        sys.exit(0)

if __name__ == "__main__":
    main()