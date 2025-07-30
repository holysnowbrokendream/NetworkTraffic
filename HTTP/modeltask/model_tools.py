import requests
from .api_config import BERT_API_URL, RULE_API_URL, GEN_API_URL

def call_bert_model(file_path):
    """
    调用BERT模型API，输入pcap文件，输出研判结果
    """
    url = BERT_API_URL
    try:
        with open(file_path, "rb") as f:
            files = {"file": f}
            resp = requests.post(url, files=files, timeout=30)
            resp.raise_for_status()
            return resp.json()  # 假设返回 {"result": "xxx"}
    except requests.exceptions.ConnectionError:
        return {"error": "模型服务未启动", "result": "模型服务暂时不可用，请稍后重试"}
    except Exception as e:
        return {"error": f"模型调用失败: {str(e)}", "result": "模型服务出现错误，请稍后重试"}

def call_rule_tool(file_path):
    """
    调用规则提取工具API，输入pcap文件，输出规则
    """
    url = RULE_API_URL
    try:
        with open(file_path, "rb") as f:
            files = {"file": f}
            resp = requests.post(url, files=files, timeout=30)
            resp.raise_for_status()
            return resp.json()  # 假设返回 {"rules": [...]}
    except requests.exceptions.ConnectionError:
        return {"error": "模型服务未启动", "rules": ["模型服务暂时不可用，请稍后重试"]}
    except Exception as e:
        return {"error": f"模型调用失败: {str(e)}", "rules": ["模型服务出现错误，请稍后重试"]}

def call_gen_model(text):
    """
    调用生成式模型API，输入指令文本，输出pcap文件内容
    """
    url = GEN_API_URL
    try:
        data = {"text": text}
        resp = requests.post(url, json=data, timeout=30)
        resp.raise_for_status()
        return resp.content  # 返回pcap文件内容
    except requests.exceptions.ConnectionError:
        # 返回一个简单的错误信息作为pcap内容
        error_content = b"Model service not started, please try again later"
        return error_content
    except Exception as e:
        error_content = f"Model service error: {str(e)}".encode('utf-8')
        return error_content 