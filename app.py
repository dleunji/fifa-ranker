import streamlit as st
import httpx, json
import pandas as pd
import asyncio
from pydantic import BaseModel
from PIL import Image
from io import BytesIO
# from dotenv import load_dotenv

# If you want to use API_KEY from .env file, please pip install python-dotenv and import
# load_dotenv(verbose=True)
# API_KEY = os.getenv('API_KEY')
API_KEY = st.secrets["API_KEY"]
BASE_URL = "https://static.api.nexon.co.kr/fifaonline4/latest/"

class Player(BaseModel):
    id: int
    po: int
    matchtype: int

async def get_actionshot(spid: int):
    img_url = f"https://fo4.dn.nexoncdn.co.kr/live/externalAssets/common/playersAction/p{spid}.png"
    async with httpx.AsyncClient() as client:
        res = await client.get(img_url)
    img = Image.open(BytesIO(res.content))
    return img

async def get_stat(player: Player):
    stat_url = "https://api.nexon.co.kr/fifaonline4/v1.0/rankers/status"
    async with httpx.AsyncClient() as client:
        res = await client.get(stat_url,
                    params = {"matchtype": player.matchtype, "players": json.dumps([{"id": player.id, "po": player.po}])}, 
                    headers={'Authorization': API_KEY})
    return res

def translate(stat: dict):
    st.write('평균 슛 수: ', stat["shoot"])
    st.write('평균 유효 슛 수:', stat["effectiveShoot"])
    st.write('평균 어시스트 수: ',stat["assist"])
    st.write('평균 득점 수: ', stat["goal"])
    st.write('평균 드리블 거리(야드): ',stat["dribble"])
    st.write('평균 드리블 시도 수: ', stat["dribbleTry"])
    st.write('평균 드리블 성공 수: ', stat["dribbleSuccess"])
    st.write('평균 패스 시도 수: ', stat["passTry"])
    st.write('평균 패스 성공 수: ', stat["passSuccess"])
    st.write('평균 블락 성공 수: ', stat["block"])
    st.write('평균 태클 성공 수: ', stat["tackle"])
    st.write('해당 포지션으로 경기 참여한 횟수: ', stat["matchCount"])

# Get Ranker Info Using FIFA Open API
async def search(player_name: str, matchtype_idx: int, pos_idx: int, athlete_idx: int):
    player = Player(matchtype=matchtype_idx, id=athlete_idx, po=pos_idx)
    stat, img = await asyncio.gather(get_stat(player), get_actionshot(athlete_idx))
    col1, col2 = st.columns(2)
    with col1:
        st.image(img, width=180, use_column_width='auto', caption=player_name)
    with col2:
        try:
            assert stat.status_code == 200
            status = stat.json()[0]['status']
            translate(status)
        except Exception as e:
            st.write('기록이 없습니다.')
            st.write('선수와 포지션이 매치되는지 확인해보세요.')
            st.write('그래도 기록이 없다고 뜨면 매치타입을 변경해보세요.')

async def main():
    st.set_page_config(
        page_title='FIFA Online4 스탯 활용 가이드',
        page_icon = '⚽'
    )

    st.title('⚽ FIFA Online4 스탯 활용 가이드')
    st.markdown('FIFA 초심자들은 어떻게 스탯을 분배해야 선수의 재량을 끌어낼 수 있는지 알기 어렵습니다.')
    st.markdown('초심자의 플레이에 도움이 되고자 **TOP 10,000 랭커 유저가 사용한 선수의 평균 스탯 기록**을 제공합니다.')
    st.markdown('참고하고 싶은 매치 타입, 포지션, 선수를 선택하세요.')

    # Client instance uses HTTP connection pooling
    # Make Several Requests to the same host, Client will reuse the underlying TCP connection
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

    # To prevent printing 'None', pass the value to r
    if st.button('Search'):
        r = await search(athlete_df.iloc[athlete_idx, 1],matchtype_id, pos_id, athlete_id)

if __name__=="__main__":
    asyncio.run(main())

