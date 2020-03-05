from discord import Message, ChannelType
from discord.ext.commands import Bot, Cog, command, Context
from ccbot import repo
from shared import fetch_tools
import os

class Submissions(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command()
    async def current(self, ctx: Context) -> None:
        await ctx.trigger_typing()
        repo.init()
        drafts = repo.drafts()
        if not drafts:
            await ctx.send('No competition active')
            return
        writeup = drafts[0]
        msg = f'Current Competition: {writeup.title}\n'
        if writeup.prompt:
            msg += f'```\n{writeup.prompt}\n```\n'
        if writeup.sections:
            msg += f'There are currently {len(writeup.sections) - 1} entries\n'
        await ctx.send(msg)

    @Cog.listener()
    async def on_message(self, msg: Message) -> None:
        if msg.channel.type != ChannelType.private:
            return
        if not msg.attachments:
            return
        await msg.channel.trigger_typing()
        repo.init()
        drafts = repo.drafts()
        if not drafts:
            await msg.channel.send('No competition active')
            return
        writeup = drafts[0]
        author_id = msg.author.id
        url = msg.attachments[0].url
        section_id = writeup.get_section_index(author_id)
        if section_id == -1:
            text = f'\n\n[{author_id}]: {url}\n\nINTRO\n\n![{msg.author.name}\'s Card Name Goes Here][{author_id}]\n\nTEXT\n\n'
            writeup.sections.append(text)
            writeup.save()
            await msg.channel.send(f'Your submission for {writeup.title} has been recorded')
        else:
            text = writeup.sections[section_id].strip()
            lines = text.splitlines()
            if text.startswith(f'[{author_id}]: '):
                lines[0] = f'[{author_id}]: {url}'
            else:
                lines.insert(0, f'[{author_id}]: {url}')
            writeup.sections[section_id] = '\n' + '\n'.join(lines) + '\n'
            writeup.save()
            await msg.channel.send(f'Your submission for {writeup.title} has been updated')

        try:
            if not os.path.exists(os.path.join('site', 'images', writeup.imgdir)):
                os.mkdir(os.path.join('site', 'images', writeup.imgdir))
            await fetch_tools.store_async(msg.attachments[0].url, os.path.join('site', 'images', writeup.imgdir, msg.attachments[0].filename))
        except Exception:
            print('Failed to download')
        repo.commit(f'{writeup.title}: {msg.author.name}\'s submission')
        await fetch_tools.post_discord_webhook('685261389836845077', 'XohTy7E-3ilDYvHIhUsjB9rJf6YaUuHWzGOra1AmJ7XNbci-5C7omOypgcEjG_UHUZRy', f'<@{author_id}> submitted {url}')

def setup(bot: Bot) -> None:
    bot.add_cog(Submissions(bot))
