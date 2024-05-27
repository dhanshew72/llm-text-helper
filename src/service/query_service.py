from langchain_community.vectorstores import DeepLake
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
import const


class QueryService:

    def __init__(self, user):
        self.user = user

    def answer(self, question):
        embeddings = OpenAIEmbeddings()
        db = DeepLake(
            dataset_path="./data/{}".format(self.user),
            embedding=embeddings,
            read_only=True,
            token=const.CREDENTIALS["DEEPLAKE_TOKEN"]
        )
        qa = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(model="gpt-3.5-turbo"),
            retriever=db.as_retriever(),
        )
        return qa.run(question)
