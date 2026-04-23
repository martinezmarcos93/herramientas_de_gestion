"""
Configuración central del Tablero de Control
"""
import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

DEFAULTS = {
    "ruta_base": r"H:\Mi unidad\00-Analista Contable\00-Clientes",
    "honorario_base": 25475.00,
    "honorario_base_mes": "2025-07",
    "meses_inactividad": 12,
    "carpetas_cliente_default": [
        "Documentos",
        "Constancias y credenciales",
        "Facturacion"
    ]
}

def cargar():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Merge con defaults para keys nuevas
            for k, v in DEFAULTS.items():
                if k not in data:
                    data[k] = v
            return data
    return DEFAULTS.copy()

def guardar(config: dict):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
