const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');
const os = require('os');

const PORT = 8089;
const HOST = '0.0.0.0';

// MIME types
const MIME_TYPES = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon'
};

// Get network interfaces
function getNetworkAddresses() {
    const interfaces = os.networkInterfaces();
    const addresses = [];
    
    for (const name of Object.keys(interfaces)) {
        for (const interface of interfaces[name]) {
            if (interface.family === 'IPv4' && !interface.internal) {
                addresses.push(interface.address);
            }
        }
    }
    
    return addresses;
}

// Get all HTML files in directory
function getHtmlFiles(dir, baseDir = dir) {
    const files = [];
    
    try {
        const items = fs.readdirSync(dir);
        
        for (const item of items) {
            const fullPath = path.join(dir, item);
            const stat = fs.statSync(fullPath);
            
            if (stat.isDirectory() && !item.startsWith('.')) {
                files.push(...getHtmlFiles(fullPath, baseDir));
            } else if (item.endsWith('.html')) {
                const relativePath = path.relative(baseDir, fullPath);
                files.push(relativePath);
            }
        }
    } catch (error) {
        console.error('Error reading directory:', error);
    }
    
    return files;
}

// Create directory listing HTML
function createDirectoryListing(dirPath, requestPath) {
    const items = fs.readdirSync(dirPath);
    const directories = [];
    const files = [];
    
    // Separate directories and files
    items.forEach(item => {
        if (item.startsWith('.')) return;
        
        const itemPath = path.join(dirPath, item);
        const stat = fs.statSync(itemPath);
        
        if (stat.isDirectory()) {
            directories.push(item);
        } else {
            files.push(item);
        }
    });
    
    // Sort alphabetically
    directories.sort();
    files.sort();
    
    let html = `
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Directory listing for ${requestPath}</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            padding: 20px;
        }
        h1 {
            color: #333;
            margin: 0 0 20px 0;
            padding-bottom: 10px;
            border-bottom: 2px solid #eee;
        }
        .item {
            display: flex;
            align-items: center;
            padding: 10px;
            text-decoration: none;
            color: #333;
            border-radius: 4px;
            transition: background 0.2s;
        }
        .item:hover {
            background: #f0f0f0;
        }
        .icon {
            width: 24px;
            margin-right: 10px;
            text-align: center;
        }
        .directory {
            color: #0066cc;
            font-weight: 500;
        }
        .file {
            color: #555;
        }
        .back-link {
            margin-bottom: 20px;
            display: inline-block;
            color: #0066cc;
            text-decoration: none;
        }
        .back-link:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📁 Directory listing for ${requestPath}</h1>
`;
    
    // Add parent directory link if not at root
    if (requestPath !== '/') {
        const parentPath = path.dirname(requestPath);
        html += `<a href="${parentPath}" class="back-link">⬆️ Parent directory</a>`;
    }
    
    // Add directories
    directories.forEach(dir => {
        const dirUrl = path.join(requestPath, dir);
        html += `
        <a href="${dirUrl}/" class="item directory">
            <span class="icon">📁</span>
            <span>${dir}/</span>
        </a>`;
    });
    
    // Add files
    files.forEach(file => {
        const fileUrl = path.join(requestPath, file);
        const ext = path.extname(file).toLowerCase();
        let icon = '📄';
        
        if (['.html', '.htm'].includes(ext)) icon = '🌐';
        else if (['.css'].includes(ext)) icon = '🎨';
        else if (['.js', '.json'].includes(ext)) icon = '📜';
        else if (['.png', '.jpg', '.jpeg', '.gif', '.svg'].includes(ext)) icon = '🖼️';
        
        html += `
        <a href="${fileUrl}" class="item file">
            <span class="icon">${icon}</span>
            <span>${file}</span>
        </a>`;
    });
    
    html += `
    </div>
</body>
</html>`;
    
    return html;
}

// Create server
const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url);
    let pathname = decodeURIComponent(parsedUrl.pathname);
    
    // Security: prevent directory traversal
    if (pathname.includes('..')) {
        res.writeHead(403, { 'Content-Type': 'text/plain' });
        res.end('403 Forbidden');
        return;
    }
    
    // Remove leading slash and default to current directory
    let filePath = pathname.slice(1) || '.';
    
    // Check if path exists
    if (!fs.existsSync(filePath)) {
        res.writeHead(404, { 'Content-Type': 'text/html' });
        res.end(`
            <html>
                <body style="font-family: sans-serif; text-align: center; padding: 50px;">
                    <h1>404 Not Found</h1>
                    <p>The requested file was not found.</p>
                    <a href="/">Go to home</a>
                </body>
            </html>
        `);
        return;
    }
    
    const stat = fs.statSync(filePath);
    
    // Handle directories
    if (stat.isDirectory()) {
        // Check for index.html
        const indexPath = path.join(filePath, 'index.html');
        if (fs.existsSync(indexPath)) {
            filePath = indexPath;
        } else {
            // Show directory listing
            try {
                const html = createDirectoryListing(filePath, pathname);
                res.writeHead(200, { 'Content-Type': 'text/html' });
                res.end(html);
                return;
            } catch (error) {
                res.writeHead(500, { 'Content-Type': 'text/plain' });
                res.end('500 Internal Server Error');
                return;
            }
        }
    }
    
    // Serve file
    const ext = path.extname(filePath).toLowerCase();
    const mimeType = MIME_TYPES[ext] || 'application/octet-stream';
    
    fs.readFile(filePath, (err, content) => {
        if (err) {
            res.writeHead(500, { 'Content-Type': 'text/plain' });
            res.end('500 Internal Server Error');
            return;
        }
        
        res.writeHead(200, { 
            'Content-Type': mimeType,
            'Cache-Control': 'no-cache'
        });
        res.end(content);
    });
});

// Start server
server.listen(PORT, HOST, () => {
    console.log('\n🌐 Local server is running!\n');
    console.log(`📱 Access from this computer: http://localhost:${PORT}`);
    
    const addresses = getNetworkAddresses();
    if (addresses.length > 0) {
        console.log('📱 Access from other devices on the same network:');
        addresses.forEach(address => {
            console.log(`   http://${address}:${PORT}`);
        });
    }
    
    const htmlFiles = getHtmlFiles('.');
    if (htmlFiles.length > 0) {
        console.log('\n📁 Your HTML files:');
        htmlFiles.forEach(file => {
            console.log(`   http://localhost:${PORT}/${file}`);
        });
    }
    
    console.log('\n⚡ Press Ctrl+C to stop the server\n');
});

// Handle server errors
server.on('error', (err) => {
    if (err.code === 'EADDRINUSE') {
        console.error(`❌ Port ${PORT} is already in use. Please close other servers or use a different port.`);
    } else {
        console.error('❌ Server error:', err);
    }
    process.exit(1);
});

// Graceful shutdown
process.on('SIGINT', () => {
    console.log('\n\n👋 Server stopped gracefully');
    process.exit(0);
});