# Pycord_ext_i18n

### A regular localization Library for pycord.

## Installation
To install the pycord_ext_i18n, you can just run the following command:

```bash
# Windows
pip install pycord_ext_i18n

# Linux/MacOS

python3 -m pip install pycord_ext_i18n
```
## Prepare
First, You will need to a locale configuration file (*.json) to store your command parameter or string.
A locale configuration file internal structure will be like it:

```json

{
    "command.{command_name}.name": "help", #your command_name name.
    "command.{command_name}.description": "help_description", #your command_name description.
    "hello": "你好" #this is string.  
}

```

And, save your locale configuration file to locale folder.
The name is the country code you want! (like Zh-TW, en-US...)

## Basic Usage 

Usage: Get a text.

```py

from pycord_ext_i18n import I18n

i18n = I18n()
i18n.load('./locale')
print(i18n.get_text("hello", "zh-TW", None)) #Print: 你好

```

Usage: Use localize_slash_commands to localize your slash command (Remember configuration file).

```py
from discord import ApplicationContext
from discord.ext import commands

from pycord_ext_i18n import I18n

i18n = I18n()

class ExampleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @i18n.localize_slash_commands()
    async def test(self, ctx: ApplicationContext):
        await ctx.response.send_message(content=f"My command name is {ctx.command.name}!")

def setup(bot):
    bot.add_cog(ExampleCog(bot))
```