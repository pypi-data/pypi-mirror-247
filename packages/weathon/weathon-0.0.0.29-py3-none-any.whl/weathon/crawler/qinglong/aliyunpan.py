import random
import requests
import time
from typing import Dict, List
from weathon.crawler.qinglong.base import SignIn
from weathon.utils.logger import get_logger, Logger
from weathon.utils import get_environ


class AliYunPan(SignIn):
    def __init__(self, refresh_tokens: List[str] = None):
        self.logger: Logger = get_logger()
        self.refresh_tokens: List[str] = refresh_tokens
        self.access_token_url: str = "https://auth.aliyundrive.com/v2/account/token"
        self.signin_url: str = "https://member.aliyundrive.com/v1/activity/sign_in_list"
        self.reward_url: str = "https://member.aliyundrive.com/v1/activity/sign_in_reward?_rx-s=mobile"

    def _sign_in(self, refresh_token: str) -> str:
        if not refresh_token:
            self.logger.error("refresh_token is None")
            raise ValueError("refresh_token is None")
        data: dict[str, str] = {"grant_type": "refresh_token", "refresh_token": refresh_token}
        response = requests.post(self.access_token_url, json=data)
        access_info: Dict[str, str] = response.json()
        user_name: str = access_info.get("user_name", None)
        access_token: str = access_info.get("access_token", None)

        if not access_token:
            self.logger.error("refresh_token错误，请重新填写refresh_token")
            raise ValueError("refresh_token错误，请重新填写refresh_token")

        # 1. 签到
        data = {"_rx-s": "mobile"}
        headers: Dict[str, str] = {"Authorization": 'Bearer ' + access_token}
        response = requests.post(self.signin_url, json=data, headers=headers)
        signin_info = response.json()
        signin_count: int = signin_info.get("result", {}).get("signInCount", 0)

        # 2. 领奖
        data = {"signInDay": str(signin_count)}
        headers = {"Authorization": 'Bearer ' + access_token}
        response = requests.post(self.reward_url, json=data, headers=headers)
        reward_info = response.json()

        reward_name: str = reward_info.get("result", {}).get("name")
        reward_notice: str = reward_info.get("result", {}).get("notice")

        # 构建签到信息
        message: str = f"账号：{user_name}，签到成功,本月累计签到{signin_count}天,获得奖励:{reward_name}，{reward_notice}"
        return message

    def signin_all(self) -> List[str]:
        messages: List[str] = []
        for refresh_token in self.refresh_tokens:
            signin_message: str = self._sign_in(refresh_token)
            messages.append(signin_message)
        return messages


if __name__ == "__main__":
    time.sleep(random.randint(1, 3600))
    refresh_tokens = get_environ("REFRESH_TOKENS").split(",")
    aliyunpan = AliYunPan(refresh_tokens)
    messages = aliyunpan.signin_all()
    print(messages)
