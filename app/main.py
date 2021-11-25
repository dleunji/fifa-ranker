from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import httpx, json, os
load_dotenv(verbose=True)
API_KEY = os.getenv('API_KEY')

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

# @app.get("/meta")
# async def read_meta():
#     match = await read_match_type()
#     pos = await read_pos()
#     athletes_id = await read_athletes()
#     return 

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: List[str] = []


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results

class Player(BaseModel):
    id: int
    po: str

class Ranker(BaseModel):
    matchtype: int
    players: List[Player] = []

# Stringify the list[object]
@app.post("/rankers")
async def get_stat(ranker: Ranker):
    url = "https://api.nexon.co.kr/fifaonline4/v1.0/rankers/status"
    # param = {"matchtype": ranker.matchtype, "players": }
    async with httpx.AsyncClient() as client:
        print(ranker.matchtype)
        print(ranker.players)
        res = await client.get(url, 
                        params={"matchtype": ranker.matchtype, "players": json.dumps([{"id": p.id, "po": p.po} for p in ranker.players])},
                        headers={'Authorization' : API_KEY})
        print(res.request.url)
        print(res.json())
    return res.json()
    # results = body
    # return results

