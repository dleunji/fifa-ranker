from enum import auto
import streamlit as st
import httpx, json, os
import pandas as pd
import asyncio
from pydantic import BaseModel
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
load_dotenv(verbose=True)

API_KEY = os.getenv('API_KEY')
BASE_URL = "https://static.api.nexon.co.kr/fifaonline4/latest/"

class Player(BaseModel):
    id: int
    po: int
    matchtype: int

# Client instance uses HTTP connection pooling
# Make Several Requests to the same host, Client will reuse the underlying TCP connection
async def get_actionshot(spid: int):
    img_url = f"https://fo4.dn.nexoncdn.co.kr/live/externalAssets/common/playersAction/p{spid}.png"
    async with httpx.AsyncClient() as client:
        res = await client.get(img_url)
    img = Image.open(BytesIO(res.content))
    return img

# Return stat per player with status code
async def get_stat(player: Player):
    stat_url = "https://api.nexon.co.kr/fifaonline4/v1.0/rankers/status"
    async with httpx.AsyncClient() as client:
        res = await client.get(stat_url,
                    params = {"matchtype": player.matchtype, "players": json.dumps([{"id": player.id, "po": player.po}])}, 
                    headers={'Authorization' : API_KEY})
    return res

async def search(matchtype_idx: int, pos_idx: int, athlete_idx: int):
    player = Player(matchtype=matchtype_idx, id=athlete_idx, po=pos_idx)
    stat, img = await asyncio.gather(get_stat(player), get_actionshot(athlete_idx))
    col1, col2 = st.columns(2)
    with col1:
        st.image(img, width=180, use_column_width=auto)
    with col2:
        try:
            assert stat.status_code == 200
            status = stat.json()[0]['status']
            st.json(status)
        except:
            st.write('기록이 없습니다.')
            st.write('선수와 포지션이 매치되는지 확인해보세요.')
            st.write('만약 그래도 이상이 없다면 매치타입을 변경해보세요')

async def main():
    st.title('⚽ FIFA Online4 스탯 분배 가이드')
    st.markdown('FIFA 초심자들은 어떻게 스탯을 분배해야 선수의 재량을 끌어낼 수 있는지 알기 어렵습니다.')
    st.markdown('초심자의 플레이에 도움이 되고자 **TOP 10,000 랭커 유저가 사용한 선수의 평균 스탯 기록**을 제공합니다.')
    st.markdown('참고하고 싶은 매치 타입, 포지션, 선수를 선택하세요.')

    # GET Meta Info
    async with httpx.AsyncClient() as client:
        matchtype, pos, athlete = await asyncio.gather(
            client.get(BASE_URL + "matchtype.json"),
            client.get(BASE_URL + "spposition.json"),
            client.get(BASE_URL + "spid.json")
        )
    matchtype = matchtype.json()
    pos = pos.json()
    athlete = athlete.json()

    matchtype_df = pd.DataFrame(matchtype)
    matchtype_idx = st.selectbox('1. 매치를 선택하세요.', range(len(matchtype_df)), format_func=lambda x: matchtype_df.iloc[x,1])
    matchtype_id = matchtype_df.iloc[matchtype_idx, 0]

    pos_df = pd.DataFrame(pos)
    pos_idx = st.selectbox('2. 포지션을 선택하세요.', range(len(pos_df)), format_func= lambda x : pos_df.iloc[x, 1])
    pos_id = pos_df.iloc[pos_idx, 0]

    athlete_df = pd.DataFrame(athlete)
    athlete_idx = st.selectbox('3. 선수를 검색하세요.',range(len(athlete_df)),format_func= lambda x : athlete_df.iloc[x, 1])
    athlete_id = athlete_df.iloc[athlete_idx, 0]

    if st.button('Search'):
        await search(matchtype_id, pos_id, athlete_id)

asyncio.run(main())

