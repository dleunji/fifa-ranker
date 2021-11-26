import streamlit as st
from typing import List
import asyncio
from pydantic import BaseModel
from dotenv import load_dotenv
import httpx, json, os
load_dotenv(verbose=True)
API_KEY = os.getenv('API_KEY')
BASE_URL = "https://static.api.nexon.co.kr/fifaonline4/latest/"

class Player(BaseModel):
    id: int
    po: int

class Ranker(BaseModel):
    matchtype: int
    players: List[Player] = []

# Client instance uses HTTP connection pooling
# Make Several Requests to the same host, Client will reuse the underlying TCP connection
client = httpx.AsyncClient()

async def read_match_type():
    res = await client.get(BASE_URL + "matchtype.json")
    matchtype = res.json()
    return matchtype

async def read_pos():
    res = await client.get(BASE_URL + "spposition.json")
    pos = res.json()
    return pos

async def read_athletes():
    res = await client.get(BASE_URL + "spid.json")
    athletes = res.json()
    return athletes

async def read_actionshot(spid: int):
    url = f"https://fo4.dn.nexoncdn.co.kr/live/externalAssets/common/playersAction/p{spid}.png"
    res = await client.get(url)
    return res

async def get_stat(ranker: Ranker):
    url = "https://api.nexon.co.kr/fifaonline4/v1.0/rankers/status"
    async with httpx.AsyncClient() as client:
        res = await client.get(url, params = {"matchtype": ranker.matchtype, "players": json.dumps([{"id": p.id, "po": p.po} for p in ranker.players])}, headers={'Authorization' : API_KEY})
    return res.json()

async def main():
    st.title('⚽ FIFA Online4 스탯 분배 가이드')
    st.markdown('FIFA 초심자들은 어떻게 스탯을 분배해야 선수의 재량을 끌어낼 수 있는지 알기 어렵습니다.')
    st.markdown('이에 도움이 되고자 **TOP 10,000 랭커 유저가 사용한 선수의 평균 스탯 기록**을 제공합니다.')
    matchtype, pos, athletes = await asyncio.gather(
        read_match_type(),
        read_pos(),
        read_athletes()
    )
    st.json(matchtype)
    st.json(pos)
    st.json(athletes)

asyncio.run(main())

