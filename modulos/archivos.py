"""
Módulo A: Archivos y Carpetas
Herramientas de gestión masiva del sistema de archivos
"""
import os
import hashlib
import shutil
import subprocess
import platform
from datetime import datetime, timedelta
from pathlib import Path


# ─────────────────────────────────────────────
# 1. IMPRESIÓN MASIVA POR ORDEN
# ─────────────────────────────────────────────
EXTENSIONES_IMPRIMIBLES = {".pdf", ".xlsx", ".xls", ".docx", ".doc"}

def listar_archivos_imprimibles(carpeta: str, orden: str = "nombre") -> list[dict]:
    """
    Devuelve archivos imprimibles de una carpeta ordenados.
    orden: 'nombre' | 'fecha_creacion' | 'fecha_modificacion'
    """
    archivos = []
    for f in Path(carpeta).iterdir():
        if f.is_file() and f.suffix.lower() in EXTENSIONES_IMPRIMIBLES:
            stat = f.stat()
            archivos.append({
                "path": str(f),
                "nombre": f.name,
                "extension": f.suffix.lower(),
                "fecha_creacion": datetime.fromtimestamp(stat.st_ctime),
                "fecha_modificacion": datetime.fromtimestamp(stat.st_mtime),
                "seleccionado": True
            })

    key_map = {
        "nombre": lambda x: x["nombre"].lower(),
        "fecha_creacion": lambda x: x["fecha_creacion"],
        "fecha_modificacion": lambda x: x["fecha_modificacion"],
    }
    archivos.sort(key=key_map.get(orden, key_map["nombre"]))
    return archivos

def imprimir_archivos(archivos: list[dict], impresora: str = None) -> tuple[int, list[str]]:
    """
    Imprime los archivos seleccionados en orden.
    Retorna (cantidad_impresos, errores)
    """
    impresos = 0
    errores = []
    for item in archivos:
        if not item.get("seleccionado", True):
            continue
        path = item["path"]
        try:
            if platform.system() == "Windows":
                if impresora:
                    os.startfile(path, "printto")
                else:
                    os.startfile(path, "print")
            impresos += 1
        except Exception as e:
            errores.append(f"{item['nombre']}: {e}")
    return impresos, errores


# ─────────────────────────────────────────────
# 2. RENOMBRADO AUTOMÁTICO
# ─────────────────────────────────────────────
def previsualizar_renombrado(carpeta: str, extension: str, patron: str) -> list[dict]:
    """
    Previsualiza cómo quedarían los archivos renombrados.
    patron: string con variables {nombre}, {fecha}, {fecha_mod}, {contador}
    Retorna lista de {original, nuevo, path}
    """
    ext = extension.lower().strip()
    if not ext.startswith("."):
        ext = "." + ext

    archivos = sorted([
        f for f in Path(carpeta).iterdir()
        if f.is_file() and f.suffix.lower() == ext
    ], key=lambda x: x.name.lower())

    resultado = []
    for i, f in enumerate(archivos, 1):
        stat = f.stat()
        fecha_mod = datetime.fromtimestamp(stat.st_mtime).strftime("%Y%m%d")
        fecha_hoy = datetime.now().strftime("%Y%m%d")
        nombre_sin_ext = f.stem

        nuevo_nombre = patron
        nuevo_nombre = nuevo_nombre.replace("{nombre}", nombre_sin_ext)
        nuevo_nombre = nuevo_nombre.replace("{fecha}", fecha_hoy)
        nuevo_nombre = nuevo_nombre.replace("{fecha_mod}", fecha_mod)
        nuevo_nombre = nuevo_nombre.replace("{contador}", str(i).zfill(3))
        nuevo_nombre = nuevo_nombre.replace("{extension}", ext)

        if not nuevo_nombre.endswith(ext):
            nuevo_nombre += ext

        resultado.append({
            "path": str(f),
            "original": f.name,
            "nuevo": nuevo_nombre,
            "conflicto": (Path(carpeta) / nuevo_nombre).exists() and nuevo_nombre != f.name
        })
    return resultado

def ejecutar_renombrado(previsualizacion: list[dict]) -> tuple[int, list[str]]:
    renombrados = 0
    errores = []
    for item in previsualizacion:
        if item.get("conflicto"):
            errores.append(f"Conflicto: {item['original']} → {item['nuevo']}")
            continue
        try:
            p = Path(item["path"])
            p.rename(p.parent / item["nuevo"])
            renombrados += 1
        except Exception as e:
            errores.append(f"{item['original']}: {e}")
    return renombrados, errores

