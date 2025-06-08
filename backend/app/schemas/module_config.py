# backend/app/core/schemas/module_config.py
from pydantic import BaseModel
from typing import List, Optional

class ModuleConfig(BaseModel):
    """
    Represents the configuration for a single module
    as defined in modules.yaml.
    """
    name: str
    path: str
    version: str
    description: Optional[str] = None
    enabled: bool
    router_variable_name: str
    prefix: str
    tags: List[str]

class ModulesFile(BaseModel):
    """
    Represents the root structure of the modules.yaml file.
    """
    modules: List[ModuleConfig]