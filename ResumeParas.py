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
import mysql.connector
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
from datetime import datetime

current_time = datetime.now()

formatted_date = current_time.strftime("%Y-%m-%d")

def resumeParas(path):
    os.environ["OPENAI_API_KEY"] = 'sk-***'
    loader = PyPDFLoader(path)
    document = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    split_docs = text_splitter.split_documents(document)
    embeddings = OpenAIEmbeddings()
    docsearch = Chroma.from_documents(split_docs, embeddings)
    qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.as_retriever(), return_source_documents=False)
    result = qa({"query": "下面的信息为求职者简历，获取这段信息里面关于名字的信息并返回出来，直接返回名字，多余信息不需要，格式为：答案"})
    name=result['result']
    result = qa({"query": "下面的信息为求职者简历，获取这段信息里面关于期望岗位的信息并返回出来，并返回他的期望岗位，只返回该岗位，不要返回多余的信息，格式为：答案"})
    post=result['result']
    result = qa({"query": "下面的信息为求职者简历，总结这段信息里面关于工作年限的信息，格式为：答案，例如：3"})
    experience_time=result['result']
    result = qa({"query": "下面的信息为求职者简历，总结这段信息里面关于求职者top3的技能，格式为：答案，例如：JAVA,SCALA,DATA"})
    top3_skill_name=result['result']
    result = qa({"query": "下面的信息为求职者简历，总结这段信息里面关于求职者的电话号码，格式为：答案，例如：15828389765"})
    phone=result['result']
    result = qa({"query": "下面的信息为求职者简历，总结这段信息里面关于求职者的性别，格式为：答案，例如：女"})
    gender=result['result']
    result = qa({"query": "下面的信息为求职者简历，总结这段信息里面关于求职者的情况并安装格式提取内容，并给出总结评价：姓名：value，性别：value,工作经验：value，教育水平：value，top3技能：value，期望薪资：value，总结评价：value"})
    summary=result['result']
    insertDB(name,phone,post,summary,gender,experience_time,top3_skill_name,path)


def insertDB(name,phone,post,summary,gender,experience_time,top3_skill_name,file):
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="resumes"
    )
    cursor = conn.cursor()
    with open(file, "rb") as file:
        file_data = file.read()
    sql = "INSERT INTO resume (full_name, phone_number, post, summary, gender, experience_time, top3_skill_name, file_data) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    data = (name,phone, post,
            summary, gender, experience_time,
            top3_skill_name,
            file_data)

    cursor.execute(sql, data)
    conn.commit()
    cursor.close()
    conn.close()
insertDB('John Doe','1234567890','Data Engineer', 'Experienced software engineer with a strong background in Python and Java.', 'Male', '5 years', 'Python, Java, SQL','C:\\Users\\harryhaojiajian\\funnyTools\\resume_managerment\\data\\300.pdf')
