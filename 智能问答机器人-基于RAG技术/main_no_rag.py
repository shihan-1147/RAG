import os
from dotenv import load_dotenv

# --- 我们只需要导入聊天模型和LCEL相关的核心组件 ---
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def main():
    # --- 1. 加载环境变量 ---
    load_dotenv()
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        print("错误：请在 .env 文件中设置你的 DASHSCOPE_API_KEY")
        return
    print("环境变量加载成功。")
    print("--- 正在运行【无RAG】的普通大模型 ---")

    # --- 2. 创建一个简单的大模型问答链 ---
    print("正在创建问答链...")

    # 2.1 初始化支持流式输出的模型
    llm = ChatTongyi(model_name="qwen-plus", dashscope_api_key=api_key, temperature=0, streaming=True)

    # 2.2 定义一个非常简单的提示词模板，不包含任何外部上下文
    # 这里的模板只是为了给模型一个基本的角色定位
    template = """
你是一个问答机器人。请回答用户提出的问题。

问题: {question}
"""
    prompt = ChatPromptTemplate.from_template(template)

    # 2.3 使用 LCEL 构建一个极简的链： 提示 -> 模型 -> 输出解析
    simple_chain = prompt | llm | StrOutputParser()

    print("问答链创建成功！现在可以开始提问了。")

    # --- 3. 循环提问 ---
    while True:
        query = input("\n请输入你的问题 (输入 'exit' 或 '退出' 即可退出): ")
        if query.lower() == 'exit' or query == '退出':
            break
        print("正在思考...")
        try:
            print("\n答案:")
            for chunk in simple_chain.stream({"question": query}):
                print(chunk, end="", flush=True)
            print()  # 在答案结束后换行
        except Exception as e:
            print(f"发生了一个错误: {e}")


if __name__ == "__main__":
    main()