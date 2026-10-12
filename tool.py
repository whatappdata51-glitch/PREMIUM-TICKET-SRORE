import os
import discord
import asyncio

from dotenv import load_dotenv
from discord.ext import commands
from discord.ui import View, Select

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
TICKET_CHANNEL_ID = int(os.getenv("TICKET_CHANNEL_ID"))

CATEGORY_NAME = "🎫 AXB SUPPORT"

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


# =========================
# CLOSE TICKET BUTTON
# =========================
class ClosePanel(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Close Ticket",
        emoji="🔒",
        style=discord.ButtonStyle.danger,
        custom_id="close_ticket_btn"
    )
    async def close_ticket(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message(
                "❌ Only Admins Can Close Tickets.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            "🔒 Closing Ticket In 5 Seconds...",
            ephemeral=True
        )

        await asyncio.sleep(5)

        try:
            await interaction.channel.delete()
        except:
            pass


# =========================
# PRODUCT SELECT MENU
# =========================
class ProductSelect(Select):
    def __init__(self):

        options = [
            discord.SelectOption(
                label="PREMIUM UID BYPASS",
                emoji="<a:welcome:1330517345508261900>",
                description="PREMIUM UID BYPASS SERVICE"
            ),
            discord.SelectOption(
                label="UID BYPASS",
                emoji="<a:welcome:1533400305775939636>",
                description="STANDARD UID BYPASS SERVICE"
            ),
            discord.SelectOption(
                label="AXB PREMIUM PANEL",
                emoji="<a:welcome:1330517345508261900>",
                description="PREMIUM PANEL ACCESS"
            ),
            discord.SelectOption(
                label="LIB BYPASS",
                emoji="<a:welcome:1330517345508261900>",
                description="LIB BYPASS ALL SERVER SAFE"
            ),
            discord.SelectOption(
                label="BR MOD",
                emoji="<a:welcome:1330517345508261900>",
                description="BR MOD PANEL"
            )
        ]

        super().__init__(
            placeholder="🛒 Select Product To Purchase...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="product_select"
        )

    async def callback(self, interaction: discord.Interaction):

        guild = interaction.guild
        user = interaction.user
        product = self.values[0]

        ticket_name = f"ticket-{user.name}".lower().replace(" ", "-")
        existing_ticket = discord.utils.get(
            guild.channels,
            name=ticket_name
        )

        if existing_ticket:
            await interaction.response.send_message(
                f"❌ You Already Have A Ticket:\n{existing_ticket.mention}",
                ephemeral=True
            )
            return

        category = discord.utils.get(
            guild.categories,
            name=CATEGORY_NAME
        )

        if category is None:
            category = await guild.create_category(
                CATEGORY_NAME
            )

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                view_channel=False
            ),

            user: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            ),

            guild.me: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            )
        }

        ticket_channel = await guild.create_text_channel(
            name=ticket_name,
            category=category,
            overwrites=overwrites
        )

        embed = discord.Embed(
            title="💎 AXB STORE ORDER",
            description=(
                f"👤 Customer: {user.mention}\n\n"
                f"🛒 Product Selected:\n"
                f"**{product}**\n\n"
                f"📩 Please Send Your Message Below.\n"
                f"⚡ Support Team Will Reply Soon."
            ),
            color=0x8B5CF6
        )

        embed.set_footer(
            text="AXB STORE • Premium Support"
        )

        await ticket_channel.send(
            content=user.mention,
            embed=embed,
            view=ClosePanel()
        )

        await interaction.response.send_message(
            f"✅ Ticket Created Successfully:\n{ticket_channel.mention}",
            ephemeral=True
        )


# =========================
# PRODUCT VIEW
# =========================
class ProductView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ProductSelect())


# =========================
# BOT READY
# =========================
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

    bot.add_view(ProductView())
    bot.add_view(ClosePanel())


# =========================
# PANEL COMMAND
# =========================
@bot.command()
async def panel(ctx):

    if ctx.channel.id != TICKET_CHANNEL_ID:
        await ctx.send(
            "❌ This Command Only Works In Buy Now Channel."
        )
        return

    embed = discord.Embed(
        title="<a:welcome:1533417041615392879>  **AXB STORE**   <a:welcome:1533417041615392879> ",
        description=(
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "<a:welcome:1546092136787611658> PURCHASE CENTER\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Select Your Product From The Menu Below.\n\n"
            "<a:welcome:1533400305775939636> PREMIUM UID BYPASS\n"
            "<a:welcome:1533400305775939636> UID BYPASS\n"
            "<a:welcome:1533400305775939636> PREMIUM PANEL\n"
            "<a:welcome:1533400305775939636> LIB BYPASS\n"
            "<a:welcome:1533400305775939636> BR MOD\n\n"
            "After Selecting A Product,\n"
            "A Private Ticket Will Be Created Automatically."
        ),
        color=0x8B5CF6
    )

    if ctx.guild.icon:
        embed.set_thumbnail(
            url=ctx.guild.icon.url
        )

    embed.set_image(
        url="https://imagetourl.cloud/96osb79g.gif"
    )

    embed.set_footer(
        text="AXB STORE • Premium Services"
    )

    await ctx.send(
        embed=embed,
        view=ProductView()
    )


bot.run(TOKEN)
