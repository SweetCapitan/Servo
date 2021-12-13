import aiohttp
from discord.webhook import Webhook


async def send_webhook(webhook_url: str, text: str):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(webhook_url, session=session)
        await webhook.send(text)
