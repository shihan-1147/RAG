import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

# --- 最终的、混合式导入，基于你的文件系统 ---
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.embeddings.dashscope import DashScopeEmbeddings

# --- 修改点 1：为新的LCEL链导入必要的组件 ---
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


def main():
    # --- 1. 加载环境变量 ---
    load_dotenv()
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        print("错误：请在 .env 文件中设置你的 DASHSCOPE_API_KEY")
        return
    print("环境变量加载成功。")

    # --- 2. 加载和分割文档 ---
    pdf_path = "xiaomiYU7.pdf"
    if not os.path.exists(pdf_path):
        print(f"错误：找不到文件 {pdf_path}")
        return
    print(f"正在加载文档: {pdf_path}...")
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    print("文档加载完成。")

    print("正在将文档分割成块...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(pages)
    print(f"文档被分割成 {len(docs)} 个块。")

    # --- 3. 文本嵌入和存入向量数据库 ---
    print("正在创建文本嵌入并存入向量数据库...")
    embeddings = DashScopeEmbeddings(model="text-embedding-v2", dashscope_api_key=api_key)
    vector_store = FAISS.from_documents(docs, embeddings)
    print("向量数据库创建完成。")

    # --- 4. 创建问答链 (使用新的LCEL方式) ---
    print("正在创建问答链...")

    # 4.1 初始化检索器
    retriever = vector_store.as_retriever()

    # 4.2 初始化支持流式输出的模型
    llm = ChatTongyi(model_name="qwen-plus", dashscope_api_key=api_key, temperature=0, streaming=True)

    # 4.3 定义一个提示词模板，告诉模型如何利用上下文
    template = """
                请根据以下提供的上下文来回答问题。
                如果你在上下文中找不到答案，就根据你的知识库查找答案，不要试图编造答案。
                
                上下文:
                {context}
                
                问题:
                {question}
                
                答案:
                """
    prompt = ChatPromptTemplate.from_template(template)

    # 4.4 定义一个辅助函数，用于将检索到的文档列表格式化为单一字符串
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # 4.5 使用 LCEL "管道" ( | ) 将所有组件连接起来，构建新的RAG链
    rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )

    print("问答链创建成功！现在可以开始提问了。")

    # --- 5. 循环提问 (使用新的流式处理方式) ---
    while True:
        query = input("\n请输入你的问题 (输入 'exit' 或 '退出' 即可退出): ")
        if query.lower() == 'exit' or query == '退出':
            break
        print("正在思考...")
        try:
            # --- 修改点 2：直接遍历新的 rag_chain.stream() 的输出 ---
            # 它会逐字(或逐词)地返回模型生成的内容
            print("\n答案:")
            for chunk in rag_chain.stream(query):
                print(chunk, end="", flush=True)
            print()  # 在答案结束后换行
        except Exception as e:
            print(f"发生了一个错误: {e}")


if __name__ == "__main__":
    main()