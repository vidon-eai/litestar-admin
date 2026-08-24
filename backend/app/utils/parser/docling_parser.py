import base64
import re
from typing import Awaitable, Callable, Iterator

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.types.doc.base import ImageRefMode
from langchain_core.documents import Document
from langchain_docling.loader import DoclingLoader, ExportType
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
)

EXPORT_TYPE = ExportType.MARKDOWN
IMAGE_RESOLUTION_SCALE = 2


class DoclingParser:
    def __init__(self, file_path: str):
        pipeline_options = PdfPipelineOptions(
            images_scale=IMAGE_RESOLUTION_SCALE,
            generate_picture_images=True,
        )

        converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )

        self._loader = DoclingLoader(
            file_path=file_path,
            export_type=EXPORT_TYPE,
            converter=converter,
            md_export_kwargs={
                "image_mode": ImageRefMode.EMBEDDED,  # 導出為 Base64 內嵌圖片
            },
        )

        self._documents: list[Document] = []
        self._images: list[bytes] = []

    def load_documents(self) -> Iterator[Document]:
        return self._loader.lazy_load()

    async def extract_images(
        self,
        documents: list[Document],
        upload_fn: Callable[[bytes, str], Awaitable[str | None]] | None = None,
    ) -> list[dict]:
        """
        提取 Base64 圖片。如果傳入 upload_fn，则上传图片并直接替换 Document 中的图片路径。

        :param documents: Document 列表
        :param upload_fn: 异步回调函数，接收 (image_bytes, format_ext)，返回替换后的 URL 或文件 key
        :return: 提取/处理后的图片元数据列表
        """
        pattern = r"!\[(?P<alt>[^\]]*)\]\((?P<data_uri>data:image/(?P<format>[a-zA-Z0-9\+\.-]+);base64,(?P<base64_data>[A-Za-z0-9+/=]+))\)"
        extracted_images = []

        for doc in documents:
            # 记录需要替换的字符串 mapping: {原始 data_uri 文本: 新的 URL/路径}
            replacements = {}

            for match in re.finditer(pattern, doc.page_content):
                data_uri_str = match.group("data_uri")
                img_format = match.group("format")
                base64_str = match.group("base64_data")
                img_bytes = base64.b64decode(base64_str)

                new_src = None
                if upload_fn:
                    # 调用传入的上传函数上传图片，并获取新路径/URL
                    new_src = await upload_fn(img_bytes, img_format)
                    if new_src:
                        replacements[data_uri_str] = new_src

                extracted_images.append(
                    {
                        "alt": match.group("alt"),
                        "format": img_format,
                        "data_bytes": img_bytes,
                        "new_src": new_src,
                    }
                )

            # 替换当前文档中的 base64 路径为上传后的路径
            for old_uri, new_path in replacements.items():
                doc.page_content = doc.page_content.replace(old_uri, new_path)

        return extracted_images

    def parse(self, documents: list[Document], extra_metadata: dict | None = None):
        splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "Header_1"),
                ("##", "Header_2"),
                ("###", "Header_3"),
            ],
            strip_headers=False,
        )

        splits: list[Document] = []
        for doc in documents:
            # 進行切片
            doc_splits = splitter.split_text(doc.page_content)

            for split in doc_splits:
                # # 1. 保留原本 doc 的 metadata（如果有的话）
                split.metadata.update(doc.metadata)

                # 2. 注入外部傳入的額外 metadata（如 file_id）
                if extra_metadata:
                    split.metadata.update(extra_metadata)

                splits.append(split)

        return splits
