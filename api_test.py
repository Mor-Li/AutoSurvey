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
        
    def __req(self, text, temperature, max_try = 5):
        url = f"{self.__api_url}"
        pay_load_dict = {"model": f"{self.model}","messages": [{
                "role": "user",
                "content": f"{text}"}],
                "temperature": temperature}
        payload = json.dumps(pay_load_dict)
        headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {self.__api_key}',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
        }
        try:
            response = requests.request("POST", url, headers=headers, data=payload, verify=False, timeout=3)
            print(f"First try response: {response.status_code} - {response.text}")
            return json.loads(response.text)['choices'][0]['message']['content']
        except Exception as e:
            print(f"First try failed: {str(e)}")
            for i in range(max_try):
                try:
                    response = requests.request("POST", url, headers=headers, data=payload, verify=False, timeout=3)
                    print(f"Retry {i+1} response: {response.status_code} - {response.text}")
                    return json.loads(response.text)['choices'][0]['message']['content']
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
        max_threads=15 # limit max concurrent threads using model API
        res_l = ['No response'] * len(text_batch)
        thread_l = []
        for i, text in zip(range(len(text_batch)), text_batch):
            thread = threading.Thread(target=self.__chat, args=(text, temperature, res_l, i))
            thread_l.append(thread)
            thread.start()
            while len(thread_l) >= max_threads: 
                for t in thread_l:
                    if not t .is_alive():
                        thread_l.remove(t)
                time.sleep(0.3) # Short delay to avoid busy-waiting

        for thread in tqdm(thread_l):
            thread.join()
        return res_l



def test_api():
    # API配置
    model = "gpt-4o"
    api_key = "sk-I6AFhSv1Qodu8FBx15126145600f4220A7D4Cc69Ef4810F7"
    api_url = "http://152.69.226.145:3000/v1/chat/completions"
    
    # 创建API Model实例
    api_model = APIModel(model=model, api_key=api_key, api_url=api_url)
    
    # 测试简单对话
    test_message = "Hello, how are you?"
    print("\nSending test message:", test_message)
    response = api_model.chat(test_message)
    print("\nResponse:", response)

if __name__ == "__main__":
    test_api()