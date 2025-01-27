import requests
import os
from dotenv import load_dotenv

# load .env
load_dotenv()

class Oauth:

    def __init__(self):
        self.auth_server = "https://kauth.kakao.com%s"
        self.api_server = "https://kapi.kakao.com%s"
        self.default_header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache",
        }

    def auth(self, code):
        return requests.post(
            url=self.auth_server % "/oauth/token",
            headers=self.default_header,
            data={
                "grant_type": "authorization_code",
                "client_id": os.environ.get('CLIENT_ID'),
                "client_secret": os.environ.get('CLIENT_SECRET'),
                "redirect_uri": os.environ.get('REDIRECT_URI'),
                "code": code,
            },
        ).json()
    
    def userinfo(self, bearer_token):
        # bearer_token에 'Bearer' 접두어가 없는 경우 추가
        if not bearer_token.startswith('Bearer '):
            bearer_token = f"Bearer {bearer_token}"

        print("사용되는 토큰:", bearer_token)  # 디버깅용
        return requests.post(
            url=self.api_server % "/v2/user/me",
            headers={
                **self.default_header,
                **{"Authorization": bearer_token }
            },
            # "property_keys":'["kakao_account.profile_image_url"]'
            data={}
        ).json()