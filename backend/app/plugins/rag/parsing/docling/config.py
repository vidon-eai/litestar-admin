from dataclasses import dataclass, field

from langchain_docling.loader import ExportType


@dataclass(frozen=True)
class DoclingConfig:
    export_type: ExportType = ExportType.MARKDOWN
    chunk_size: int = 500
    chunk_overlap: int = 50
    headers_to_split_on: list[tuple[str, str]] = field(
        default_factory=lambda: [
            ("#", "Header_1"),
            ("##", "Header_2"),
            ("###", "Header_3"),
        ]
    )
