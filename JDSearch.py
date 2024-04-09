from langchain.document_loaders import UnstructuredFileLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import OpenAI
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.chains import RetrievalQA
import logging
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
import getpass
import os

os.environ["OPENAI_API_KEY"] = getpass.getpass()

text="""
**Java 开发工程师**

**职位描述：**
我们正在寻找一名热情、有经验的 Java 开发工程师，负责开发和维护我们的软件产品。该职位需要具备扎实的 Java 编程技能、良好的沟通能力和团队合作精神。候选人应具备扎实的软件开发经验，能够快速学习新技术，并将其应用到我们的项目中。

**岗位职责：**
- 设计、开发和维护高质量的 Java 后端代码，满足项目需求。
- 参与需求分析、技术方案设计和代码评审。
- 协助团队解决技术难题和系统故障。
- 与产品团队和其他开发人员密切合作，确保项目按时交付，并达到高质量标准。
- 参与制定和执行测试计划，确保软件的稳定性和性能。

**任职要求：**
- 本科及以上学历，计算机相关专业优先。
- 3年以上 Java 后端开发经验，熟悉常用的 Java 开发框架（如 Spring、Spring Boot）。
- 熟悉数据库设计和 SQL 查询语言。
- 具备良好的数据结构和算法基础。
- 良好的沟通能力和团队合作精神，能够与团队成员有效地沟通和协作。
- 对新技术和开发方法有浓厚的兴趣，能够快速学习和应用新知识。

**加分项：**
- 熟悉微服务架构和分布式系统设计。
- 熟悉前端开发技术（如 HTML、CSS、JavaScript）。
- 有大型互联网公司工作经验者优先考虑。
- 具备云计算和容器化技术经验（如 Docker、Kubernetes）。

**工作地点：** 北京市海淀区

**薪资待遇：** 月薪 20,000 - 30,000 元，具体待遇面议。

**福利待遇：**
- 五险一金
- 弹性工作制
- 年度调薪
- 健康体检
- 周年旅游
"""
def JDParas(text):

    db = SQLDatabase.from_uri("mysql+pymysql://root:root@127.0.0.1/chinook")
    llm = OpenAI(temperature=0)
    db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)
    result=db_chain.run('这段文字是一个简历的JD:'+text+'.请根据这个JD，解析出工作年限需求，岗位需求，性别需求，技能需求，分别与表resume的experience_time，post，gender，top3_skill_name 匹配，如果JD里面没有明确要求则不需要硬匹配，并返回合适的名字，输出格式：full_name:{value},experience_time：{value},top3_skill_name:{value}')
    print(result)
JDParas(text)
