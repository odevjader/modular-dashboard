import yaml
from typing import List, Optional, Dict, Any
import importlib
from app.schemas.module_config import ModulesFile # Added import
from fastapi import APIRouter
import os
from app.core.config import logger # Assuming logger is configured here

# Define the base path for modules relative to the app directory
APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # app/
STANDARD_MODULES_BASE_DIR = os.path.join(APP_DIR, "modules") # app/modules/
CORE_MODULES_BASE_DIR = os.path.join(APP_DIR, "core_modules") # app/core_modules/
CONFIG_DIR = os.path.join(APP_DIR, "config") # app/config/
MODULE_CONFIG_FILE = os.path.join(CONFIG_DIR, "modules.yaml") # <- This was already correct

# ModuleConfig and ModulesConfig classes are removed as per plan.
# Their definitions were here.
# Validator methods validate_module_path_structure and validate_version_format
# were part of ModuleConfig and are thus also removed.

def load_modules_config(config_path: str = MODULE_CONFIG_FILE) -> ModulesFile: # Return type changed
    logger.info(f"Attempting to load module configurations from: {config_path}")
    if not os.path.exists(config_path):
        logger.error(f"Module configuration file not found: {config_path}")
        # Return empty config instead of raising FileNotFoundError to allow app to start
        # if modules.yaml is optional or for testing. Error will be logged.
        return ModulesFile(modules=[]) # Changed to ModulesFile

    try:
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
        if not config_data or 'modules' not in config_data: # Ensure modules.yaml content is handled
            logger.warning(f"No modules defined or 'modules' key missing in {config_path}. Returning empty list.")
            return ModulesFile(modules=[]) # Changed to ModulesFile

        # Use the imported ModulesFile schema for parsing and validation
        parsed_config = ModulesFile(**config_data) # Changed to ModulesFile
        logger.info(f"Successfully loaded and validated {len(parsed_config.modules)} module configurations from {config_path}")
        return parsed_config
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML in {config_path}: {e}", exc_info=True)
        raise ValueError(f"Error parsing module configuration file: {e}")
    except Exception as e: # Catches Pydantic validation errors too
        logger.error(f"An unexpected error or validation error occurred while loading {config_path}: {e}", exc_info=True)
        raise


def discover_module_routers(modules_config: ModulesFile) -> List[Dict[str, Any]]: # Parameter type changed
    loaded_routers_info = []
    if not modules_config or not modules_config.modules:
        logger.info("No modules to discover routers from based on provided config.")
        return loaded_routers_info

    for module_conf in modules_config.modules:
        if not module_conf.enabled:
            logger.info(f"Module '{module_conf.name}' version '{module_conf.version}' is disabled. Skipping router discovery.")
            continue

        try:
            # module_conf.path is now like "modules.info.v1" or "core_modules.auth.v1"
            # This path is relative to 'app', so the import becomes "app.modules.info.v1.endpoints"
            full_module_import_path = f"app.{module_conf.path}.endpoints"

            logger.info(f"Attempting to import router from: {full_module_import_path} for module '{module_conf.name} (v{module_conf.version})'")

            module_spec = importlib.util.find_spec(full_module_import_path)
            if module_spec is None:
                logger.error(f"Module '{module_conf.name}': Could not find spec for {full_module_import_path}. Ensure the path in modules.yaml is correct and __init__.py files exist in all parent directories.")
                continue

            imported_module = importlib.import_module(full_module_import_path)

            router_instance = getattr(imported_module, module_conf.router_variable_name, None)

            if router_instance and isinstance(router_instance, APIRouter):
                # Use provided prefix/tags or generate defaults
                api_prefix = module_conf.prefix if module_conf.prefix is not None else f"/{module_conf.name}/{module_conf.version}"
                tags = module_conf.tags if module_conf.tags is not None else [module_conf.name.capitalize()]

                loaded_routers_info.append({
                    "router": router_instance,
                    "prefix": api_prefix,
                    "tags": tags,
                    "name": module_conf.name,
                    "version": module_conf.version
                })
                logger.info(f"Successfully discovered and loaded router for module '{module_conf.name} (v{module_conf.version})' with prefix '{api_prefix}'.")
            else:
                logger.warning(f"Module '{module_conf.name} (v{module_conf.version})': Router variable '{module_conf.router_variable_name}' not found or not an APIRouter instance in {full_module_import_path}.")

        except ImportError as e:
            logger.error(f"Module '{module_conf.name} (v{module_conf.version})': Failed to import module or router from {full_module_import_path}. Error: {e}", exc_info=True)
        except AttributeError as e:
            logger.error(f"Module '{module_conf.name} (v{module_conf.version})': Attribute error (e.g., router variable not found). Error: {e}", exc_info=True)
        except Exception as e:
            logger.error(f"Module '{module_conf.name} (v{module_conf.version})': An unexpected error occurred during router discovery. Error: {e}", exc_info=True)

    return loaded_routers_info


