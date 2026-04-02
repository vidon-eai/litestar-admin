from litestar import Litestar


async def on_startup(app: Litestar) -> None:
    from src.core.logger import log

    sorted_routes = sorted(app.route_handler_method_map.items())
    for route_path, method_map in sorted_routes:
        for http_method, handler in method_map.items():
            if http_method == "OPTIONS":
                continue
            controller_part, handler_name = str(handler).rsplit(".", 1)
            controller_name = controller_part.rsplit(".", 1)[-1]
            log.info(
                f"[{http_method:<7}] {route_path:<35} - {controller_name}:{handler_name}"
            )


def create_app() -> Litestar:
    from src.core.logger import setup_logging
    from src.api.register_routers import register_routers

    setup_logging()
    api_routers = register_routers()
    return Litestar(
        path="/api/v1",
        route_handlers=api_routers,
        on_startup=[on_startup],
        openapi_config=None,
    )


if __name__ == "__main__":
    import uvicorn
    from src.core.logger import setup_logging

    setup_logging()
    uvicorn.run(
        "main:create_app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        factory=True,
        log_config=None,
    )
