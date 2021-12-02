<h1 align="center"> ⚽ FIFA Online4 스탯 활용 가이드</h1>
<p align="center">
    FIFA 초심자가 참고하면 좋은 TOP 10,000 랭커 기록
</p>
<p align="center">
    <a href="https://share.streamlit.io/dleunji/fifa-ranker/app.py">
        <img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg" alt="Open in Streamlit" />
    </a>    
</p>

![prototype](https://user-images.githubusercontent.com/46207836/144355863-04ceaa0c-791a-41ae-8e9b-ac9bf7008cd1.PNG)


[Nexon Open API](https://developers.nexon.com/fifaonline4/api/11/22)를 사용해 FIFA 초심자들이 랭커의 스탯 기록을 참고해 플레이를 즐길 수 있도록 합니다.

Streamlit으로 프로토타입을 제작한 후 [Streamlit Cloud](https://streamlit.io/cloud)로 배포하였습니다.

## Getting Started
```shell
$ git clone https://github.com/dleunji/fifa-ranker .
```

## Requirements
```python
$ pip install -r requirements.txt
```

### API Key Issue
환경변수인 API KEY를 `.steamlit/secrets.toml`에 저장하여 사용하나 보안 상의 문제로 Repository 에 업로드하지 않았습니다. TOML의 형식에 맞게 `.steamlit/secrets.toml`에 `API_KEY="<your secret key>"`를 입력하세요.





