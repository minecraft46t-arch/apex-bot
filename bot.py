import os
import json
import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)
DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"tournaments": {}, "registrations": {}, "leaderboard": {}, "match_results": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@bot.event
async def on_ready():
    print(f"ApexBot Online: {bot.user}")
    await bot.tree.sync()
    print("Commands synced!")

@bot.tree.command(name="create_tournament", description="Naya tournament banao")
@app_commands.describe(name="Tournament naam", date="Date DD/MM/YYYY", time="Time HH:MM", prize="Prize pool", max_teams="Max teams")
@app_commands.checks.has_permissions(administrator=True)
async def create_tournament(interaction: discord.Interaction, name: str, date: str, time: str, prize: str, max_teams: int):
    data = load_data()
    tid = f"T{len(data['tournaments']) + 1}"
    data["tournaments"][tid] = {"name": name, "date": date, "time": time, "prize": prize, "max_teams": max_teams, "registered_teams": 0, "status": "OPEN"}
    data["registrations"][tid] = []
    save_data(data)
    embed = discord.Embed(title="New Tournament!", description=f"**{name}**", color=0xFFD700)
    embed.add_field(name="ID", value=tid, inline=True)
    embed.add_field(name="Date", value=date, inline=True)
    embed.add_field(name="Prize", value=prize, inline=True)
    embed.add_field(name="Max Teams", value=max_teams, inline=True)
    embed.set_footer(text="APEX REQUIEM | /register se join karo!")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="register", description="Tournament join karo")
@app_commands.describe(tournament_id="Tournament ID", team_name="Team naam", player1="Player 1 UID", player2="Player 2 UID", player3="Player 3 UID", player4="Player 4 UID")
async def register(interaction: discord.Interaction, tournament_id: str, team_name: str, player1: str, player2: str, player3: str, player4: str = "N/A"):
    data = load_data()
    if tournament_id not in data["tournaments"]:
        await interaction.response.send_message("Tournament ID galat hai!", ephemeral=True); return
    t = data["tournaments"][tournament_id]
    if t["status"] != "OPEN":
        await interaction.response.send_message("Registration band hai!", ephemeral=True); return
    if t["registered_teams"] >= t["max_teams"]:
        await interaction.response.send_message("Tournament full hai!", ephemeral=True); return
    for r in data["registrations"][tournament_id]:
        if r["uid"] == str(interaction.user.id):
            await interaction.response.send_message("Pehle se register ho!", ephemeral=True); return
    slot = t["registered_teams"] + 1
    data["registrations"][tournament_id].append({"team_name": team_name, "players": [player1, player2, player3, player4], "uid": str(interaction.user.id), "slot": slot})
    data["tournaments"][tournament_id]["registered_teams"] += 1
    save_data(data)
    embed = discord.Embed(title="Registration Ho Gaya!", color=0x00FF88)
    embed.add_field(name="Tournament", value=t["name"], inline=True)
    embed.add_field(name="Team", value=team_name, inline=True)
    embed.add_field(name="Slot", value=f"#{slot}", inline=True)
    embed.add_field(name="Players", value=f"1.{player1}\n2.{player2}\n3.{player3}\n4.{player4}", inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="tournaments", description="Saare tournaments dekho")
async def tournaments(interaction: discord.Interaction):
    data = load_data()
    if not data["tournaments"]:
        await interaction.response.send_message("Koi tournament nahi hai!", ephemeral=True); return
    embed = discord.Embed(title="APEX REQUIEM Tournaments", color=0xFFD700)
    for tid, t in data["tournaments"].items():
        emoji = "✅" if t["status"] == "OPEN" else "🔒"
        embed.add_field(name=f"{emoji} [{tid}] {t['name']}", value=f"📅{t['date']} ⏰{t['time']}\n💎{t['prize']} | 👥{t['registered_teams']}/{t['max_teams']}", inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="registrations", description="Registered teams dekho")
@app_commands.checks.has_permissions(manage_messages=True)
async def registrations(interaction: discord.Interaction, tournament_id: str):
    data = load_data()
    if tournament_id not in data["registrations"] or not data["registrations"][tournament_id]:
        await interaction.response.send_message("Koi registration nahi!", ephemeral=True); return
    embed = discord.Embed(title=f"Registrations - {data['tournaments'][tournament_id]['name']}", color=0x00BFFF)
    for r in data["registrations"][tournament_id]:
        embed.add_field(name=f"Slot #{r['slot']} | {r['team_name']}", value="\n".join([f"• {p}" for p in r["players"] if p != "N/A"]), inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="add_result", description="Match result add karo")
