import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from datetime import datetime

# ============================================================
#   APEX REQUIEM - FREE FIRE TOURNAMENT BOT
#   Bot Name: ApexBot ⚡
#   Developer: Setup by APEX REQUIEM Admin
# ============================================================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

DATA_FILE = "data.json"

# ---------- Data Load/Save ----------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {
        "tournaments": {},
        "registrations": {},
        "leaderboard": {},
        "match_results": []
    }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------- Bot Ready ----------
@bot.event
async def on_ready():
    print(f"✅ ApexBot is Online as {bot.user}")
    print(f"🎮 Managing: APEX REQUIEM Free Fire Tournaments")
    try:
        synced = await bot.tree.sync()
        print(f"🔄 Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"❌ Sync Error: {e}")

# ============================================================
#   TOURNAMENT COMMANDS
# ============================================================

@bot.tree.command(name="create_tournament", description="Naya tournament banao")
@app_commands.describe(
    name="Tournament ka naam",
    date="Tournament ki date (DD/MM/YYYY)",
    time="Tournament ka time (HH:MM)",
    prize="Prize pool (e.g. ₹500)",
    max_teams="Maximum teams allowed"
)
@app_commands.checks.has_permissions(administrator=True)
async def create_tournament(interaction: discord.Interaction, name: str, date: str, time: str, prize: str, max_teams: int):
    data = load_data()
    tid = f"T{len(data['tournaments']) + 1}"
    data["tournaments"][tid] = {
        "name": name,
        "date": date,
        "time": time,
        "prize": prize,
        "max_teams": max_teams,
        "registered_teams": 0,
        "status": "OPEN",
        "created_by": str(interaction.user),
        "created_at": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    data["registrations"][tid] = []
    save_data(data)

    embed = discord.Embed(
        title="🏆 New Tournament Created!",
        description=f"**{name}**",
        color=0xFFD700
    )
    embed.add_field(name="🆔 Tournament ID", value=tid, inline=True)
    embed.add_field(name="📅 Date", value=date, inline=True)
    embed.add_field(name="⏰ Time", value=time, inline=True)
    embed.add_field(name="💎 Prize Pool", value=prize, inline=True)
    embed.add_field(name="👥 Max Teams", value=max_teams, inline=True)
    embed.add_field(name="📊 Status", value="✅ OPEN", inline=True)
    embed.set_footer(text="APEX REQUIEM ⚡ | Use /register to join!")
    embed.timestamp = datetime.now()

    await interaction.response.send_message(embed=embed)

# ---------- Register Team ----------
@bot.tree.command(name="register", description="Tournament mein team register karo")
@app_commands.describe(
    tournament_id="Tournament ID (e.g. T1)",
    team_name="Tumhari team ka naam",
    player1="Player 1 Free Fire UID",
    player2="Player 2 Free Fire UID",
    player3="Player 3 Free Fire UID",
    player4="Player 4 Free Fire UID (optional)"
)
async def register(interaction: discord.Interaction, tournament_id: str, team_name: str, player1: str, player2: str, player3: str, player4: str = "N/A"):
    data = load_data()

    if tournament_id not in data["tournaments"]:
        await interaction.response.send_message("❌ Tournament ID galat hai! `/tournaments` se check karo.", ephemeral=True)
        return

    t = data["tournaments"][tournament_id]
    if t["status"] != "OPEN":
        await interaction.response.send_message("❌ Yeh tournament abhi registration ke liye open nahi hai.", ephemeral=True)
        return

    if t["registered_teams"] >= t["max_teams"]:
        await interaction.response.send_message("❌ Tournament full ho gaya hai!", ephemeral=True)
        return

    # Check duplicate
    for reg in data["registrations"][tournament_id]:
        if reg["registered_by"] == str(interaction.user.id):
            await interaction.response.send_message("❌ Tumne pehle se register kar liya hai!", ephemeral=True)
            return

    entry = {
        "team_name": team_name,
        "players": [player1, player2, player3, player4],
        "registered_by": str(interaction.user.id),
        "registered_by_name": str(interaction.user),
        "registered_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "slot": t["registered_teams"] + 1
    }
    data["registrations"][tournament_id].append(entry)
    data["tournaments"][tournament_id]["registered_teams"] += 1
    save_data(data)

    embed = discord.Embed(
        title="✅ Registration Successful!",
        color=0x00FF88
    )
    embed.add_field(name="🏆 Tournament", value=t["name"], inline=False)
    embed.add_field(name="👥 Team Name", value=team_name, inline=True)
    embed.add_field(name="🎰 Slot Number", value=f"#{entry['slot']}", inline=True)
    embed.add_field(name="👤 Players", value=f"1. {player1}\n2. {player2}\n3. {player3}\n4. {player4}", inline=False)
    embed.set_footer(text=f"APEX REQUIEM ⚡ | Registered by {interaction.user}")
    embed.timestamp = datetime.now()

    await interaction.response.send_message(embed=embed)

# ---------- View All Tournaments ----------
@bot.tree.command(name="tournaments", description="Saare tournaments dekho")
async def tournaments(interaction: discord.Interaction):
    data = load_data()

    if not data["tournaments"]:
        await interaction.response.send_message("❌ Abhi koi tournament nahi hai.", ephemeral=True)
        return

    embed = discord.Embed(
        title="🏆 APEX REQUIEM - Active Tournaments",
        color=0xFFD700
    )
    for tid, t in data["tournaments"].items():
        status_emoji = "✅" if t["status"] == "OPEN" else "🔒" if t["status"] == "CLOSED" else "⚔️"
        embed.add_field(
            name=f"{status_emoji} [{tid}] {t['name']}",
            value=f"📅 {t['date']} | ⏰ {t['time']}\n💎 Prize: {t['prize']} | 👥 {t['registered_teams']}/{t['max_teams']} teams",
            inline=False
        )
    embed.set_footer(text="APEX REQUIEM ⚡ | Use /register <ID> to join!")
    await interaction.response.send_message(embed=embed)

# ---------- Add Match Result ----------
@bot.tree.command(name="add_result", description="Match result add karo")
@app_commands.describe(
    tournament_id="Tournament ID",
    rank="Team ka rank (1st, 2nd, etc.)",
    team_name="Team ka naam",
    kills="Total kills",
    points="Total points"
)
@app_commands.checks.has_permissions(manage_messages=True)
async def add_result(interaction: discord.Interaction, tournament_id: str, rank: int, team_name: str, kills: int, points: int):
    data = load_data()

    if tournament_id not in data["tournaments"]:
        await interaction.response.send_message("❌ Tournament ID galat hai!", ephemeral=True)
        return

    result = {
        "tournament_id": tournament_id,
        "tournament_name": data["tournaments"][tournament_id]["name"],
        "rank": rank,
        "team_name": team_name,
        "kills": kills,
        "points": points,
        "added_by": str(interaction.user),
        "added_at": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    data["match_results"].append(result)

    # Update leaderboard
    if team_name not in data["leaderboard"]:
        data["leaderboard"][team_name] = {"total_points": 0, "total_kills": 0, "matches": 0, "wins": 0}
    data["leaderboard"][team_name]["total_points"] += points
    data["leaderboard"][team_name]["total_kills"] += kills
    data["leaderboard"][team_name]["matches"] += 1
    if rank == 1:
        data["leaderboard"][team_name]["wins"] += 1

    save_data(data)

    embed = discord.Embed(
        title="📊 Match Result Added!",
        color=0xFF6600
    )
    medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}"
    embed.add_field(name="🏆 Tournament", value=data["tournaments"][tournament_id]["name"], inline=False)
    embed.add_field(name="🏅 Rank", value=medal, inline=True)
    embed.add_field(name="👥 Team", value=team_name, inline=True)
    embed.add_field(name="🔫 Kills", value=kills, inline=True)
    embed.add_field(name="⭐ Points", value=points, inline=True)
    embed.set_footer(text=f"APEX REQUIEM ⚡ | Added by {interaction.user}")
    embed.timestamp = datetime.now()

    await interaction.response.send_message(embed=embed)

# ---------- Leaderboard ----------
@bot.tree.command(name="leaderboard", description="Overall leaderboard dekho")
async def leaderboard(interaction: discord.Interaction):
    data = load_data()

    if not data["leaderboard"]:
        await interaction.response.send_message("❌ Abhi koi results nahi hain.", ephemeral=True)
        return

    sorted_lb = sorted(data["leaderboard"].items(), key=lambda x: x[1]["total_points"], reverse=True)

    embed = discord.Embed(
        title="🏆 APEX REQUIEM - Overall Leaderboard",
        color=0xFFD700
    )
    medals = ["🥇", "🥈", "🥉"]
    lb_text = ""
    for i, (team, stats) in enumerate(sorted_lb[:10]):
        medal = medals[i] if i < 3 else f"`#{i+1}`"
        lb_text += f"{medal} **{team}** — ⭐{stats['total_points']} pts | 🔫{stats['total_kills']} kills | 🏆{stats['wins']} wins\n"

    embed.description = lb_text
    embed.set_footer(text="APEX REQUIEM ⚡ | Top 10 Teams")
    embed.timestamp = datetime.now()

    await interaction.response.send_message(embed=embed)

# ---------- Match Results List ----------
@bot.tree.command(name="results", description="Kisi tournament ke results dekho")
@app_commands.describe(tournament_id="Tournament ID (e.g. T1)")
async def results(interaction: discord.Interaction, tournament_id: str):
    data = load_data()
    filtered = [r for r in data["match_results"] if r["tournament_id"] == tournament_id]

    if not filtered:
        await interaction.response.send_message("❌ Is tournament ke koi results nahi hain.", ephemeral=True)
        return

    filtered.sort(key=lambda x: x["rank"])
    t_name = data["tournaments"].get(tournament_id, {}).get("name", tournament_id)

    embed = discord.Embed(
        title=f"📊 Results - {t_name}",
        color=0xFF6600
    )
    for r in filtered[:10]:
        medal = "🥇" if r["rank"] == 1 else "🥈" if r["rank"] == 2 else "🥉" if r["rank"] == 3 else f"#{r['rank']}"
        embed.add_field(
            name=f"{medal} {r['team_name']}",
            value=f"⭐ Points: {r['points']} | 🔫 Kills: {r['kills']}",
            inline=False
        )
    embed.set_footer(text="APEX REQUIEM ⚡")
    await interaction.response.send_message(embed=embed)

# ---------- Registrations List ----------
@bot.tree.command(name="registrations", description="Tournament mein registered teams dekho")
@app_commands.describe(tournament_id="Tournament ID (e.g. T1)")
@app_commands.checks.has_permissions(manage_messages=True)
async def registrations(interaction: discord.Interaction, tournament_id: str):
    data = load_data()

    if tournament_id not in data["registrations"]:
        await interaction.response.send_message("❌ Tournament ID galat hai!", ephemeral=True)
        return

    regs = data["registrations"][tournament_id]
    if not regs:
        await interaction.response.send_message("❌ Koi team registered nahi hai abhi.", ephemeral=True)
        return

    t_name = data["tournaments"][tournament_id]["name"]
    embed = discord.Embed(
        title=f"📝 Registrations - {t_name}",
        color=0x00BFFF
    )
    for reg in regs:
        players_str = "\n".join([f"• {p}" for p in reg["players"] if p != "N/A"])
        embed.add_field(
            name=f"Slot #{reg['slot']} | 👥 {reg['team_name']}",
            value=f"{players_str}\n🕐 {reg['registered_at']}",
            inline=False
        )
    embed.set_footer(text=f"APEX REQUIEM ⚡ | Total: {len(regs)} teams")
    await interaction.response.send_message(embed=embed)

# ---------- Close Tournament ----------
@bot.tree.command(name="close_tournament", description="Tournament registration band karo")
@app_commands.describe(tournament_id="Tournament ID")
@app_commands.checks.has_permissions(administrator=True)
async def close_tournament(interaction: discord.Interaction, tournament_id: str):
    data = load_data()
    if tournament_id not in data["tournaments"]:
        await interaction.response.send_message("❌ Tournament ID galat hai!", ephemeral=True)
        return

    data["tournaments"][tournament_id]["status"] = "CLOSED"
    save_data(data)
    t_name = data["tournaments"][tournament_id]["name"]
    await interaction.response.send_message(f"🔒 **{t_name}** tournament band kar diya gaya! Ab koi registration nahi hogi.")

# ---------- Prize Center ----------
@bot.tree.command(name="prize", description="Tournament ka prize info dekho")
@app_commands.describe(tournament_id="Tournament ID")
async def prize(interaction: discord.Interaction, tournament_id: str):
    data = load_data()
    if tournament_id not in data["tournaments"]:
        await interaction.response.send_message("❌ Tournament ID galat hai!", ephemeral=True)
        return

    t = data["tournaments"][tournament_id]
    embed = discord.Embed(
        title="💎 Prize Center",
        description=f"**{t['name']}**",
        color=0x9B59B6
    )
    embed.add_field(name="💎 Total Prize Pool", value=t["prize"], inline=False)
    embed.add_field(name="🥇 1st Place", value="50% of Prize", inline=True)
    embed.add_field(name="🥈 2nd Place", value="30% of Prize", inline=True)
    embed.add_field(name="🥉 3rd Place", value="20% of Prize", inline=True)
    embed.set_footer(text="APEX REQUIEM ⚡ | Prizes distributed after verification")
    await interaction.response.send_message(embed=embed)

# ---------- Room Access ----------
@bot.tree.command(name="room", description="Room ID aur Password share karo (Admin only)")
@app_commands.describe(
    tournament_id="Tournament ID",
    room_id="Free Fire Room ID",
    password="Room Password"
)
@app_commands.checks.has_permissions(administrator=True)
async def room(interaction: discord.Interaction, tournament_id: str, room_id: str, password: str):
    data = load_data()
    if tournament_id not in data["tournaments"]:
        await interaction.response.send_message("❌ Tournament ID galat hai!", ephemeral=True)
        return

    t_name = data["tournaments"][tournament_id]["name"]
    embed = discord.Embed(
        title="🎮 Room Access Details",
        description=f"**{t_name}**",
        color=0xFF0000
    )
    embed.add_field(name="🏠 Room ID", value=f"||{room_id}||", inline=True)
    embed.add_field(name="🔑 Password", value=f"||{password}||", inline=True)
    embed.add_field(name="⚠️ Note", value="Sirf registered players hi join karein!", inline=False)
    embed.set_footer(text="APEX REQUIEM ⚡ | Good Luck!")
    embed.timestamp = datetime.now()

    await interaction.response.send_message(embed=embed)

# ---------- Ping ----------
@bot.tree.command(name="ping", description="Bot ki latency check karo")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    color = 0x00FF00 if latency < 100 else 0xFFFF00 if latency < 200 else 0xFF0000
    embed = discord.Embed(title="🏓 Pong!", description=f"Latency: **{latency}ms**", color=color)
    embed.set_footer(text="APEX REQUIEM ⚡ ApexBot")
    await interaction.response.send_message(embed=embed)

# ---------- Help Command ----------
@bot.tree.command(name="help", description="Saare commands ki list dekho")
async def help_cmd(interaction: discord.Interaction):
    embed = discord.Embed(
        title="⚡ ApexBot - Command List",
        description="APEX REQUIEM Free Fire Tournament Bot",
        color=0xFFD700
    )
    embed.add_field(
        name="🏆 Tournament Commands",
        value="`/create_tournament` - Naya tournament banao\n`/tournaments` - Saare tournaments dekho\n`/close_tournament` - Tournament band karo",
        inline=False
    )
    embed.add_field(
        name="📝 Registration",
        value="`/register` - Tournament mein join karo\n`/registrations` - Registered teams dekho",
        inline=False
    )
    embed.add_field(
        name="📊 Results & Leaderboard",
        value="`/add_result` - Match result add karo\n`/results` - Tournament results dekho\n`/leaderboard` - Overall ranking dekho",
        inline=False
    )
    embed.add_field(
        name="🎮 Match Day",
        value="`/room` - Room ID & Password share karo\n`/prize` - Prize info dekho",
        inline=False
    )
    embed.add_field(
        name="🔧 Utility",
        value="`/ping` - Bot latency check karo\n`/help` - Yeh message",
        inline=False
    )
    embed.set_footer(text="APEX REQUIEM ⚡ | Admin commands ke liye permission chahiye")
    await interaction.response.send_message(embed=embed)

# ---------- Error Handling ----------
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("❌ Tumhare paas yeh command use karne ki permission nahi hai!", ephemeral=True)
    else:
        await interaction.response.send_message(f"❌ Error aaya: {str(error)}", ephemeral=True)

# ============================================================
#   RUN BOT
# ============================================================
if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    if not TOKEN:
        print("❌ Error: DISCORD_TOKEN environment variable set nahi hai!")
        print("👉 .env file mein apna token daalo ya TOKEN variable mein seedha paste karo")
        exit(1)
    bot.run(TOKEN)
