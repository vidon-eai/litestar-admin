import base64
import re
from pathlib import Path

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.types.doc import ImageRefMode
from langchain_core.documents import Document
from langchain_docling.loader import DoclingLoader, ExportType
from langchain_text_splitters import MarkdownHeaderTextSplitter

EXPORT_TYPE = ExportType.MARKDOWN
IMAGE_RESOLUTION_SCALE = 1


class DoclingParser:
    def __init__(self, file_path: str):
        pipeline_options = PdfPipelineOptions(
            images_scale=IMAGE_RESOLUTION_SCALE, generate_picture_images=True
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

    def load_documents(self) -> list[Document]:
        return self._loader.load()

    def extract_base64_images(self, documents: list[Document]) -> list[dict]:
        pattern = r"!\[(?P<alt>[^\]]*)\]\((?P<data_uri>data:image/(?P<format>[a-zA-Z0-9\+\.-]+);base64,(?P<base64_data>[A-Za-z0-9+/=]+))\)"
        matches = []

        for doc in documents:
            for match in re.finditer(pattern, doc.page_content):
                data_uri = match.group("data_uri")
                if "," in data_uri:
                    base64_str = data_uri.split(",", 1)[1]
                else:
                    base64_str = data_uri
                matches.append(
                    {
                        "alt": match.group("alt"),  # 圖片替代文字
                        "format": match.group(
                            "format"
                        ),  # 圖片格式 (例如: png, jpeg, webp)
                        "data_uri": base64.b64decode(
                            base64_str
                        ),  # 完整的 Data URI 標籤
                        "base64_data": match.group("base64_data"),  #
                    }
                )

        return matches

    def parse(self, documents: list[Document]):
        splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "Header_1"),
                ("##", "Header_2"),
                ("###", "Header_3"),
            ],
        )
        splits = [
            split
            for doc in documents
            for split in splitter.split_text(doc.page_content)
        ]

        return splits

    def _replacer(self, match):
        alt_text = match.group(1)
        img_type = match.group(2)
        base64_str = match.group(3)

        # 解碼並保存
        img_data = base64.b64decode(base64_str)

        # 判斷格式
        if img_data[:2] == b"\x89P":
            ext = "png"
        elif img_data[:2] == b"\xff\xd8":
            ext = "jpg"
        else:
            ext = img_type

        filename = f"image_{self._replacer.counter}.{ext}"
        filepath = Path("storage", "uuid", filename)
        self._replacer.counter += 1
        return f"![{alt_text}]({filepath})"


# parser = DoclingParser(file_path="../../../storage/c4611_sample_explain.pdf")
# documents = parser.load_documents()

# if EXPORT_TYPE == ExportType.DOC_CHUNKS:
#     splits = documents
# elif EXPORT_TYPE == ExportType.MARKDOWN:
#     from langchain_text_splitters import MarkdownHeaderTextSplitter

#     splitter = MarkdownHeaderTextSplitter(
#         headers_to_split_on=[
#             ("#", "Header_1"),
#             ("##", "Header_2"),
#             ("###", "Header_3"),
#         ],
#     )
#     splits = [
#         split for doc in documents for split in splitter.split_text(doc.page_content)
#     ]

# pattern = r"!\[(.*?)\]\(data:image/([^;]+);base64,([^)]+)\)"


# def replacer(match):
#     alt_text = match.group(1)
#     img_type = match.group(2)
#     base64_str = match.group(3)

#     # 解碼並保存
#     img_data = base64.b64decode(base64_str)

#     # 判斷格式
#     if img_data[:2] == b"\x89P":
#         ext = "png"
#     elif img_data[:2] == b"\xff\xd8":
#         ext = "jpg"
#     else:
#         ext = img_type

#     filename = f"image_{replacer.counter}.{ext}"
#     filepath = Path("storage", "uuid", filename)
#     replacer.counter += 1
#     return f"![{alt_text}]({filepath})"


# replacer.counter = 1
# for doc in documents:
#     doc.page_content = re.sub(pattern, replacer, doc.page_content)


# splitter = MarkdownHeaderTextSplitter(
#     headers_to_split_on=[
#         ("#", "Header_1"),
#         ("##", "Header_2"),
#         ("###", "Header_3"),
#     ],
# )
# splits = [split for doc in documents for split in splitter.split_text(doc.page_content)]

# for doc in splits:
#     print("------------------------")
#     print(doc.page_content)
