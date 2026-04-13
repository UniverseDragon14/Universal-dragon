#!/bin/bash
cd "$HOME/universal_dragon/nova3" || exit 1
source venv/bin/activate

while true; do
    clear
    echo "⚡ NOVA3 GUARD MODE"
    echo "If terminal crashes, auto restart in 2 sec..."
    python dragon_terminal.py
    code=$?

    if [ "$code" -eq 0 ]; then
        echo "✅ NOVA3 exited cleanly"
        break
    fi

    echo "⚠️ NOVA3 crashed with code $code"
    echo "🔁 Restarting..."
    sleep 2
done
