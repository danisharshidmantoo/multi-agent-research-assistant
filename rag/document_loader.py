from pathlib import Path

from langchain_community.document_loaders import (
    CSVLoader,
    DirectoryLoader,
    PyPDFLoader,
    TextLoader,
)


class DocumentLoader:
    def __init__(self, directory: str):
        self.directory = Path(directory)

    def load_documents(self):
        documents = []

        pdf_loader = DirectoryLoader(
            str(self.directory),
            glob="**/*.pdf",
            loader_cls=PyPDFLoader,
        )
        documents.extend(pdf_loader.load())

        txt_loader = DirectoryLoader(
            str(self.directory),
            glob="**/*.txt",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"},
        )
        documents.extend(txt_loader.load())

        csv_loader = DirectoryLoader(
            str(self.directory),
            glob="**/*.csv",
            loader_cls=CSVLoader,
            loader_kwargs={"encoding": "utf-8"},
        )
        documents.extend(csv_loader.load())

        return documents