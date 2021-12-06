import aiohttp
<<<<<<< HEAD
from discord.webhook import Webhook, AsyncWebhookAdapter
=======
from discord.webhook import Webhook
>>>>>>> e1b86f4 ([Update] Lib.py is spliced into other small files)


async def send_webhook(webhook_url: str, text: str):
    async with aiohttp.ClientSession() as session:
<<<<<<< HEAD
        webhook = Webhook.from_url(webhook_url, adapter=AsyncWebhookAdapter(session))
=======
        webhook = Webhook.from_url(webhook_url, session=session)
>>>>>>> e1b86f4 ([Update] Lib.py is spliced into other small files)
        await webhook.send(text)
