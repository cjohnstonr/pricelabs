#!/bin/bash

# Start local development server
echo "🚀 Starting local development server..."

# Check if Node.js is available
if command -v node &> /dev/null; then
    echo "📦 Using Node.js server..."
    node server.js
elif command -v python3 &> /dev/null; then
    echo "🐍 Node.js not found, using Python server..."
    python3 start-server.py
else
    echo "❌ Error: Neither Node.js nor Python 3 is installed."
    echo "Please install Node.js (https://nodejs.org) or Python 3 to run the server."
    exit 1
fi