"""
Commands to manage the bot blacklist.

This file should only be called through `bot.add_blacklist()`,
after the "blacklist" value has been set in the config.
"""

import aiosqlite
import discord

from .. import emb
from ..blacklist import _BanDB
from ..bot import Bot, Cog
from ..components import event
from ..errors import Blacklisted, ErrorMessageSent
from ..internal import EzConfig, t
from ..internal.dc import DPY, PYCORD, commands, discord
from ..logs import log
from ..utils import create_text_file

_db = _BanDB()


async def get_or_fetch_user(bot, user_id: int):
    if user := bot.get_user(user_id):
        return user
    try:
        return await bot.fetch_user(user_id)
    except discord.NotFound:
        return None


async def _check_blacklist(interaction: discord.Interaction) -> bool:
    bans = await _db.get_bans()
    if interaction.user.id in bans and EzConfig.blacklist:
        if EzConfig.blacklist.raise_error:
            raise Blacklisted()
        else:
            await interaction.response.send_message(t("no_perms"), ephemeral=True)
        raise ErrorMessageSent()
    return True


@event
async def view_check(interaction: discord.Interaction):
    return await _check_blacklist(interaction)


class Blacklist(Cog, hidden=True):
    def __init__(self, bot: Bot):
        super().__init__(bot)

        if DPY:
            bot.tree.interaction_check = self.global_interaction_check

    async def bot_check(self, ctx):
        """Checks if a blacklisted user is trying to use a command."""
        return await _check_blacklist(ctx)

    async def cog_check(self, ctx):
        if EzConfig.blacklist.owner_only:
            if not await self.bot.is_owner(ctx.user):
                if DPY:
                    return False
                else:
                    raise commands.NotOwner()
        return True

    async def global_interaction_check(self, interaction: discord.Interaction):
        """Bot check for application commands in Discord.py."""
        return await _check_blacklist(interaction)

    async def interaction_check(self, interaction: discord.Interaction):
        """Cog check for application commands in Discord.py."""
        await self.cog_check(interaction)

    @Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        bans = await _db.get_bans()
        if guild.owner.id in bans:
            try:
                await guild.owner.send(t("guild_error", guild.name))
            except discord.Forbidden:
                pass
            await guild.leave()

    if PYCORD:
        admin = discord.SlashCommandGroup(
            t("admin_group"),
            description="syncord admin commands",
            guild_ids=EzConfig.admin_guilds,
            default_member_permissions=discord.Permissions(administrator=True),
        )
        leave = admin.create_subgroup("leave")
        blacklist = admin.create_subgroup("blacklist")
    else:
        admin = discord.app_commands.Group(
            name=t("admin_group"),
            description="syncord admin commands",
            guild_ids=EzConfig.admin_guilds,
            default_permissions=discord.Permissions(administrator=True),
        )
        leave = discord.app_commands.Group(
            parent=admin,
            name="leave",
            description="Make the bot leave a server",
        )
        blacklist = discord.app_commands.Group(
            parent=admin,
            name="blacklist",
            description="Manage the blacklist",
        )

    @blacklist.command(name="add", description="Add a member  blacklist")
    # @discord.option("user", description="The user to ban/unban")
    # @discord.option("reason", description="The reason for the ban", default=None)
    async def blacklist_add(
        self,
        ctx,
        user: discord.Member,
        reason: str = None,  # type: ignore
    ):
        if user.id == ctx.user.id:
            return await emb.error(ctx, "You can't ban yourself.")
        if user.bot:
            return await emb.error(ctx, "You can't ban a bot.")

        try:
            await _db.add_ban(user.id, reason)
        except aiosqlite.IntegrityError:
            return await emb.error(ctx, "This user is already banned.")
        await ctx.response.send_message(
            f"The user was banned successfully.\n- **Name:** {user}\n- **ID:** {user.id}",
            ephemeral=True,
        )

    @blacklist.command(name="remove", description="Remove a member from the blacklist")
    # @discord.option("user", description="The user to ban/unban")
    async def blacklist_remove(self, ctx, user: discord.Member):
        rowcount = await _db.remove_ban(user.id)
        if rowcount == 0:
            return await emb.error(ctx, "This user is not banned.")
        await ctx.response.send_message(
            f"The user **{user}** was unbanned successfully.", ephemeral=True
        )

    @blacklist.command(name="show", description="Show the bot blacklist")
    async def show_blacklist(self, ctx):
        await ctx.response.defer(ephemeral=True)
        bans = await _db.get_full_bans()
        desc = ""

        for user_id, reason, _ in bans:
            if not reason:
                reason = "No reason provided"

            user = await get_or_fetch_user(self.bot, user_id)
            name = f"{user.name} ({user.id})" if user else user_id
            desc += f"{name} - {reason}\n"

        if not desc:
            desc = "No bans found."

        file = create_text_file(desc, "bans.txt")
        await ctx.followup.send(file=file, ephemeral=True)

    @admin.command(description="Show all bot servers")
    async def show_servers(self, ctx):
        await ctx.response.defer(ephemeral=True)
        longest_name = max([guild.name for guild in self.bot.guilds], key=len)
        sep = f"<{len(longest_name)}"

        desc = ""
        for guild in self.bot.guilds:
            desc += f"{guild.name:{sep}} - {guild.member_count:<6,}"
            desc += f" - {guild.id}"
            if guild.owner:
                desc += f" - {guild.owner} ({guild.owner.id})"
            desc += "\n"

        file = create_text_file(desc, "guilds.txt")
        await ctx.followup.send(file=file, ephemeral=True)

    @leave.command(name="server", description="Make the bot leave a server")
    # @discord.option("guild_id", description="Leave the server with the given ID", default=None)
    async def leave_guild(self, ctx, guild_id: str):
        await ctx.response.defer(ephemeral=True)
        try:
            guild = await self.bot.fetch_guild(guild_id)
        except Exception as e:
            return await ctx.response.send_message(
                f"I could not load this server: ```{e}```", ephemeral=True
            )

        await guild.leave()
        await ctx.response.send_message(f"I left **{guild.name}** ({guild.id})", ephemeral=True)

    @leave.command(name="owner", description="Make the bot leave all guilds with a given owner")
    # @discord.option("owner_id", description="Leave all servers with the specified owner")
    async def leave_owner(self, ctx, owner: discord.User):
        await ctx.defer(ephemeral=True)
        guilds = []
        member_count = 0
        for guild in self.bot.guilds:
            if guild.owner.id == owner.id:
                guilds.append(guild)
                member_count += guild.member_count

        return await ctx.response.send_message(
            f"I found **{len(guilds)}** servers with **{owner}** as the owner "
            f"(with a total of **{member_count}** members).",
            ephemeral=True,
            view=LeaveGuilds(guilds),
        )


class LeaveGuilds(discord.ui.View):
    def __init__(self, guilds: list[discord.Guild]):
        self.guilds = guilds
        super().__init__(timeout=None)

    @discord.ui.button(label="Leave all", style=discord.ButtonStyle.red)
    async def leave(self, _: discord.ui.Button, interaction: discord.Interaction):
        if not PYCORD:
            interaction = _

        for child in self.children:
            child.disabled = True
        embed = discord.Embed(
            description="I'll now leave all servers. This may take a while."
            "\n\nI'll ping you when I'm done.",
        )
        await interaction.response.edit_message(embed=embed, view=self)

        leave_count = 0
        for guild in self.guilds:
            try:
                await guild.leave()
                leave_count += 1
            except Exception as e:
                log.warning(f"Could not leave guild **{guild.id}**: {e}")
                continue

        await interaction.followup.send(
            f"{interaction.user.mention} I successfully left **{leave_count}** servers.",
            ephemeral=True,
        )

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.grey)
    async def cancel(self, _: discord.ui.Button, interaction: discord.Interaction):
        if not PYCORD:
            interaction = _

        for child in self.children:
            child.disabled = True
        await interaction.edit(view=self)
