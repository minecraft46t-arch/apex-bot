#!/bin/bash
# ============================================================
#   APEX REQUIEM - ApexBot Setup Script for Termux
#   Yeh script automatically sab kuch install kar dega
# ============================================================

echo "╔════════════════════════════════════════╗"
echo "║   ⚡ APEX REQUIEM - ApexBot Setup ⚡   ║"
echo "╚════════════════════════════════════════╝"
echo ""

echo "📦 Step 1: Termux packages update ho rahe hain..."
pkg update -y && pkg upgrade -y

echo ""
echo "🐍 Step 2: Python install ho raha hai..."
pkg install python -y

echo ""
echo "📁 Step 3: Bot folder ban raha hai..."
mkdir -p ~/apexbot
cd ~/apexbot

echo ""
echo "📥 Step 4: discord.py install ho rahi hai..."
pip install discord.py python-dotenv

echo ""
echo "✅ Setup complete! Ab bot.py aur .env file daalo"
echo ""
echo "▶️  Bot start karne ke liye:"
echo "    cd ~/apexbot && python bot.py"
echo ""
echo "⚡ APEX REQUIEM - Ready to Fight!"
