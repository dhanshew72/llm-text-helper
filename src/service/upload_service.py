from langchain_community.vectorstores import DeepLake
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

import const
from utils import pdf


class UploadService:

    def __init__(self, user, start, end):
        self.user = user
        self.start = start
        self.end = end

    def upload(self, file_path):
        text_path = self._convert_pdf(file_path)
        embeddings = OpenAIEmbeddings()
        loader = TextLoader(text_path)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)
        db = DeepLake(
            dataset_path="./data/{}".format(self.user),
            embedding=embeddings,
            overwrite=True,
            token=const.CREDENTIALS["DEEPLAKE_TOKEN"]
        )
        db.delete_dataset()
        db.add_documents(docs)

    def _convert_pdf(self, pdf_path):
        text_path = 'data/converted/{}.txt'.format(self.user)
        text = pdf.read(pdf_path, self.start, self.end)
        with open(text_path, 'w') as file:
            file.write(text)
        return text_path
