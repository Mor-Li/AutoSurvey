import time
import requests
import json
from tqdm import tqdm
import threading
import urllib3
import os
import hashlib
import re
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
        
        # 初始化缓存
        self.cache_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cache")
        os.makedirs(self.cache_dir, exist_ok=True)
        self.cache_file = os.path.join(self.cache_dir, f"{model}_cache.json")
        self.response_cache = self._load_cache()
        self.cache_hits = 0
        self.cache_misses = 0
        
    def _load_cache(self):
        """加载缓存文件"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载缓存文件失败: {str(e)}")
                return {}
        return {}
    
    def _save_cache(self):
        """保存缓存到文件"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.response_cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存缓存文件失败: {str(e)}")
    
    def _normalize_text(self, text):
        """标准化文本以忽略空白差异和大小写"""
        # 确保先转为字符串（防止接收到非字符串对象）
        text = str(text)
        # 移除多余空白并转为小写
        normalized = re.sub(r'\s+', ' ', text).strip().lower()
        # 打印用于调试
        # print(f"原始文本: '{text}'")
        # print(f"标准化后: '{normalized}'")
        return normalized
    
    def _get_text_hash(self, text):
        """计算文本的哈希值作为缓存键"""
        # 标准化后再计算哈希,确保空白差异不影响缓存
        normalized_text = self._normalize_text(text)
        hash_value = hashlib.md5(normalized_text.encode('utf-8')).hexdigest()
        # print(f"生成的哈希值: {hash_value}")
        return hash_value
        
    def __req(self, text, temperature, max_try = 5):
        # 检查缓存
        text_hash = self._get_text_hash(text)
        
        # 如果启用了相同temperature的缓存查找
        cache_key = f"{text_hash}_{temperature}"
        if cache_key in self.response_cache:
            self.cache_hits += 1
            print(f"Cache hit! Using cached response (hits: {self.cache_hits}, misses: {self.cache_misses})")
            return self.response_cache[cache_key]
            
        # 未命中缓存,调用API
        self.cache_misses += 1
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": text}
                ],
                temperature=temperature
            )
            response = completion.choices[0].message.content
            print(f"First try response successful")
            # 存入缓存
            self.response_cache[cache_key] = response
            # 每10次缓存未命中后保存一次缓存
            if self.cache_misses % 10 == 0:
                self._save_cache()
            return response
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
                    response = completion.choices[0].message.content
                    print(f"Retry {i+1} response successful")
                    # 存入缓存
                    self.response_cache[cache_key] = response
                    self._save_cache()
                    return response
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
            
        # 批处理完成后保存缓存
        self._save_cache()
        return res_l
    
    # 可选：退出时保存缓存
    def __del__(self):
        try:
            self._save_cache()
            print(f"Cache statistics - Hits: {self.cache_hits}, Misses: {self.cache_misses}")
        except:
            pass
    
