本地知识库问答机器人 (RAG) - 项目使用文档
1. 项目简介
本项目是一个基于检索增强生成 (RAG) 技术的智能问答机器人。它能够读取本地的 PDF 文档，将其作为知识库，并精准地回答用户基于该文档内容提出的问题。

为了直观地展示 RAG 技术的价值，项目中包含了两个版本：

main.py (RAG 版本): 一个功能完整的 RAG 应用，它会先从 PDF 中检索相关信息，然后再让大语言模型基于这些信息生成答案。这使得它能回答非常具体、细节化的问题，且不易产生幻觉。

main_no_rag.py (普通版本): 一个不使用 RAG 的普通大模型聊天程序。它仅依赖模型自身的预训练知识来回答问题，用于和 RAG 版本进行效果对比。

所有回答都支持流式输出，提供类似打字机的实时交互体验。

2. 技术栈
编程语言: Python 3.10

核心框架: LangChain

大语言模型: 阿里巴巴 通义千问 (Qwen-plus)

嵌入模型: 阿里巴巴 通义千问 (text-embedding-v2)

向量数据库: FAISS (Facebook AI Similarity Search) - 轻量级本地向量库

PDF 解析: PyPDFLoader

3. 项目文件结构
/your-project-folder
|-- main.py              # 核心代码：带RAG功能的版本
|-- main_no_rag.py       # 对比代码：不带RAG功能的版本
|-- xiaomiYU7.pdf        # 你的本地知识库文件（可替换）
|-- .env                 # 环境变量文件，用于存放API Key
|-- requirements.txt     # 项目依赖库
`-- README.md            # 本使用文档
4. 环境配置与安装
请严格按照以下步骤进行环境配置，以确保项目顺利运行。

第 1 步：准备工作
确保你的电脑已经安装了 Python 3.10。

确保你的电脑已经安装了 Conda (推荐使用 Miniconda)。

第 2 步：创建并激活 Conda 环境
为了不污染主环境，我们创建一个全新的、纯净的虚拟环境。

Bash

# 创建一个名为 rag_env 的新环境
conda create --name rag_env python=3.10 -y

# 激活这个新环境
conda activate rag_env
（激活后，你的终端行首应显示 (rag_env)）

第 3 步：安装项目依赖
在项目根目录下，创建一个名为 requirements.txt 的文件，并将以下内容复制进去：

Plaintext

langchain
langchain-community
dashscope
pypdf
faiss-cpu
python-dotenv
tiktoken
然后在终端中（确保 (rag_env) 已激活），运行以下命令来安装所有依赖：

Bash

pip install -r requirements.txt
第 4 步：配置 API Key
在项目根目录下，创建一个名为 .env 的文件。

打开 .env 文件，在里面写入你的通义千问 API Key，格式如下：

DASHSCOPE_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
请将 sk-xxxx... 替换为你自己的真实 Key。

第 5 步：准备知识库
将你想要作为知识库的 PDF 文件放入项目根目录，并将其重命名为 xiaomiYU7.pdf。你也可以使用其他 PDF 文件，只需相应地修改代码中的 pdf_path 变量即可。

5. 如何运行
确保你的终端已经激活了 rag_env 环境 (conda activate rag_env)。

运行 RAG 版本
在终端中执行：

Bash

python main.py
程序启动后，会首先加载和处理 PDF 文件，当看到 “问答链创建成功！现在可以开始提问了。” 的提示时，你就可以开始提问关于 PDF 内容的问题了。

运行普通版本（用于对比）
在终端中执行：

Bash

python main_no_rag.py
这个版本启动更快，因为它不需要处理 PDF。你可以直接向它提问。

6. RAG 效果对比演示
为了直观感受 RAG 的强大之处，请尝试以下对比：

准备一个只存在于 xiaomiYU7.pdf 中的细节问题。

例如：“请问小米YU7手机的保养建议第三条是什么？”

向 RAG 版本 (main.py) 提问。

它应该能够准确地从 PDF 中找到并给出答案。

向普通版本 (main_no_rag.py) 提出完全相同的问题。

它很可能会回答“我不知道”或编造一个错误的答案，因为它从未学习过这份文档的内容。

这个简单的对比实验能够清晰地展示 RAG 在基于私有数据进行精准问答方面的巨大优势。

7. 未来可扩展方向
构建Web界面: 使用 Streamlit 或 Gradio 为本项目创建一个简单的图形用户界面。

支持更多文档格式: 扩展 DocumentLoader 以支持如 .docx, .txt, .md 等更多格式。

更换组件: 尝试替换向量数据库为 ChromaDB，或更换不同的大语言模型。

优化RAG流程: 引入更高级的 RAG 技术，如查询改写 (Query Transformation)、重排 (Re-ranking) 等，以提升检索效果。