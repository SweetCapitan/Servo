import aiohttp
from discord.webhook import Webhook, AsyncWebhookAdapter


async def send_webhook(webhook_url: str, text: str):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(webhook_url, adapter=AsyncWebhookAdapter(session))
        await webhook.send(text)
