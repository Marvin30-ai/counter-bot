from flask import Flask
from threading import Thread
import discord
from discord.ui import Button, View

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot läuft!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

TOKEN = "DEIN_NEUER_TOKEN"

counter = {}

class CounterView(View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.user_id = user_id

    @discord.ui.button(label="+1", style=discord.ButtonStyle.green)
    async def add(self, button, interaction):
        if interaction.user.id != self.user_id:
            return await interaction.response.send_message("Nicht dein Counter!", ephemeral=True)
        counter[self.user_id] = counter.get(self.user_id, 0) + 1
        await interaction.response.edit_message(content=self.get_text(interaction.user.name))

    @discord.ui.button(label="-1", style=discord.ButtonStyle.red)
    async def sub(self, button, interaction):
        if interaction.user.id != self.user_id:
            return await interaction.response.send_message("Nicht dein Counter!", ephemeral=True)
        counter[self.user_id] = max(0, counter.get(self.user_id, 0) - 1)
        await interaction.response.edit_message(content=self.get_text(interaction.user.name))

    def get_text(self, name):
        zahl = counter.get(self.user_id, 0)
        return f"**{name}** hat aktuell: **{zahl}**"

class MyBot(discord.Bot):
    async def on_ready(self):
        print(f"Bot ist online als {self.user}")

bot = MyBot()

@bot.slash_command(name="counter", description="Startet deinen persönlichen Counter")
async def counter_cmd(ctx):
    view = CounterView(ctx.author.id)
    await ctx.respond(f"**{ctx.author.name}** hat aktuell: **0**", view=view)

keep_alive()
bot.run(TOKEN)
