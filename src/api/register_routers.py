from pathlib import Path
import importlib
from litestar import Controller
from src.core.logger import log


def register_routers() -> list[type[Controller]]:
    """Automatically load all Controller classes from src/modules/*/controller.py"""
    controllers = []
    registered_controller_ids: set[int] = set()  # 用來追蹤已註冊的路徑
    modules_path = Path(__file__).parent.parent / "modules"  # src/modules

    for module_dir in modules_path.iterdir():
        if module_dir.is_dir() and (module_dir / "controller.py").exists():
            module_name = f"src.modules.{module_dir.name}.controller"
            try:
                module = importlib.import_module(module_name)
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)

                    if (
                        isinstance(attr, type)
                        and issubclass(attr, Controller)
                        and attr != Controller
                        and attr.__module__ == module_name
                    ):
                        # 獲取 controller 的 path
                        controller_id = id(attr)

                        # 檢測路徑是否重複
                        if controller_id in registered_controller_ids:
                            log.warning(f"Duplicate controller found: {attr.__name__}")
                        else:
                            registered_controller_ids.add(controller_id)

                        controllers.append(attr)
                        log.info(
                            f"✅ Loaded controller: {attr.__name__} (path = {getattr(attr, 'path', 'None')})"
                        )

            except ImportError as e:
                # Log the error but continue loading other controllers
                log.warning(f"Failed to load controller from {module_name}: {e}")
        else:
            log.warning(f"Controller file not found: {module_dir / 'controller.py'}")
    log.info(f"✅ Loaded controllers: {(len(controllers))} controllers")

    return controllers
