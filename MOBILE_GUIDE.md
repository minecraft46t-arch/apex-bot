# ⚡ APEX REQUIEM - Mobile Pe Bot Kaise Chalayein

## 📱 METHOD 1: TERMUX (Android - FREE, Recommended)

---

### 🔽 STEP 1: Termux Install Karo

> ⚠️ Play Store wala Termux purana hai — F-Droid se lo!

1. **F-Droid** download karo: https://f-droid.org
2. F-Droid mein search karo: **Termux**
3. Install karo (10-20MB)

---

### ⚙️ STEP 2: Termux Mein Commands Chalao

Termux kholo aur yeh ek ek karke likho:

```bash
# 1. Update karo
pkg update -y

# 2. Python install karo
pkg install python -y

# 3. Bot folder banao
mkdir apexbot
cd apexbot

# 4. discord.py install karo
pip install discord.py python-dotenv
```

---

### 📄 STEP 3: Bot Files Create Karo

Termux mein hi files banao:

```bash
# bot.py file banana
nano bot.py
```
> Nano editor khuleg — wahan bot.py ka poora code paste karo
> Paste karne ke liye: **Long Press → Paste**
> Save karne ke liye: **Ctrl+X → Y → Enter**

```bash
# .env file banana
nano .env
```
> Isme likho:
> `DISCORD_TOKEN=tumhara_token_yahan`
> Phir: **Ctrl+X → Y → Enter**

---

### ▶️ STEP 4: Bot Start Karo

```bash
cd ~/apexbot
python bot.py
```

"✅ ApexBot is Online" dikhega — Bot chal raha hai! 🎉

---

### 😴 STEP 5: Phone Band Hone Par Bhi Chalaye Rakhna

```bash
# proot-distro ya screen use karo
pkg install screen -y

# screen session mein bot chalao
screen -S apexbot
python bot.py

# Ab Ctrl+A phir D dabaao — background mein chala jayega!
# Wapas aane ke liye:
screen -r apexbot
```

---

## ☁️ METHOD 2: ONLINE FREE HOSTING (24/7 - Better Option)

### Render.com (FREE)

1. https://render.com pe account banao (GitHub se login karo)
2. GitHub pe apna bot upload karo
3. Render pe "New Web Service" banao
4. Bot automatic 24/7 chalega — **phone band hone par bhi!**

> Bot files GitHub pe daalne ke liye:
> https://github.com pe free account banao

---

## 🔑 Discord Token Kahan Se Milega?

1. https://discord.com/developers/applications kholo
2. "New Application" → Naam: **ApexBot**
3. Left mein "Bot" click karo
4. "Reset Token" → Token copy karo
5. Neeche wale **ON** karo:
   - ✅ SERVER MEMBERS INTENT
   - ✅ MESSAGE CONTENT INTENT

---

## 🤖 Bot Ko Server Mein Add Karo

1. Developer Portal → OAuth2 → URL Generator
2. Scopes: ✅ `bot` + ✅ `applications.commands`
3. Permissions: ✅ Administrator
4. URL copy karo → Browser mein open karo → Server select karo

---

## ❓ Common Problems

| Problem | Solution |
|---------|----------|
| `pip not found` | `pkg install python -y` dobara chalao |
| `Token Invalid` | .env mein token sahi paste kiya? |
| `Bot offline after closing Termux` | `screen` command use karo (Step 5) |
| `Command not syncing` | 1 baar bot restart karo |

---

**⚡ APEX REQUIEM - Dominate the Game!**
