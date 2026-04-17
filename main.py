import os
from litestar import Litestar, Router
from litestar.openapi.config import OpenAPIConfig


async def on_startup(app: Litestar) -> None:
    from src.core.logger import log

    sorted_routes = app.route_handler_method_map.items()
    for route_path, method_map in sorted_routes:

        if route_path == "/api/v1/schema" or route_path.startswith("/api/v1/schema"):
            continue

        for http_method, handler in method_map.items():
            if http_method == "OPTIONS":
                continue
            controller_part, handler_name = str(handler).rsplit(".", 1)
            controller_name = controller_part.rsplit(".", 1)[-1]
            log.info(
                f"[{http_method:<6}] {route_path:<35} - {controller_name}:{handler_name}"
            )


def create_app() -> Litestar:
    from src.core.logger import setup_logging
    from src.api.register_routers import register_routers

    setup_logging()
    system_routers = register_routers()
    plugin_routers = register_routers("plugins")
    os.environ["ENVIRONMENT"] = "dev"
    
    from src.config.setting import get_settings
    settings = get_settings()
    get_settings.cache_clear()
    
    
    print(settings.environment)

    return Litestar(
        path=settings.root_path,
        route_handlers=[
            *system_routers,
            Router(path="/plugins", route_handlers=plugin_routers),
        ],
        openapi_config=OpenAPIConfig(
            title=settings.title,
            version=settings.version,
            description=settings.description,
            summary=settings.summary,
        ),
        on_startup=[on_startup],
    )


if __name__ == "__main__":
    
    
    import uvicorn
    from src.core.logger import setup_logging
    
    from src.config.setting import get_settings
    settings = get_settings()
    get_settings.cache_clear()

    setup_logging()
    uvicorn.run(
        "main:create_app",
        host=settings.server_host,
        port=settings.server_port,
        reload=settings.debug,
        factory=True,
        log_config=None,
    )
