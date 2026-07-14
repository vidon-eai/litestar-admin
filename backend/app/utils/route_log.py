from app.core.logger import log
from litestar.config.app import AppConfig
from litestar.plugins import ReceiveRoutePlugin
from litestar.routes import BaseRoute, HTTPRoute


class RouteLoggerPlugin(ReceiveRoutePlugin):
    plugin_tag = "route_logger"

    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        log.info("🚀 [Plugin] RouteLoggerPlugin initialized")
        return app_config

    def receive_route(self, route: BaseRoute) -> None:
        if route.path.startswith("/api/v1/schema"):
            return

        if isinstance(route, HTTPRoute):
            for method, (route_handler, _) in route.route_handler_map.items():
                if method == "OPTIONS":
                    continue

                raw_id = route_handler.handler_id

                try:
                    clean_path = raw_id.split("::")[0]
                    parts = clean_path.split(".")
                    simplified_id = f"{parts[-2]}.{parts[-1]}"
                except (IndexError, AttributeError):
                    simplified_id = raw_id
                log.info(f"📍 {route.path:<35} | {method:<6} | {simplified_id}")
