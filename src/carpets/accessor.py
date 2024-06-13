import aiohttp
import asyncio
import json
from core.config import settings


class Text2ImageAPI:

    @classmethod
    async def get_model(cls):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=settings.ai_setting.ai_url + settings.ai_setting.ai_model_request,
                headers=settings.ai_setting.ai_model_headers
            ) as response:
                data = await response.json()
                return data[0]['id']

    @classmethod
    async def generate(cls, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": str(images),
            "width": str(width),
            "height": str(height),
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = aiohttp.FormData()
        data.add_field('model_id', str(model))
        data.add_field('params', json.dumps(params), content_type='application/json')

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=settings.ai_setting.ai_url + settings.ai_setting.ai_model_run,
                headers=settings.ai_setting.ai_model_headers,
                data=data
            ) as response:
                data = await response.json()
                return data['uuid']

    @classmethod
    async def check_generation(cls, request_id, attempts=10, delay=10):
        while attempts > 0:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url=settings.ai_setting.ai_url + settings.ai_setting.ai_model_status + request_id,
                    headers=settings.ai_setting.ai_model_headers
                ) as response:
                    data = await response.json()
                    if data['status'] == 'DONE':
                        return data['images']

            attempts -= 1
            await asyncio.sleep(delay)
