import requests
from .api_config import BERT_API_URL, RULE_API_URL, GEN_API_URL

def call_bert_model(file_path):
    """
    调用BERT模型API，输入pcap文件，输出研判结果
    """
    url = BERT_API_URL
    with open(file_path, "rb") as f:
        files = {"file": f}
        resp = requests.post(url, files=files, timeout=30)
        resp.raise_for_status()
        return resp.json()  # 假设返回 {"result": "xxx"}

def call_rule_tool(file_path):
    """
    调用规则提取工具API，输入pcap文件，输出规则
    """
    url = RULE_API_URL
    with open(file_path, "rb") as f:
        files = {"file": f}
        resp = requests.post(url, files=files, timeout=30)
        resp.raise_for_status()
        return resp.json()  # 假设返回 {"rules": [...]}

def call_gen_model(text):
    """
    调用生成式模型API，输入指令文本，输出pcap文件内容
    """
    url = GEN_API_URL
    data = {"text": text}
    resp = requests.post(url, json=data, timeout=30)
    resp.raise_for_status()
    return resp.content  # 返回pcap文件内容 