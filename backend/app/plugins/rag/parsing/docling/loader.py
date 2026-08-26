from typing import Any

from app.plugins.rag.parsing.base_loader import BaseLoader
from langchain_core.documents import Document
from langchain_docling.loader import DoclingLoader as Loader
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

from .config import DoclingConfig


class DoclingLoader(BaseLoader):
    def __init__(self, config: DoclingConfig | None = None):
        self._config = config or DoclingConfig()

        self._markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=self._config.headers_to_split_on,
            strip_headers=False,
        )
        self._text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self._config.chunk_size,
            chunk_overlap=self._config.chunk_overlap,
        )

    def parse(
        self, source_path: str, extra_metadata: dict[str, Any] | None = None
    ) -> list[Document]:

        loader = Loader(
            file_path=source_path,
            export_type=self._config.export_type,
        )

        chunks = loader.load()
        splits = [
            split
            for doc in chunks
            for split in self._markdown_splitter.split_text(doc.page_content)
        ]
        documents = self._text_splitter.split_documents(splits)

        for doc in documents:
            doc.metadata.update({"Header_1": ""})
            if extra_metadata:
                doc.metadata.update(extra_metadata)

        return documents


class LoaderFactory:
    def init_loader(self) -> DoclingLoader:
        return DoclingLoader(config=DoclingConfig())
