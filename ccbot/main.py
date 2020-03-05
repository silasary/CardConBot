from shared import configuration
import discord
from discord.ext import commands

class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix='->')
        super().load_extension('ccbot.submit')


    def init(self) -> None:
        self.run(configuration.get('token'))

    async def on_ready(self) -> None:
        print(f'{self.user.name} has connected to Discord!')
        super()
