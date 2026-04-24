from pathlib import Path
import importlib
from litestar import Controller
from app.core.logger import log


def register_routers(module_dir: str = "modules") -> list[type[Controller]]:
    """
    Automatically load all Controller classes from the specified directory.

    Args:
        module_dir (str, optional): The directory to search for controllers. Defaults to "modules".

    Returns:
        list[type[Controller]]: A list of Controller classes.
    """
    controllers = []
    registered_controller_ids: set[int] = set()
    base_dir = Path(__file__).parent.parent
    try:
        log.info(f"🚀 Starting to search for controllers in [{module_dir}]")
        controller_files = list(base_dir.glob(f"{module_dir}/**/controller.py"))
        controller_files.sort()
        for file in controller_files:
            rel_path = file.relative_to(Path.cwd())
            path_parts = rel_path.parts
            module_path = f"{'.'.join(path_parts[:-1])}.controller"
            try:
                module = importlib.import_module(module_path)
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)

                    if (
                        isinstance(attr, type)
                        and issubclass(attr, Controller)
                        and attr != Controller
                        and attr.__module__ == module_path
                    ):
                        controller_id = id(attr)
                        if controller_id in registered_controller_ids:
                            log.warning(f"Duplicate controller found: {attr.__name__}")
                        else:
                            registered_controller_ids.add(controller_id)

                        controllers.append(attr)
                        log.info(
                            f"✅ Loaded controller: {attr.__name__} (path = {module_path})"
                        )

            except ImportError as e:
                log.warning(f"Failed to load controller from {module_path}: {e}")
        log.info(
            f"✅️ Registered {module_dir}: {len(registered_controller_ids)} controllers"
        )
    except Exception as e:
        log.error(f"Failed to find controller files: {e}")
        controller_files = []

    return controllers
