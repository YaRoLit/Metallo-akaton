import os
import time
import requests
import uuid
import json


class Giga_chat():
    def __init__(self):
        self.llm = self.load_llm()


    def load_llm(self,
            model_type="GigaChat-Pro",
            auth_url="https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
            scope="GIGACHAT_API_PERS",
            req_url="https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    ) -> None:
        """
        Загрузка 
        """
        self.token_start_time = time.time()
        #self.__auth_token = os.environ['gigachat_api_token']
        self.scope = scope
        self.auth_url = auth_url
        self.req_url = req_url
        self.model_params = {
            "model": model_type,
            "messages":  [{
                "role": "user",
                "content": ""
            }],
            "temperature": 1,
            "top_p": 0.1,
            "n": 1,
            "stream": False,
            "max_tokens": 512,
            "repetition_penalty": 1,
            "update_interval": 0
        }        
        self.tokens_session_cntr = {
            "prompt": 0,
            "cmpl": 0,
            "total": 0
        }
        self.__token = self.get_token()


    def get_token(self) -> str:
        """
        POST запрос на токен с отключеной верификацией (МинЦифры)
        """
        response = requests.post(
            self.auth_url,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
                "RqUID": str(uuid.uuid4()),
                "Authorization": f"Basic NDNlYzAyMzgtNWQ4Zi00M2U1LWE3YWItYTdlODRiZmEyY2NkOmE1YmY2ZDc1LTQ4ZjktNDhkMi1iOGQ0LTkzY2NmZmVmOTdjMQ=="
            },
            data={"scope": self.scope},
            verify=False
        )
        return response.json()["access_token"]


    def llm_request(self, prompt: str) -> str:
        """
        Посылаем запросы, получаем ответы, считаем токены
        """
        if not hasattr(self, 'llm'):
            self.load_llm()
        if (round(time.time() - self.token_start_time) // 60) > 30:
                self.__token = self.get_token()
                self.token_start_time = time.time()
        self.model_params["messages"][0]["content"] = prompt
        response = requests.post(
            self.req_url,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {self.__token}"
            },
            data=json.dumps(self.model_params),
            verify=False
        )
        answer = response.json()
        return answer["choices"][0]["message"]["content"]