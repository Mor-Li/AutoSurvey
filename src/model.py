import time
import requests
import json
from tqdm import tqdm
import threading
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # 禁用不安全请求警告

class APIModel:

    def __init__(self, model, api_key, api_url) -> None:
        self.__api_key = api_key
        self.__api_url = api_url
        self.model = model
        # 初始化OpenAI客户端
        from openai import OpenAI
        self.client = OpenAI(api_key=self.__api_key, 
                             base_url=self.__api_url.rsplit('/chat/completions', 1)[0])
        
    def __req(self, text, temperature, max_try = 5):
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": text}
                ],
                temperature=temperature
            )
            print(f"First try response successful")
            return completion.choices[0].message.content
        except Exception as e:
            print(f"First try failed: {str(e)}")
            for i in range(max_try):
                try:
                    completion = self.client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {"role": "user", "content": text}
                        ],
                        temperature=temperature
                    )
                    print(f"Retry {i+1} response successful")
                    return completion.choices[0].message.content
                except Exception as e:
                    print(f"Retry {i+1} failed: {str(e)}")
                time.sleep(0.2)
            return None

    def chat(self, text, temperature=1):
        response = self.__req(text, temperature=temperature, max_try=5)
        if response is None:
            print(f"Warning: API call failed for text: {text[:100]}...")
            return ""  # 返回空字符串而不是 None
        return response

    def __chat(self, text, temperature, res_l, idx):
        
        response = self.__req(text, temperature=temperature)
        res_l[idx] = response
        return response
        
    def batch_chat(self, text_batch, temperature=0):
        # 不使用多线程，改为顺序请求
        res_l = []
        for i, text in enumerate(tqdm(text_batch)):
            print(f"Processing request {i+1}/{len(text_batch)}")
            response = self.chat(text, temperature)
            res_l.append(response)
            time.sleep(1.0)  # 请求间隔1秒
        return res_l