# backend/app/api_router.py
from fastapi import APIRouter
from app.core.config import logger
from app.core.module_loader import load_modules_config, discover_module_routers

# Create the main API router - this router will be prefixed by /api from main.py
api_router = APIRouter()

# --- Dynamic Module Router Inclusion ---
# This section replaces the previous static imports and router inclusions.
logger.info("api_router.py: Attempting to load and include dynamic module routers...")
try:
    # Load module configurations from the YAML file (e.g., app/configs/modules.yaml)
    modules_configurations = load_modules_config()

    # Discover actual APIRouter instances based on the configurations
    # This returns a list of dicts: [{"router": APIRouter_instance, "prefix": "/prefix", "tags": ["Tag"], "name": "module_name"}, ...]
    discovered_routers_info = discover_module_routers(modules_configurations)

    if discovered_routers_info:
        logger.info(f"api_router.py: Found {len(discovered_routers_info)} module routers to include.")
        for router_info in discovered_routers_info:
            instance = router_info.get("router")
            prefix = router_info.get("prefix")
            tags = router_info.get("tags")
            name = router_info.get("name", "unknown") # Get module name for logging

            if instance and prefix and tags:
                api_router.include_router(instance, prefix=prefix, tags=tags)
                logger.info(f"api_router.py: Successfully included router for module '{name}' with prefix '{prefix}' and tags {tags}.")
            else:
                logger.warning(f"api_router.py: Skipping a module due to missing router instance, prefix, or tags. Module: {name}")
    else:
        logger.info("api_router.py: No dynamic module routers were discovered or loaded. Check modules.yaml and module implementations.")

except FileNotFoundError:
    logger.error("api_router.py: CRITICAL - modules.yaml not found. No dynamic modules will be loaded.")
except ValueError as ve:
    logger.error(f"api_router.py: CRITICAL - Error parsing modules.yaml or validating module configurations: {ve}. No dynamic modules will be loaded.")
except Exception as e:
    logger.error(f"api_router.py: CRITICAL - An unexpected error occurred during dynamic router inclusion: {e}", exc_info=True)
    # If this fails, the application might have no module-specific routes.

# Note: Core modules like Auth and Health are now also expected to be defined in modules.yaml
# and loaded dynamically. If any "always-on" static routes are needed, they could be added here,
# but the goal is to make everything modular.

# Example of a static route if needed (though ideally everything is a module):
# @api_router.get("/ping", tags=["API System"])
# async def ping():
#     return {"message": "pong from api_router"}

logger.info("api_router.py: Dynamic module router inclusion process complete.")