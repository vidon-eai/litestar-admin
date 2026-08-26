from app.plugins.rag.parsing.loader_factory import Loader


class ParserService:
    def __init__(self):
        self._loader = Loader()

    def parse(self, source_path: str):
        return self._loader.parse(source_path)
