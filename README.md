# Tablero de Control — Estudio Contable
## Instalación

### Requisitos
- Python 3.10 o superior
- Windows 10/11

### 1. Instalar dependencias
```
pip install customtkinter openpyxl requests
```

### 2. Ejecutar
```
python main.py
```

---

## Estructura del proyecto
```
estudio_contable/
├── main.py                  ← Ejecutar esto
├── config/
│   ├── settings.py          ← Configuración central
│   ├── config.json          ← Se genera al guardar configuración
│   └── inflacion.json       ← Índices INDEC guardados
└── modulos/
    ├── archivos.py          ← Módulo A: Archivos y carpetas
    ├── clientes.py          ← Módulo C: Clientes
    └── honorarios.py        ← Módulo H: Honorarios
```

---

## Módulos disponibles

### 📁 Archivos y carpetas
| Herramienta | Descripción |
|---|---|
| Renombrado | Renombra archivos de una extensión con patrón configurable |
| Lister → TXT | Lista todos los archivos de una carpeta en un .txt |
| Duplicados | Detecta archivos idénticos por hash MD5 |
| Huérfanos | Archivos sin modificar en X años |
| Histórico | Mueve archivos viejos a `_HISTORICO/{año}/{cliente}/` |
| Impresión | Imprime todos los archivos de una carpeta en orden |

**Variables para renombrado:**
- `{nombre}` — nombre original sin extensión
- `{fecha}` — fecha de hoy (YYYYMMDD)
- `{fecha_mod}` — fecha de última modificación (YYYYMMDD)
- `{contador}` — número correlativo (001, 002...)
- `{extension}` — extensión del archivo

### 👤 Clientes
| Herramienta | Descripción |
|---|---|
| Nuevo cliente | Crea la estructura completa de carpetas |
| Nomenclatura | Detecta archivos que no cumplen el patrón de nombres |
| AFIP / ARCA | Descarga de constancias (requiere Selenium — próxima etapa) |

### 💰 Honorarios
| Herramienta | Descripción |
|---|---|
| Tabla de honorarios | Calcula y proyecta honorarios con inflación INDEC |
| Índices INDEC | Carga manual o sincronización automática de índices |

**Lógica de cálculo:**
```
honorario[mes] = honorario[mes-1] × (1 + inflación[mes] / 100)
```
- Si no hay índice para un mes → se congela automáticamente
- El recupero acumula los índices de meses salteados

---

## Configuración
Desde el menú ⚙️ Configuración podés ajustar:
- Ruta base de clientes (`H:\Mi unidad\00-Analista Contable\00-Clientes`)
- Honorario base y mes de inicio
- Meses de inactividad para mover al histórico
- Subcarpetas default para clientes nuevos
