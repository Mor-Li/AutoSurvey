import os
import time
from src.model import APIModel

def test_cache():
    # 设置测试参数
    model = "gpt-4o"  # 替换为您的模型
    api_key = "sk-FQoAQv3CvhQEOPai4dBaBe7024C848D194F3B8110dE24eAf"  # 替换为您的API密钥
    api_url = "http://152.69.226.145:3000/v1/chat/completions"  # 替换为您的API URL
    
    # 初始化APIModel
    api_model = APIModel(model, api_key, api_url)
    
    print("=== 缓存功能测试 ===")
    
    # 测试场景1: 完全相同的请求
    print("\n测试1: 完全相同的请求")
    prompt1 = "解释什么是深度学习"
    
    print("第一次请求...")
    response1 = api_model.chat(prompt1, temperature=0.7)
    print(f"响应长度: {len(response1)} 字符")
    
    print("第二次完全相同的请求...")
    response2 = api_model.chat(prompt1, temperature=0.7)
    print(f"响应长度: {len(response2)} 字符")
    
    # 测试场景2: 带有空格差异的请求
    print("\n测试2: 带有空格差异的请求")
    prompt2 = "解释  什么  是  深度  学习  "
    
    print("发送带有额外空格的相似请求...")
    response3 = api_model.chat(prompt2, temperature=0.7)
    print(f"响应长度: {len(response3)} 字符")
    
    # 测试场景3: 大小写差异的请求
    print("\n测试3: 大小写差异的请求")
    prompt3 = "解释什么是DEEP LEARNING"
    
    print("发送大小写不同的相似请求...")
    response4 = api_model.chat(prompt3, temperature=0.7)
    print(f"响应长度: {len(response4)} 字符")
    
    # 测试场景4: 完全不同的请求
    print("\n测试4: 完全不同的请求")
    prompt4 = "解释什么是强化学习"
    
    print("发送完全不同的请求...")
    response5 = api_model.chat(prompt4, temperature=0.7)
    print(f"响应长度: {len(response5)} 字符")
    
    # 测试场景5: 温度参数不同
    print("\n测试5: 温度参数不同")
    
    print("发送相同的请求但温度不同...")
    response6 = api_model.chat(prompt1, temperature=1.0)
    print(f"响应长度: {len(response6)} 字符")
    
    # 检查缓存是否正确保存
    cache_file = api_model.cache_file
    if os.path.exists(cache_file):
        print(f"\n缓存文件已创建: {cache_file}")
        print(f"缓存文件大小: {os.path.getsize(cache_file)} 字节")
    else:
        print(f"\n警告: 缓存文件未创建: {cache_file}")
    
    # 打印统计信息
    print(f"\n缓存命中次数: {api_model.cache_hits}")
    print(f"缓存未命中次数: {api_model.cache_misses}")
    
    # 理论上，应该有2次命中（测试1的第二次请求和测试2的空格差异请求）
    expected_hits = 2
    if api_model.cache_hits >= expected_hits:
        print(f"\n✅ 测试通过! 至少有 {expected_hits} 次缓存命中")
    else:
        print(f"\n❌ 测试失败! 缓存命中次数少于预期的 {expected_hits} 次")

if __name__ == "__main__":
    test_cache()