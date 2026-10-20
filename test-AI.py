import tomllib
from openai import OpenAI

# 1. 读取 config.toml（注意这里是用 "rb" 二进制模式读取）
with open("config.toml", "rb") as f:
    config = tomllib.load(f)

# 2. 拿数据
ai_config = config.get("ai", {})
api_key = ai_config.get("api_key", "")
base_url = ai_config.get("base_url", "https://api.siliconflow.cn/v1")
model_name = ai_config.get("model", "XingChenAGI/Xing4.0-29B")

if not api_key or api_key == "sk-API":
    print("❌ 错误: config.toml 中的 api_key 还没填真实的 Key！")
    exit(1)

print(f"✅ 读取配置成功，当前模型: {model_name}")
print("正在请求模型，请稍候...")

client = OpenAI(api_key=api_key, base_url=base_url)

prompt = "题目：以下哪种行为在遇到火灾时是错误的？\nA. 用湿毛巾捂住口鼻\nB. 乘坐电梯快速逃生\nC. 弯腰低姿态前行\nD. 拨打119报警\n请直接输出正确选项的字母，不要输出其他解释。"

response = client.chat.completions.create(
    model=model_name,
    messages=[{"role": "user", "content": prompt}],
    max_tokens=2048,
    temperature=0.1
)

print("\n=== 正式输出内容 ===")
print(f"[{response.choices[0].message.content}]")

if hasattr(response.choices[0].message, 'reasoning_content') and response.choices[0].message.reasoning_content:
    print("\n=== 模型的思考过程 ===")
    print(response.choices[0].message.reasoning_content)