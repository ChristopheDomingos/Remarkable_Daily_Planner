from __future__ import annotations
import os
import yaml
from typing import Dict, Any

DEFAULTS: Dict[str, Any] = {
    "margins": {"left": 10, "top": 15, "right": 10, "bottom": 15},
    "locale": "en_US",
    "quotes": {
        "path": "my_quotes.csv",
        "seed": 0
    }
}

MONTHS = {
    "en_US": ["", "January","February","March","April","May","June","July","August","September","October","November","December"],
    "pt_PT": ["", "Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"],
    "pl_PL": ["", "Styczeń","Luty","Marzec","Kwiecień","Maj","Czerwiec","Lipiec","Sierpień","Wrzesień","Październik","Listopad","Grudzień"],
}

def load_config(path: str | None) -> Dict[str, Any]:
    data: Dict[str, Any] = {}
    if path and os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    # shallow merge
    cfg = DEFAULTS.copy()
    for k, v in data.items():
        if isinstance(v, dict) and isinstance(cfg.get(k), dict):
            merged = cfg[k].copy()
            merged.update(v)
            cfg[k] = merged
        else:
            cfg[k] = v
    # sanity for margins
    m = cfg.get("margins", {})
    for key in ["left","top","right","bottom"]:
        if float(m.get(key, 0)) < 0:
            raise ValueError(f"Margin '{key}' must be >= 0")
    return cfg

def month_name(locale_code: str, month: int) -> str:
    table = MONTHS.get(locale_code, MONTHS["en_US"])
    return table[month]
