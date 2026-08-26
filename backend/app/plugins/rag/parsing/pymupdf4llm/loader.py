from pathlib import Path
from typing import Any

import pymupdf4llm
from app.plugins.rag.parsing.base_loader import BaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

from .config import PyMuPDF4LLMConfig


class PyMuPDF4LLMLoader(BaseLoader):
    def __init__(self, config: PyMuPDF4LLMConfig | None = None):
        self._config = config or PyMuPDF4LLMConfig()

        self._markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=self._config.headers_to_split_on,
            strip_headers=False,
        )
        self._text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self._config.chunk_size,
            chunk_overlap=self._config.chunk_overlap,
        )

    def parse(
        self, source_path: str | Path, extra_metadata: dict[str, Any] | None = None
    ) -> list[Document]:
        extra_metadata = extra_metadata or {}

        kwargs = {
            "header": self._config.header,
            "footer": self._config.footer,
            "write_images": self._config.write_images,
            "page_chunks": self._config.page_chunks,
            "image_format": self._config.image_format,
            "image_dpi": self._config.image_dpi,
        }

        chunks = pymupdf4llm.to_markdown(str(source_path), **kwargs)

        if self._config.page_chunks and isinstance(chunks, list):
            # 使用列表推導式提升效能並修正 Return 位置 Bug
            return [
                Document(
                    page_content=chunk["text"],
                    metadata={
                        **chunk.get("metadata", {}),
                        **extra_metadata,
                        **{"Header_1": ""},
                    },
                )
                for chunk in chunks
            ]

        # page_chunks=False 時，chunks 為 str 型態
        markdown_text = str(chunks)
        splits = self._markdown_splitter.split_text(markdown_text)
        documents = self._text_splitter.split_documents(splits)

        if extra_metadata:
            for doc in documents:
                doc.metadata.update(extra_metadata)

        return documents


class LoaderFactory:
    def init_loader(self) -> PyMuPDF4LLMLoader:
        return PyMuPDF4LLMLoader(config=PyMuPDF4LLMConfig())
