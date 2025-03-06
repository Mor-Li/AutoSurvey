import time
import requests
import json
import threading
import os
import urllib3
from tqdm import tqdm
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class APIModel:
    def __init__(self, model, api_key, api_url) -> None:
        self.__api_key = api_key
        self.__api_url = api_url
        self.model = model
        print(f"Initialized APIModel with: model={model}, api_url={api_url}")
    
    def __req(self, text, temperature, max_try=5):
        # 创建不使用环境代理的会话
        session = requests.Session()
        session.trust_env = False
        
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
        
        print(f"Sending request to: {url}")
        print(f"Headers: {headers}")
        print(f"Payload: {payload}")
        
        try:
            response = session.post(url, headers=headers, data=payload, verify=False, timeout=10)
            print(f"Response: {response.status_code} - {response.text[:200]}...")
            return json.loads(response.text)['choices'][0]['message']['content']
        except Exception as e:
            print(f"Request failed: {str(e)}")
            for i in range(max_try):
                try:
                    response = session.post(url, headers=headers, data=payload, verify=False, timeout=10)
                    print(f"Retry {i+1} response: {response.status_code} - {response.text[:200]}...")
                    return json.loads(response.text)['choices'][0]['message']['content']
                except Exception as e:
                    print(f"Retry {i+1} failed: {str(e)}")
                time.sleep(0.2)
            return None
    
    def chat(self, text, temperature=0):
        return self.__req(text, temperature)
    
    def __thread_req(self, text, temperature, results, idx):
        try:
            result = self.__req(text, temperature)
            results[idx] = result
        except Exception as e:
            print(f"Thread request failed: {str(e)}")
            results[idx] = None
    
    def batch_chat(self, text_batch, temperature=0):
        max_threads = 2  # 减少并发线程数，从15降到2
        res_l = ['No response'] * len(text_batch)
        thread_l = []
        
        for i, text in zip(range(len(text_batch)), text_batch):
            thread = threading.Thread(target=self.__chat, args=(text, temperature, res_l, i))
            thread_l.append(thread)
            thread.start()
            print(f"Started thread {i} for prompt")
            time.sleep(2.0)  # 增加线程启动间隔，给服务器更多恢复时间
            
            # 等待线程数量低于最大值
            while len([t for t in thread_l if t.is_alive()]) >= max_threads:
                time.sleep(1.0)  # 增加检查间隔
        
        # 等待所有线程完成
        for thread in tqdm(thread_l):
            thread.join()
        
        return res_l

def test_batch_chat():
    # 配置参数
    model = "gpt-4o"
    api_key = "sk-I6AFhSv1Qodu8FBx15126145600f4220A7D4Cc69Ef4810F7"
    api_url = "http://152.69.226.145:3000/v1/chat/completions"
    
    # 创建API Model实例
    api_model = APIModel(model=model, api_key=api_key, api_url=api_url)
    
    # 先测试单个请求
    print("\n===== Testing single chat request =====")
    response = api_model.chat("Hello, how are you?")
    print(f"Single chat response: {response}")
    
    # 测试批量请求
    print("\n===== Testing batch chat request =====")
    prompts = [
        "What is artificial intelligence?",
        "Explain machine learning in simple terms.",
        "What are the applications of deep learning?",
        "How does natural language processing work?"
    ]
    
    responses = api_model.batch_chat(prompts)
    
    print("\n===== Batch Chat Results =====")
    for i, response in enumerate(responses):
        print(f"\nPrompt {i+1}: {prompts[i][:50]}...")
        print(f"Response: {response[:200]}..." if response else "No response")

if __name__ == "__main__":
    # 禁用所有代理
    os.environ['http_proxy'] = ''
    os.environ['https_proxy'] = ''
    os.environ['HTTP_PROXY'] = ''
    os.environ['HTTPS_PROXY'] = ''
    os.environ['no_proxy'] = '*'
    os.environ['NO_PROXY'] = '*'
    
    print("Environment proxy settings:")
    for key in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'no_proxy', 'NO_PROXY']:
        print(f"{key}: {os.environ.get(key, 'Not set')}")
    
    test_batch_chat()