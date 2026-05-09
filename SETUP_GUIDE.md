# ⚡ APEX REQUIEM - ApexBot Setup Guide

## Bot ka Naam: ApexBot
## Kaam: Free Fire Tournament Management

---

## 📦 STEP 1: Required Files
Yeh 3 files ek folder mein rakh lo:
- `bot.py` ← Main bot code
- `requirements.txt` ← Dependencies
- `.env` ← Token file

---

## 🔧 STEP 2: Python Install karo
https://python.org se Python 3.10+ download karo

---

## 🤖 STEP 3: Discord Bot Banao

1. https://discord.com/developers/applications kholo
2. "New Application" click karo → Naam: **ApexBot**
3. Left mein "Bot" click karo
4. "Add Bot" → "Yes, do it!"
5. "Reset Token" click karo → Token copy kar lo
6. Neeche wale ON karo:
   - ✅ SERVER MEMBERS INTENT
   - ✅ MESSAGE CONTENT INTENT

---

## 🔑 STEP 4: Token .env mein daalo

`.env` file kholo aur yahan paste karo:
```
DISCORD_TOKEN=tumhara_copied_token_yahan
```

---

## 📨 STEP 5: Bot ko Server mein Add karo

1. Discord Developer Portal > OAuth2 > URL Generator
2. Scopes mein: ✅ `bot` + ✅ `applications.commands`
3. Bot Permissions mein:
   - ✅ Administrator (ya manually: Send Messages, Embed Links, Read Messages)
4. Generated URL copy karo → Browser mein kholo → Server select karo

---

## ▶️ STEP 6: Bot Run karo

Terminal/CMD mein yeh commands chalao:

```bash
# Folder mein jao
cd apex_bot

# Dependencies install karo (sirf pehli baar)
pip install -r requirements.txt

# Bot start karo
python bot.py
```

"✅ ApexBot is Online" dikhe toh bot chal raha hai!

---

## 🎮 COMMANDS LIST

| Command | Kaam | Permission |
|---------|------|-----------|
| `/create_tournament` | Naya tournament banao | Admin |
| `/tournaments` | Saare tournaments dekho | Sab |
| `/close_tournament` | Registration band karo | Admin |
| `/register` | Tournament join karo | Sab |
| `/registrations` | Teams list dekho | Mod+ |
| `/add_result` | Match result daalo | Mod+ |
| `/results` | Tournament results dekho | Sab |
| `/leaderboard` | Overall ranking | Sab |
| `/room` | Room ID/Pass share karo | Admin |
| `/prize` | Prize info dekho | Sab |
| `/ping` | Bot check | Sab |
| `/help` | Commands list | Sab |

---

## 📊 DATA STORAGE
Bot automatic `data.json` file banata hai — isme saara data save hota hai.
Yeh file delete mat karna! Tournament data wahan hota hai.

---

## ❓ Problem aaye toh:
- Python version: `python --version` (3.10+ hona chahiye)
- Token sahi hai? `.env` file check karo
- Bot server mein hai? Step 5 dobara karo

**APEX REQUIEM ⚡ - Good Luck bhai!**