@app_commands.checks.has_permissions(manage_messages=True)
async def add_result(interaction: discord.Interaction, tournament_id: str, rank: int, team_name: str, kills: int, points: int):
    data = load_data()
    if tournament_id not in data["tournaments"]:
        await interaction.response.send_message("Tournament ID galat!", ephemeral=True); return
    data["match_results"].append({"tournament_id": tournament_id, "rank": rank, "team_name": team_name, "kills": kills, "points": points})
    lb = data["leaderboard"]
    if team_name not in lb:
        lb[team_name] = {"total_points": 0, "total_kills": 0, "matches": 0, "wins": 0}
    lb[team_name]["total_points"] += points
    lb[team_name]["total_kills"] += kills
    lb[team_name]["matches"] += 1
    if rank == 1: lb[team_name]["wins"] += 1
    save_data(data)
    medal = "🥇" if rank==1 else "🥈" if rank==2 else "🥉" if rank==3 else f"#{rank}"
    embed = discord.Embed(title="Result Add Ho Gaya!", color=0xFF6600)
    embed.add_field(name="Rank", value=medal, inline=True)
    embed.add_field(name="Team", value=team_name, inline=True)
    embed.add_field(name="Kills", value=kills, inline=True)
    embed.add_field(name="Points", value=points, inline=True)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="leaderboard", description="Leaderboard dekho")
async def leaderboard(interaction: discord.Interaction):
    data = load_data()
    if not data["leaderboard"]:
        await interaction.response.send_message("Koi data nahi!", ephemeral=True); return
    sorted_lb = sorted(data["leaderboard"].items(), key=lambda x: x[1]["total_points"], reverse=True)
    embed = discord.Embed(title="APEX REQUIEM Leaderboard", color=0xFFD700)
    text = ""
    for i, (team, s) in enumerate(sorted_lb[:10]):
        m = ["🥇","🥈","🥉"][i] if i < 3 else f"#{i+1}"
        text += f"{m} **{team}** — {s['total_points']}pts | {s['total_kills']} kills | {s['wins']} wins\n"
    embed.description = text
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="results", description="Tournament results dekho")
async def results(interaction: discord.Interaction, tournament_id: str):
    data = load_data()
    filtered = sorted([r for r in data["match_results"] if r["tournament_id"] == tournament_id], key=lambda x: x["rank"])
    if not filtered:
        await interaction.response.send_message("Koi results nahi!", ephemeral=True); return
    embed = discord.Embed(title=f"Results - {data['tournaments'].get(tournament_id, {}).get('name', tournament_id)}", color=0xFF6600)
    for r in filtered[:10]:
        m = "🥇" if r["rank"]==1 else "🥈" if r["rank"]==2 else "🥉" if r["rank"]==3 else f"#{r['rank']}"
        embed.add_field(name=f"{m} {r['team_name']}", value=f"Points:{r['points']} Kills:{r['kills']}", inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="close_tournament", description="Tournament band karo")
@app_commands.checks.has_permissions(administrator=True)
async def close_tournament(interaction: discord.Interaction, tournament_id: str):
    data = load_data()
    if tournament_id not in data["tournaments"]:
        await interaction.response.send_message("ID galat!", ephemeral=True); return
    data["tournaments"][tournament_id]["status"] = "CLOSED"
    save_data(data)
    await interaction.response.send_message(f"🔒 **{data['tournaments'][tournament_id]['name']}** band ho gaya!")

@bot.tree.command(name="room", description="Room ID share karo")
@app_commands.checks.has_permissions(administrator=True)
async def room(interaction: discord.Interaction, tournament_id: str, room_id: str, password: str):
    data = load_data()
    if tournament_id not in data["tournaments"]:
        await interaction.response.send_message("ID galat!", ephemeral=True); return
    embed = discord.Embed(title="Room Details", description=f"**{data['tournaments'][tournament_id]['name']}**", color=0xFF0000)
    embed.add_field(name="Room ID", value=f"||{room_id}||", inline=True)
    embed.add_field(name="Password", value=f"||{password}||", inline=True)
    embed.add_field(name="Note", value="Sirf registered players join karein!", inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="prize", description="Prize info dekho")
async def prize(interaction: discord.Interaction, tournament_id: str):
    data = load_data()
    if tournament_id not in data["tournaments"]:
        await interaction.response.send_message("ID galat!", ephemeral=True); return
    t = data["tournaments"][tournament_id]
    embed = discord.Embed(title="Prize Center", description=f"**{t['name']}**\nTotal: {t['prize']}", color=0x9B59B6)
    embed.add_field(name="🥇 1st", value="50%", inline=True)
    embed.add_field(name="🥈 2nd", value="30%", inline=True)
    embed.add_field(name="🥉 3rd", value="20%", inline=True)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="ping", description="Bot check karo")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! {round(bot.latency*1000)}ms")

@bot.tree.command(name="help", description="Commands list")
async def help_cmd(interaction: discord.Interaction):
    embed = discord.Embed(title="ApexBot Commands", color=0xFFD700)
    embed.add_field(name="Tournament", value="/create_tournament /tournaments /close_tournament", inline=False)
    embed.add_field(name="Registration", value="/register /registrations", inline=False)
    embed.add_field(name="Results", value="/add_result /results /leaderboard", inline=False)
    embed.add_field(name="Match Day", value="/room /prize", inline=False)
    embed.add_field(name="Utility", value="/ping /help", inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.error
async def on_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("Permission nahi hai!", ephemeral=True)
    else:
        await interaction.response.send_message(f"Error: {error}", ephemeral=True)

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    print("DISCORD_TOKEN nahi mila!")
    exit(1)
bot.run(TOKEN)
