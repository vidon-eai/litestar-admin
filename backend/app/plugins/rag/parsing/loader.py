import pymupdf4llm
from langchain_core.documents import Document


class PyMuPDF4LLMLoader:
    def parse(self, source_path: str):
        args = {
            "header": False,
            "footer": False,
            "write_image": False,
            "page_chunks": True,
        }

        chunks = pymupdf4llm.to_markdown(source_path, **args)

        documents = []
        for chunk in chunks:
            # 结合原有的 chunk metadata 与自定义 metadata
            metadata = {
                **chunk["metadata"],  # 包含 page, total_pages, title 等
                "source": source_path,
                "filename": source_path,
            }

            doc = Document(page_content=chunk["text"], metadata=metadata)
            documents.append(doc)

        return documents
        # splitter = MarkdownHeaderTextSplitter(
        #     headers_to_split_on=[
        #         ("#", "Header_1"),
        #         ("##", "Header_2"),
        #         ("###", "Header_3"),
        #     ],
        #     strip_headers=False,
        # )

        # splits = splitter.split_text(str(md_text))
        # for d in splits:
        #     d.metadata["source"] = source_path
        #     d.metadata["filename"] = source_path
        # return splits