def load_and_register_modules(router: APIRouter):
    """
    Centralizes dynamic module loading and registration.
    Loads module configurations, discovers routers, and registers them with the main FastAPI router.
    """
    logger.info("Starting dynamic module loading and registration process.")

    try:
        # Step 1: Load modules configuration
        logger.info("Loading modules configuration...")
        modules_config = load_modules_config()
        if not modules_config.modules:
            logger.info("No modules configured in modules.yaml or the file is empty.")
            # No further action needed if no modules are configured.
            return

        # Step 2: Discover module routers
        logger.info("Discovering module routers based on configuration...")
        discovered_routers_info = discover_module_routers(modules_config)

        # Step 3: Register discovered routers
        if not discovered_routers_info:
            logger.info("No module routers were discovered or loaded. Check module configurations and ensure routers are correctly defined.")
            return

        loaded_count = 0
        skipped_count = 0
        for router_info in discovered_routers_info:
            instance = router_info.get("router") # Corrected key from 'instance' to 'router'
            prefix = router_info.get("prefix")
            tags = router_info.get("tags")
            name = router_info.get("name")
            version = router_info.get("version")

            if instance and prefix and tags: # Basic validation
                router.include_router(instance, prefix=prefix, tags=tags)
                logger.info(f"Successfully included router for module: '{name} (v{version})' with prefix '{prefix}'.")
                loaded_count += 1
            else:
                logger.warning(
                    f"Skipping module '{name} (v{version})' due to missing router instance, prefix, or tags. "
                    f"Instance: {'Found' if instance else 'Missing'}, "
                    f"Prefix: '{prefix if prefix else 'Missing'}', "
                    f"Tags: {'Found' if tags else 'Missing'}."
                )
                skipped_count += 1

        logger.info(f"Module router registration complete. Loaded: {loaded_count}, Skipped: {skipped_count}.")

    except FileNotFoundError:
        # This specific exception for modules.yaml is handled by load_modules_config,
        # which logs an error and returns an empty ModulesFile.
        # load_and_register_modules will then proceed to log "No modules configured..."
        logger.warning("Module configuration file (modules.yaml) not found. No modules will be loaded.")
    except ValueError as ve:
        # This can be raised by load_modules_config for YAML parsing errors or Pydantic validation errors.
        logger.error(f"Failed to load or register modules due to a value or validation error: {ve}", exc_info=True)
    except Exception as e:
        logger.error(f"An unexpected error occurred during module loading and registration: {e}", exc_info=True)
        # Depending on policy, you might want to re-raise or handle differently.

if __name__ == '__main__':
    # This test assumes it's run from the 'app' directory or that PYTHONPATH is set up.
    # For direct execution: python -m app.core.module_loader
    print(f"Attempting to run module_loader.py as a script from: {os.getcwd()}")
    print(f"APP_DIR resolved to: {APP_DIR}")
    print(f"STANDARD_MODULES_BASE_DIR resolved to: {STANDARD_MODULES_BASE_DIR}")
    print(f"CORE_MODULES_BASE_DIR resolved to: {CORE_MODULES_BASE_DIR}")
    print(f"CONFIG_DIR resolved to: {CONFIG_DIR}")
    print(f"MODULE_CONFIG_FILE resolved to: {MODULE_CONFIG_FILE}")

    if not os.path.exists(MODULE_CONFIG_FILE):
        print(f"CRITICAL: `modules.yaml` not found at expected location: {MODULE_CONFIG_FILE}")
        print("Please ensure it exists. This test might fail or use an empty config.")
    else:
        print(f"Found `modules.yaml` at {MODULE_CONFIG_FILE}")


    print("\nTesting load_modules_config...")
    try:
        # Test with explicit path for clarity if run from outside app/core
        # config_file_abs_path = os.path.join(APP_DIR, "configs", "modules.yaml")
        config = load_modules_config() # Uses MODULE_CONFIG_FILE default
        if config and config.modules:
            print(f"Loaded {len(config.modules)} module configurations.")
            for m in config.modules:
                print(f"  - Module: {m.name}, Path: {m.path}, Version: {m.version}, Enabled: {m.enabled}, Prefix: {m.prefix}")

            print("\nTesting discover_module_routers...")
            routers_info = discover_module_routers(config)
            if routers_info:
                print(f"Discovered {len(routers_info)} routers.")
                for r_info in routers_info:
                    print(f"  - Router for module: {r_info['name']} (v{r_info['version']}), Prefix: {r_info['prefix']}, Tags: {r_info['tags']}")
            else:
                print("No routers discovered (or all disabled/ errored).")
        elif config and not config.modules:
             print("Module config loaded, but no modules are defined in it.")
        else:
            print("No config loaded or config was empty.")

    except FileNotFoundError:
        # This case should ideally be handled by load_modules_config returning empty ModulesConfig
        print(f"CRITICAL FileNotFoundError: `modules.yaml` not found during test execution.")
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()
