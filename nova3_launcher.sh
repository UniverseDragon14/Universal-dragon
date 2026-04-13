#!/bin/bash
# NOVA3 Universal Dragon OS Launcher

NOVA_DIR="$HOME/universal_dragon/nova3"
cd "$NOVA_DIR"

# Check if venv exists, if not create it
if [ ! -d "venv" ]; then
    echo "🐉 Setting up NOVA3 for first time..."
    python3 -m venv venv
    source venv/bin/activate
    pip install requests python-dotenv -q
else
    source venv/bin/activate
fi

# Check Ollama status
if ! systemctl is-active --quiet ollama; then
    echo "🔄 Starting Ollama service..."
    sudo systemctl start ollama
    sleep 2
fi

# Launch Dragon Terminal
clear
echo "⚡ UNIVERSAL DRAGON OS - Initializing..."
python dragon_terminal.py
