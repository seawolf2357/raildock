import httpx
import asyncio
import aiohttp
from fastapi import FastAPI, Request

app = FastAPI()


async def getResponseFromChatbase(prompt):
    url = "https://www.chatbase.co/api/v1/chat"
    payload = {
        "stream": False,
        "temperature": 0,
        "chatId": "6dMpdT5zPPS5ik9pKptsH",
        "messages": [{"role": "user", "content": prompt}]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer e81b355c-30cc-47ca-b9fa-deb33f7159ad"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as resp:
            response = await resp.json()
            return response['text']

def textResponseFormat(bot_response):
    response = {
        'version': '2.0',
        'template': {
            'outputs': [{"simpleText": {"text": bot_response}}],
            'quickReplies': []
        }
    }
    return response

async def create_callback_request_kakao(prompt, callbackUrl):
    bot_res = await getResponseFromChatbase(prompt)
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    async with aiohttp.ClientSession() as session:
        async with session.post(callbackUrl, json=textResponseFormat(bot_res), headers=headers, timeout=5) as resp:
            await resp.text()

@app.post("/chat2/", tags=["kakao"])

async def chat2(request: Request):
    kakao_request = await request.json()

    length = len(kakao_request["userRequest"]["utterance"])
    if length < 5 or length > 200:
        return textResponseFormat("질문은 5자 이상 200자 이하로 입력해주세요")

    asyncio.create_task(
        create_callback_request_kakao(
            prompt=kakao_request["userRequest"]["utterance"],
            callbackUrl=kakao_request["userRequest"]["callbackUrl"],
        )
    )

    return {"version": "2.0", "useCallback": True}