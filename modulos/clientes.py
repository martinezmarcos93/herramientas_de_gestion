"""
Módulo C: Gestión de Clientes
Estructura de carpetas, nomenclatura y descarga AFIP
"""
import os
import re
from pathlib import Path
from datetime import datetime


# ─────────────────────────────────────────────
# 1. GENERADOR DE ESTRUCTURA NUEVO CLIENTE
# ─────────────────────────────────────────────
def crear_estructura_cliente(
    carpeta_base: str,
    nombre: str,
    cuit: str,
    subcarpetas: list[str]
) -> tuple[str, list[str]]:
    """
    Crea la carpeta del cliente y sus subcarpetas.
    Retorna (ruta_creada, lista_carpetas_creadas)
    """
    # Sanitizar nombre para carpeta
    nombre_limpio = nombre.strip().upper()
    carpeta_cliente = Path(carpeta_base) / nombre_limpio
    creadas = []

    try:
        carpeta_cliente.mkdir(parents=True, exist_ok=False)
        creadas.append(str(carpeta_cliente))
    except FileExistsError:
        raise FileExistsError(f"Ya existe una carpeta para '{nombre_limpio}'")

    for sub in subcarpetas:
        sub_path = carpeta_cliente / sub
        sub_path.mkdir(parents=True, exist_ok=True)
        creadas.append(str(sub_path))

    # Archivo de datos del cliente
    info_path = carpeta_cliente / "_datos_cliente.txt"
    with open(info_path, "w", encoding="utf-8") as f:
        f.write(f"Cliente: {nombre_limpio}\n")
        f.write(f"CUIT: {cuit}\n")
        f.write(f"Alta: {datetime.now().strftime('%d/%m/%Y')}\n")
    creadas.append(str(info_path))

    return str(carpeta_cliente), creadas

def listar_clientes(carpeta_base: str) -> list[dict]:
    """Lista todos los clientes en la carpeta base."""
    clientes = []
    base = Path(carpeta_base)
    if not base.exists():
        return clientes
    for d in sorted(base.iterdir()):
        if d.is_dir() and not d.name.startswith("_"):
            subcarpetas = [s.name for s in d.iterdir() if s.is_dir()]
            clientes.append({
                "nombre": d.name,
                "path": str(d),
                "subcarpetas": subcarpetas,
                "cantidad_archivos": sum(1 for _ in d.rglob("*") if _.is_file())
            })
    return clientes

def detectar_subcarpetas_existentes(carpeta_base: str) -> list[str]:
    """
    Escanea todos los clientes y devuelve las subcarpetas más comunes.
    Útil para sugerir el template de carpetas al crear un cliente nuevo.
    """
    conteo: dict[str, int] = {}
    base = Path(carpeta_base)
    if not base.exists():
        return []
    for cliente_dir in base.iterdir():
        if not cliente_dir.is_dir() or cliente_dir.name.startswith("_"):
            continue
        for sub in cliente_dir.iterdir():
            if sub.is_dir():
                conteo[sub.name] = conteo.get(sub.name, 0) + 1
    # Devolver ordenadas por frecuencia
    return [k for k, v in sorted(conteo.items(), key=lambda x: -x[1])]


# ─────────────────────────────────────────────
# 2. DETECTOR DE NOMBRES INCORRECTOS
# ─────────────────────────────────────────────
def validar_nombre_archivo(nombre: str, patron_regex: str) -> bool:
    """Valida si un nombre cumple el patrón."""
    return bool(re.match(patron_regex, nombre, re.IGNORECASE))

def detectar_nombres_incorrectos(
    carpeta: str,
    patron_regex: str,
    extensiones: list[str] = None,
    recursivo: bool = True
) -> list[dict]:
    """
    Escanea archivos y detecta los que no cumplen la nomenclatura.
    patron_regex: ej. r'^\\d{11}_\\d{8}_.*' para CUIT_FECHA_nombre
    """
    incorrectos = []
    iterador = Path(carpeta).rglob("*") if recursivo else Path(carpeta).iterdir()

    for f in iterador:
        if not f.is_file():
            continue
        if extensiones and f.suffix.lower() not in [e.lower() for e in extensiones]:
            continue
        if not validar_nombre_archivo(f.name, patron_regex):
            incorrectos.append({
                "path": str(f),
                "nombre": f.name,
                "carpeta": str(f.parent),
                "extension": f.suffix.lower()
            })
    return incorrectos


# ─────────────────────────────────────────────
# 3. DESCARGADOR AFIP/ARCA
# ─────────────────────────────────────────────
def obtener_instrucciones_afip() -> str:
    """
    Devuelve las instrucciones para la descarga de constancias AFIP.
    La descarga real requiere Selenium + clave fiscal del usuario,
    por eso se gestiona desde la interfaz con aviso al usuario.
    """
    return (
        "Para descargar constancias de AFIP/ARCA se requiere:\n"
        "1. CUIT del titular\n"
        "2. Clave fiscal nivel 2 o superior\n"
        "3. Selenium WebDriver (se instala automáticamente)\n\n"
        "El programa navegará a:\n"
        "- Constancia de inscripción: https://www.afip.gob.ar/constancia\n"
        "- Certificado fiscal: https://www.afip.gob.ar/cfc\n\n"
        "Los archivos se guardarán en:\n"
        "  Clientes/{nombre}/Constancias y credenciales/"
    )

def descargar_constancia_afip(
    cuit: str,
    clave: str,
    carpeta_destino: str,
    tipo: str = "inscripcion"
) -> tuple[bool, str]:
    """
    Placeholder para descarga real con Selenium.
    Requiere: pip install selenium webdriver-manager
    tipo: 'inscripcion' | 'certificado_fiscal'
    """
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        # Implementación real se agrega en la siguiente etapa
        return False, "Módulo Selenium disponible - implementación en próxima etapa"
    except ImportError:
        return False, "Selenium no instalado. Ejecute: pip install selenium webdriver-manager"
