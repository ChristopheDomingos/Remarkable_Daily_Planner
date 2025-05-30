# -*- coding: utf-8 -*-
# Remarkable Daily Planner
# Version 2.2
#
# Created by: Christophe Domingos
# Date: May 30, 2025
#
# Description: Handles loading of planner configuration from a YAML file.

import yaml
from pathlib import Path
from typing import Any, Dict

def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """
    Loads configuration settings from a YAML file.

    Args:
        config_path: Path to the configuration file. Defaults to "config.yaml"
                     expected in the project root.

    Returns:
        A dictionary containing the configuration settings.

    Raises:
        FileNotFoundError: If the configuration file is not found.
    """
    path = Path(config_path)
    if not path.exists():
        # This error helps identify if config.yaml is missing from project root
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)