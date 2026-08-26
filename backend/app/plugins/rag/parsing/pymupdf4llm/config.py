from dataclasses import dataclass, field


@dataclass(frozen=True)
class PyMuPDF4LLMConfig:
    header: bool = False
    footer: bool = False
    write_images: bool = False
    image_format: str = "png"
    image_dpi: int = 150
    page_chunks: bool = True
    chunk_size: int = 500
    chunk_overlap: int = 50
    headers_to_split_on: list[tuple[str, str]] = field(
        default_factory=lambda: [
            ("#", "Header_1"),
            ("##", "Header_2"),
            ("###", "Header_3"),
        ]
    )
