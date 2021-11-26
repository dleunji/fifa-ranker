from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import httpx, json, os
load_dotenv(verbose=True)
API_KEY = os.getenv('API_KEY')

class Player(BaseModel):
    id: int
    po: int

class Ranker(BaseModel):
    matchtype: int
    players: List[Player] = []

app = FastAPI()

@app.get("/match")
async def read_match_type():
    url = "https://static.api.nexon.co.kr/fifaonline4/latest/matchtype.json"
    async with httpx.AsyncClient() as client:
        res = await client.get(url)
    return res.json()

@app.get("/pos")
async def read_pos():
    url = "https://static.api.nexon.co.kr/fifaonline4/latest/spposition.json"
    async with httpx.AsyncClient() as client:
        res = await client.get(url)
    return res.json()

@app.get("/athlete")
async def read_athletes():
    url = "https://static.api.nexon.co.kr/fifaonline4/latest/spid.json"
    async with httpx.AsyncClient() as client:
        res = await client.get(url)
    return res.json()


@app.get("/actionshot/{spid}")
async def read_actionshot(spid: int):
    url = f"https://fo4.dn.nexoncdn.co.kr/live/externalAssets/common/playersAction/p{spid}.png"
    async with httpx.AsyncClient() as client:
        res = await client.get(url)
    return res


# Stringify the list[object]
@app.post("/rankers")
async def get_stat(ranker: Ranker):
    # 1안
    # url = f"https://api.nexon.co.kr/fifaonline4/v1.0/rankers/status?matchtype={ranker.matchtype}&players=["
    # for p in ranker.players:
    #     url += "{\"id\":" + str(p.id) + ", \"po\":" + str(p.po) + "}"
    # url += "]"
    # async with httpx.AsyncClient() as client:
    #     res = await client.get(url, headers={'Authorization' : API_KEY})
    # print(res.request.url)
    # return res.json()

    # 2안 
    # url = "https://api.nexon.co.kr/fifaonline4/v1.0/rankers/status"
    # async with httpx.AsyncClient() as client:
    #     res = await client.get(url, params = {"matchtype": ranker.matchtype, "players": ranker.players}, headers={'Authorization' : API_KEY})
    # print(res.request.url)
    # return res.json()

    # 3안
    url = "https://api.nexon.co.kr/fifaonline4/v1.0/rankers/status"
    async with httpx.AsyncClient() as client:
        res = await client.get(url, params = {"matchtype": ranker.matchtype, "players": json.dumps([{"id": p.id, "po": p.po} for p in ranker.players])}, headers={'Authorization' : API_KEY})
    print(res.request.url)
    return res.json()