def listar_archivos_a_txt(carpeta: str, destino_txt: str, recursivo: bool = False) -> int:
    """Genera un .txt con la lista de archivos de una carpeta."""
    lineas = []
    if recursivo:
        for root, dirs, files in os.walk(carpeta):
            dirs.sort()
            for f in sorted(files):
                rel = os.path.relpath(os.path.join(root, f), carpeta)
                lineas.append(rel)
    else:
        lineas = sorted([
            f.name for f in Path(carpeta).iterdir() if f.is_file()
        ])

    with open(destino_txt, "w", encoding="utf-8") as fh:
        fh.write(f"Listado de: {carpeta}\n")
        fh.write(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        fh.write(f"Total: {len(lineas)} archivos\n")
        fh.write("─" * 60 + "\n")
        for l in lineas:
            fh.write(l + "\n")
    return len(lineas)


# ─────────────────────────────────────────────
# 3. ORGANIZADOR ANUAL (mueve a HISTORICO)
# ─────────────────────────────────────────────
def escanear_para_historico(carpeta_clientes: str, meses_inactividad: int) -> list[dict]:
    """
    Escanea todas las carpetas de clientes y detecta archivos
    no modificados hace más de X meses.
    Retorna lista con path, cliente, año destino, etc.
    """
    limite = datetime.now() - timedelta(days=meses_inactividad * 30)
    candidatos = []

    base = Path(carpeta_clientes)
    for cliente_dir in sorted(base.iterdir()):
        if not cliente_dir.is_dir() or cliente_dir.name.startswith("_"):
            continue
        for f in cliente_dir.rglob("*"):
            if not f.is_file():
                continue
            # No tocar archivos que ya están en _HISTORICO
            if "_HISTORICO" in str(f):
                continue
            stat = f.stat()
            fecha_mod = datetime.fromtimestamp(stat.st_mtime)
            if fecha_mod < limite:
                año_destino = str(fecha_mod.year)
                candidatos.append({
                    "path": str(f),
                    "nombre": f.name,
                    "cliente": cliente_dir.name,
                    "fecha_mod": fecha_mod,
                    "año_destino": año_destino,
                    "seleccionado": True
                })
    return candidatos

def mover_a_historico(candidatos: list[dict], carpeta_clientes: str) -> tuple[int, list[str]]:
    """
    Mueve los archivos seleccionados a:
    carpeta_clientes/_HISTORICO/{año}/{cliente}/archivo
    """
    movidos = 0
    errores = []
    base = Path(carpeta_clientes)

    for item in candidatos:
        if not item.get("seleccionado", True):
            continue
        destino_dir = base / "_HISTORICO" / item["año_destino"] / item["cliente"]
        destino_dir.mkdir(parents=True, exist_ok=True)
        destino = destino_dir / item["nombre"]

        # Evitar colisiones: agregar sufijo si ya existe
        if destino.exists():
            stem = Path(item["nombre"]).stem
            suffix = Path(item["nombre"]).suffix
            ts = datetime.now().strftime("%H%M%S")
            destino = destino_dir / f"{stem}_{ts}{suffix}"
        try:
            shutil.move(item["path"], str(destino))
            movidos += 1
        except Exception as e:
            errores.append(f"{item['nombre']}: {e}")
    return movidos, errores


# ─────────────────────────────────────────────
# 4. DETECTOR DE DUPLICADOS
# ─────────────────────────────────────────────
def calcular_hash(path: str, chunk: int = 8192) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        while bloque := f.read(chunk):
            h.update(bloque)
    return h.hexdigest()

def detectar_duplicados(carpeta: str, recursivo: bool = True) -> list[list[dict]]:
    """
    Escanea y agrupa archivos con el mismo hash MD5.
    Retorna lista de grupos, cada grupo = lista de archivos idénticos.
    """
    hashes: dict[str, list] = {}
    iterador = Path(carpeta).rglob("*") if recursivo else Path(carpeta).iterdir()

    for f in iterador:
        if not f.is_file():
            continue
        try:
            h = calcular_hash(str(f))
            stat = f.stat()
            if h not in hashes:
                hashes[h] = []
            hashes[h].append({
                "path": str(f),
                "nombre": f.name,
                "tamaño": stat.st_size,
                "fecha_mod": datetime.fromtimestamp(stat.st_mtime),
                "hash": h
            })
        except Exception:
            continue

    return [grupo for grupo in hashes.values() if len(grupo) > 1]

def eliminar_duplicados(grupos: list[list[dict]], mantener: str = "primero") -> tuple[int, list[str]]:
    """
    Elimina duplicados de cada grupo, manteniendo el primero o el último.
    """
    eliminados = 0
    errores = []
    for grupo in grupos:
        a_eliminar = grupo[1:] if mantener == "primero" else grupo[:-1]
        for item in a_eliminar:
            if not item.get("eliminar", True):
                continue
            try:
                os.remove(item["path"])
                eliminados += 1
            except Exception as e:
                errores.append(f"{item['nombre']}: {e}")
    return eliminados, errores


# ─────────────────────────────────────────────
# 5. DETECTOR DE HUÉRFANOS (+3 años sin uso)
# ─────────────────────────────────────────────
def detectar_huerfanos(carpeta: str, años: int = 3) -> list[dict]:
    """
    Detecta archivos no modificados en los últimos X años.
    """
    limite = datetime.now() - timedelta(days=años * 365)
    huerfanos = []

    for f in Path(carpeta).rglob("*"):
        if not f.is_file():
            continue
        if "_HISTORICO" in str(f):
            continue
        stat = f.stat()
        fecha_mod = datetime.fromtimestamp(stat.st_mtime)
        if fecha_mod < limite:
            huerfanos.append({
                "path": str(f),
                "nombre": f.name,
                "fecha_mod": fecha_mod,
                "años_inactivo": round((datetime.now() - fecha_mod).days / 365, 1),
                "tamaño": stat.st_size,
                "seleccionado": True
            })

    huerfanos.sort(key=lambda x: x["fecha_mod"])
    return huerfanos
