# dico
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/0eff61ab0fd741ff8e13a086699d6672)](https://www.codacy.com/gh/eunwoo1104/dico/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=eunwoo1104/dico&amp;utm_campaign=Badge_Grade)
[![Discord](https://img.shields.io/discord/832488748843401217)](https://discord.gg/QH4AXNySpB)

**Keep in mind that this project is still WIP, therefore it might be unstable.**

Yet another Discord API wrapper for Python, aimed to follow Discord API format as much as possible but also simple and easy to use.

[Discord Server](https://discord.gg/QH4AXNySpB)

## Features
- Discord v10 API (including Threads, components, context menus, etc.)
- Full interaction support
- API-Only supported, with aiohttp-based or requests-based HTTP client.
- More soon™

## Installation
Development Version:
```
pip install -U git+https://github.com/dico-api/dico
```
PyPi(**Not Recommended**):
```
pip install -U dico-api
```

## Quick Example

### API Client

```py
import dico

api = dico.APIClient("APPLICATION_TOKEN_HERE", base=dico.HTTPRequest)
# You may use AsyncHTTPClient for async support.

# All endpoints are implemented, and for the example request_user (= Get User) will be used.
user = api.request_user()  # You may pass any user ID or it will be the application itself.
# You may use either int, str, dico.Snowflake, or dico.User itself.
print(user.username)
```

### Websocket Client
```py
import dico


client = dico.Client("YOUR_BOT_TOKEN_HERE", intents=dico.Intents.full())


@client.on_message_create
async def on_message_create(message: dico.Message):
    if message.content.startswith("!hello"):
        await message.reply("Hello, World!")


client.run()
```
More examples are in [here](https://github.com/dico-api/dico/tree/master/examples).

## Requirements
- Python 3.7+

## Extra Libs
- [dico-interaction](https://github.com/dico-api/dico-interaction)
- [dico-command](https://github.com/dico-api/dico-command)
