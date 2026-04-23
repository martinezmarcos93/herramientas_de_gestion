"""
Tablero de Control — Estudio Contable
GUI principal con CustomTkinter
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
import sys
from pathlib import Path
from datetime import datetime

# Ajustar path para imports locales
sys.path.insert(0, os.path.dirname(__file__))
from config import settings
from modulos import archivos, clientes, honorarios

# ─── Tema ───────────────────────────────────
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

COLOR_PURPLE = "#6C63FF"
COLOR_TEAL   = "#0F9E7B"
COLOR_AMBER  = "#BA7517"
COLOR_DANGER = "#C0392B"
COLOR_BG2    = "#F7F7F7"


# ══════════════════════════════════════════════
# VENTANA PRINCIPAL
# ══════════════════════════════════════════════
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.config = settings.cargar()
        self.title("Tablero de Control — Estudio Contable")
        self.geometry("1100x700")
        self.minsize(900, 600)
        self._build_layout()

    def _build_layout(self):
        # Sidebar izquierdo
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        self.sidebar.pack_propagate(False)

        # Área de contenido
        self.content = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content.pack(side="left", fill="both", expand=True, padx=0, pady=0)

        self._build_sidebar()
        self._mostrar_inicio()

    def _build_sidebar(self):
        # Logo / título
        ctk.CTkLabel(
            self.sidebar, text="📊 Estudio\nContable",
            font=ctk.CTkFont(size=16, weight="bold"),
            justify="center"
        ).pack(pady=(24, 20), padx=12)

        ctk.CTkFrame(self.sidebar, height=1, fg_color="gray70").pack(fill="x", padx=16, pady=0)

        # Menú de módulos
        self.btn_activo = None
        modulos = [
            ("🏠  Inicio",              self._mostrar_inicio),
            ("📁  Archivos y carpetas", self._mostrar_archivos),
            ("👤  Clientes",            self._mostrar_clientes),
            ("💰  Honorarios",          self._mostrar_honorarios),
            ("⚙️   Configuración",      self._mostrar_config),
        ]

        self.btns_menu = {}
        for label, cmd in modulos:
            btn = ctk.CTkButton(
                self.sidebar, text=label, anchor="w",
                fg_color="transparent", text_color=("gray10", "gray90"),
                hover_color=("gray85", "gray25"),
                font=ctk.CTkFont(size=13),
                command=lambda c=cmd, l=label: self._nav(c, l)
            )
            btn.pack(fill="x", padx=8, pady=2)
            self.btns_menu[label] = btn

        # Versión al pie
        ctk.CTkLabel(
            self.sidebar, text="v1.0  |  Python",
            font=ctk.CTkFont(size=10), text_color="gray60"
        ).pack(side="bottom", pady=12)

    def _nav(self, cmd, label):
        for l, b in self.btns_menu.items():
            b.configure(fg_color="transparent")
        self.btns_menu[label].configure(fg_color=("gray80", "gray30"))
        cmd()

    def _limpiar_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _header(self, titulo: str, subtitulo: str = ""):
        frame = ctk.CTkFrame(self.content, fg_color="transparent")
        frame.pack(fill="x", padx=28, pady=(20, 4))
        ctk.CTkLabel(frame, text=titulo,
                     font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w")
        if subtitulo:
            ctk.CTkLabel(frame, text=subtitulo,
                         font=ctk.CTkFont(size=12), text_color="gray60").pack(anchor="w")
        ctk.CTkFrame(self.content, height=1, fg_color="gray80").pack(
            fill="x", padx=28, pady=(6, 12))

    # ──────────────────────────────────────────
    # INICIO
    # ──────────────────────────────────────────
    def _mostrar_inicio(self):
        self._limpiar_content()
        self._header("Tablero de Control", "Estudio Contable — Herramientas de gestión")

        grid = ctk.CTkFrame(self.content, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=24, pady=8)

        tarjetas = [
            ("📁", "Archivos y carpetas", "6 herramientas",
             "Impresión, renombrado, duplicados, histórico", self._mostrar_archivos),
            ("👤", "Gestión de clientes", "4 herramientas",
             "Estructura, nomenclatura, AFIP", self._mostrar_clientes),
            ("💰", "Honorarios", "2 herramientas",
             "Controlador de aumentos, presupuesto", self._mostrar_honorarios),
        ]

        for i, (ico, titulo, badge, desc, cmd) in enumerate(tarjetas):
            col = i % 3
            row = i // 3
            card = ctk.CTkFrame(grid, corner_radius=12, border_width=1,
                                 border_color="gray75")
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            grid.columnconfigure(col, weight=1)

            ctk.CTkLabel(card, text=ico, font=ctk.CTkFont(size=28)).pack(pady=(20, 4))
            ctk.CTkLabel(card, text=titulo,
                         font=ctk.CTkFont(size=14, weight="bold")).pack()
            ctk.CTkLabel(card, text=badge,
                         font=ctk.CTkFont(size=11), text_color="gray60").pack(pady=2)
            ctk.CTkLabel(card, text=desc, font=ctk.CTkFont(size=11),
                         text_color="gray55", wraplength=200, justify="center").pack(pady=4)
            ctk.CTkButton(card, text="Abrir módulo →", command=cmd,
                          height=30, font=ctk.CTkFont(size=12)).pack(pady=(8, 18), padx=20, fill="x")

        # Ruta base actual
        ruta_frame = ctk.CTkFrame(self.content, corner_radius=8)
        ruta_frame.pack(fill="x", padx=24, pady=(4, 16))
        ctk.CTkLabel(ruta_frame, text="📂 Ruta base: ",
                     font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=12, pady=8)
        ctk.CTkLabel(ruta_frame, text=self.config.get("ruta_base", "No configurada"),
                     font=ctk.CTkFont(size=12), text_color="gray60").pack(side="left", pady=8)

    # ──────────────────────────────────────────
    # MÓDULO ARCHIVOS
    # ──────────────────────────────────────────
    def _mostrar_archivos(self):
        self._limpiar_content()
        self._header("📁 Archivos y carpetas", "Gestión masiva del sistema de archivos")

        tabs = ctk.CTkTabview(self.content)
        tabs.pack(fill="both", expand=True, padx=20, pady=0)

        for nombre in ["Renombrado", "Lister → TXT", "Duplicados", "Huérfanos", "Histórico", "Impresión"]:
            tabs.add(nombre)

        self._tab_renombrado(tabs.tab("Renombrado"))
        self._tab_lister(tabs.tab("Lister → TXT"))
        self._tab_duplicados(tabs.tab("Duplicados"))
        self._tab_huerfanos(tabs.tab("Huérfanos"))
        self._tab_historico(tabs.tab("Histórico"))
        self._tab_impresion(tabs.tab("Impresión"))

    def _carpeta_row(self, parent, label="Carpeta:", var=None):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(fill="x", padx=16, pady=(10, 0))
        ctk.CTkLabel(f, text=label, width=120, anchor="w").pack(side="left")
        if var is None:
            var = ctk.StringVar(value=self.config.get("ruta_base", ""))
        entry = ctk.CTkEntry(f, textvariable=var, width=360)
        entry.pack(side="left", padx=(4, 4))
        ctk.CTkButton(f, text="...", width=36,
                      command=lambda: var.set(
                          filedialog.askdirectory() or var.get()
                      )).pack(side="left")
        return var

    def _log_box(self, parent):
        box = ctk.CTkTextbox(parent, height=140, font=ctk.CTkFont(family="Courier", size=11))
        box.pack(fill="x", padx=16, pady=8)
        return box

    def _log(self, box, msg):
        box.insert("end", f"{datetime.now().strftime('%H:%M:%S')}  {msg}\n")
        box.see("end")

    # ── TAB: Renombrado ──
    def _tab_renombrado(self, parent):
        carpeta_var = self._carpeta_row(parent)

        f2 = ctk.CTkFrame(parent, fg_color="transparent")
        f2.pack(fill="x", padx=16, pady=(8, 0))
        ctk.CTkLabel(f2, text="Extensión:", width=120, anchor="w").pack(side="left")
        ext_var = ctk.StringVar(value=".pdf")
        ctk.CTkEntry(f2, textvariable=ext_var, width=80).pack(side="left", padx=4)

        f3 = ctk.CTkFrame(parent, fg_color="transparent")
        f3.pack(fill="x", padx=16, pady=(8, 0))
        ctk.CTkLabel(f3, text="Patrón:", width=120, anchor="w").pack(side="left")
        patron_var = ctk.StringVar(value="{fecha}_{nombre}{extension}")
        ctk.CTkEntry(f3, textvariable=patron_var, width=360).pack(side="left", padx=4)

        ctk.CTkLabel(parent,
                     text="Variables: {nombre}  {fecha}  {fecha_mod}  {contador}  {extension}",
                     font=ctk.CTkFont(size=11), text_color="gray60").pack(anchor="w", padx=16, pady=2)

        tabla_frame = ctk.CTkFrame(parent)
        tabla_frame.pack(fill="both", expand=True, padx=16, pady=8)

        cols = ("original", "nuevo", "estado")
        tree = ttk.Treeview(tabla_frame, columns=cols, show="headings", height=8)
        tree.heading("original", text="Nombre original")
        tree.heading("nuevo",    text="Nombre nuevo")
        tree.heading("estado",   text="Estado")
        tree.column("original", width=280)
        tree.column("nuevo",    width=280)
        tree.column("estado",   width=100)
        scroll = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        log = self._log_box(parent)
        self._previsualizacion_renombrado = []

        def previsualizar():
            for row in tree.get_children():
                tree.delete(row)
            self._previsualizacion_renombrado = []
            try:
                prev = archivos.previsualizar_renombrado(
                    carpeta_var.get(), ext_var.get(), patron_var.get())
                self._previsualizacion_renombrado = prev
                for item in prev:
                    estado = "⚠ Conflicto" if item["conflicto"] else "✓ OK"
                    tree.insert("", "end", values=(item["original"], item["nuevo"], estado))
                self._log(log, f"Previsualización: {len(prev)} archivos encontrados.")
            except Exception as e:
                self._log(log, f"Error: {e}")

        def ejecutar():
            if not self._previsualizacion_renombrado:
                messagebox.showwarning("Aviso", "Primero hacé la previsualización.")
                return
            if not messagebox.askyesno("Confirmar", "¿Renombrar los archivos listados?"):
                return
            n, err = archivos.ejecutar_renombrado(self._previsualizacion_renombrado)
            self._log(log, f"Renombrados: {n}. Errores: {len(err)}")
            for e in err:
                self._log(log, f"  ✗ {e}")

        bf = ctk.CTkFrame(parent, fg_color="transparent")
        bf.pack(fill="x", padx=16, pady=(0, 8))
        ctk.CTkButton(bf, text="👁 Previsualizar", command=previsualizar).pack(side="left", padx=4)
        ctk.CTkButton(bf, text="✅ Ejecutar renombrado", command=ejecutar,
                      fg_color=COLOR_TEAL, hover_color="#0b7a5e").pack(side="left", padx=4)

    # ── TAB: Lister ──
    def _tab_lister(self, parent):
        carpeta_var = self._carpeta_row(parent)
        rec_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(parent, text="Incluir subcarpetas (recursivo)",
                        variable=rec_var).pack(anchor="w", padx=16, pady=6)
        log = self._log_box(parent)

        def ejecutar():
            carpeta = carpeta_var.get()
            if not carpeta or not os.path.isdir(carpeta):
                messagebox.showerror("Error", "Carpeta no válida.")
                return
            destino = filedialog.asksaveasfilename(
                defaultextension=".txt", filetypes=[("Texto", "*.txt")],
                initialfile="listado_archivos.txt")
            if not destino:
                return
            n = archivos.listar_archivos_a_txt(carpeta, destino, rec_var.get())
            self._log(log, f"✓ Listado generado: {n} archivos → {destino}")

        ctk.CTkButton(parent, text="📄 Generar listado .txt", command=ejecutar,
                      fg_color=COLOR_TEAL).pack(anchor="w", padx=16, pady=4)

    # ── TAB: Duplicados ──
    def _tab_duplicados(self, parent):
        carpeta_var = self._carpeta_row(parent)
        rec_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(parent, text="Buscar en subcarpetas",
                        variable=rec_var).pack(anchor="w", padx=16, pady=6)

        tabla_frame = ctk.CTkFrame(parent)
        tabla_frame.pack(fill="both", expand=True, padx=16, pady=4)
        cols = ("grupo", "nombre", "ruta", "fecha")
        tree = ttk.Treeview(tabla_frame, columns=cols, show="headings", height=8)
        tree.heading("grupo",  text="#")
        tree.heading("nombre", text="Nombre")
        tree.heading("ruta",   text="Ruta")
        tree.heading("fecha",  text="Modificado")
        tree.column("grupo",  width=40)
        tree.column("nombre", width=180)
        tree.column("ruta",   width=300)
        tree.column("fecha",  width=130)
        sb = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        log = self._log_box(parent)
        self._grupos_dup = []

        def escanear():
            for row in tree.get_children():
                tree.delete(row)
            self._log(log, "Escaneando... (puede tardar)")
            self.update()
            try:
                grupos = archivos.detectar_duplicados(carpeta_var.get(), rec_var.get())
                self._grupos_dup = grupos
                total = sum(len(g) for g in grupos)
                for i, grupo in enumerate(grupos, 1):
                    for item in grupo:
                        tree.insert("", "end", values=(
                            i, item["nombre"], item["path"],
                            item["fecha_mod"].strftime("%d/%m/%Y %H:%M")
                        ))
                self._log(log, f"Encontrados {len(grupos)} grupos, {total} archivos duplicados.")
            except Exception as e:
                self._log(log, f"Error: {e}")

        def eliminar():
            if not self._grupos_dup:
                messagebox.showinfo("Info", "Primero escaneá duplicados.")
                return
            if not messagebox.askyesno("Confirmar",
                    "Se eliminará el SEGUNDO archivo de cada grupo (se mantiene el primero). ¿Continuar?"):
                return
            n, err = archivos.eliminar_duplicados(self._grupos_dup, mantener="primero")
            self._log(log, f"Eliminados: {n}. Errores: {len(err)}")

        bf = ctk.CTkFrame(parent, fg_color="transparent")
        bf.pack(fill="x", padx=16, pady=(0, 8))
        ctk.CTkButton(bf, text="🔍 Escanear", command=escanear).pack(side="left", padx=4)
        ctk.CTkButton(bf, text="🗑 Eliminar duplicados", command=eliminar,
                      fg_color=COLOR_DANGER, hover_color="#a93226").pack(side="left", padx=4)

    # ── TAB: Huérfanos ──
    def _tab_huerfanos(self, parent):
        carpeta_var = self._carpeta_row(parent)

        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(fill="x", padx=16, pady=6)
        ctk.CTkLabel(f, text="Sin modificar hace más de (años):", anchor="w").pack(side="left")
        años_var = ctk.IntVar(value=3)
        ctk.CTkEntry(f, textvariable=años_var, width=60).pack(side="left", padx=8)

        tabla_frame = ctk.CTkFrame(parent)
        tabla_frame.pack(fill="both", expand=True, padx=16, pady=4)
        cols = ("nombre", "años", "ruta", "fecha")
        tree = ttk.Treeview(tabla_frame, columns=cols, show="headings", height=8)
        tree.heading("nombre", text="Nombre")
        tree.heading("años",   text="Años inactivo")
        tree.heading("ruta",   text="Ruta")
        tree.heading("fecha",  text="Últ. modificación")
        tree.column("nombre", width=200)
        tree.column("años",   width=100)
        tree.column("ruta",   width=280)
        tree.column("fecha",  width=130)
        sb = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        log = self._log_box(parent)

        def escanear():
            for row in tree.get_children():
                tree.delete(row)
            try:
                resultados = archivos.detectar_huerfanos(carpeta_var.get(), años_var.get())
                for item in resultados:
                    tree.insert("", "end", values=(
                        item["nombre"], item["años_inactivo"],
                        item["path"],
                        item["fecha_mod"].strftime("%d/%m/%Y")
                    ))
                self._log(log, f"Encontrados {len(resultados)} archivos huérfanos.")
            except Exception as e:
                self._log(log, f"Error: {e}")

        ctk.CTkButton(parent, text="🔍 Buscar huérfanos",
                      command=escanear).pack(anchor="w", padx=16, pady=4)

    # ── TAB: Histórico ──
    def _tab_historico(self, parent):
        carpeta_var = self._carpeta_row(parent, "Carpeta clientes:")

        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(fill="x", padx=16, pady=6)
        ctk.CTkLabel(f, text="Meses sin modificar:", anchor="w", width=170).pack(side="left")
        meses_var = ctk.IntVar(value=self.config.get("meses_inactividad", 12))
        ctk.CTkEntry(f, textvariable=meses_var, width=60).pack(side="left", padx=4)

        tabla_frame = ctk.CTkFrame(parent)
        tabla_frame.pack(fill="both", expand=True, padx=16, pady=4)
        cols = ("sel", "nombre", "cliente", "año", "fecha")
        tree = ttk.Treeview(tabla_frame, columns=cols, show="headings", height=8)
        tree.heading("sel",    text="✓")
        tree.heading("nombre", text="Archivo")
        tree.heading("cliente",text="Cliente")
        tree.heading("año",    text="Año destino")
        tree.heading("fecha",  text="Últ. modificación")
        tree.column("sel",    width=30)
        tree.column("nombre", width=200)
        tree.column("cliente",width=150)
        tree.column("año",    width=90)
        tree.column("fecha",  width=130)
        sb = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        log = self._log_box(parent)
        self._candidatos_hist = []

        def escanear():
            for row in tree.get_children():
                tree.delete(row)
            self._candidatos_hist = []
            try:
                cands = archivos.escanear_para_historico(carpeta_var.get(), meses_var.get())
                self._candidatos_hist = cands
                for item in cands:
                    tree.insert("", "end", values=(
                        "☑", item["nombre"], item["cliente"],
                        item["año_destino"],
                        item["fecha_mod"].strftime("%d/%m/%Y")
                    ))
                self._log(log, f"{len(cands)} archivos candidatos a mover al histórico.")
            except Exception as e:
                self._log(log, f"Error: {e}")

        def mover():
            if not self._candidatos_hist:
                messagebox.showinfo("Info", "Primero escaneá.")
                return
            dest_info = (Path(carpeta_var.get()) / "_HISTORICO" / "{año}" / "{cliente}")
            if not messagebox.askyesno("Confirmar",
                    f"Se moverán los archivos a:\n{dest_info}\n\n¿Continuar?"):
                return
            n, err = archivos.mover_a_historico(self._candidatos_hist, carpeta_var.get())
            self._log(log, f"Movidos: {n}. Errores: {len(err)}")
            for e in err:
                self._log(log, f"  ✗ {e}")

        bf = ctk.CTkFrame(parent, fg_color="transparent")
        bf.pack(fill="x", padx=16, pady=(0, 8))
        ctk.CTkButton(bf, text="🔍 Escanear candidatos", command=escanear).pack(side="left", padx=4)
        ctk.CTkButton(bf, text="📦 Mover al histórico", command=mover,
                      fg_color=COLOR_AMBER, hover_color="#9a5e0e").pack(side="left", padx=4)

    # ── TAB: Impresión ──
    def _tab_impresion(self, parent):
        carpeta_var = self._carpeta_row(parent)

        f2 = ctk.CTkFrame(parent, fg_color="transparent")
        f2.pack(fill="x", padx=16, pady=6)
        ctk.CTkLabel(f2, text="Orden:", anchor="w", width=80).pack(side="left")
        orden_var = ctk.StringVar(value="nombre")
        ctk.CTkOptionMenu(f2, values=["nombre", "fecha_creacion", "fecha_modificacion"],
                          variable=orden_var, width=200).pack(side="left", padx=4)

        tabla_frame = ctk.CTkFrame(parent)
        tabla_frame.pack(fill="both", expand=True, padx=16, pady=4)
        cols = ("orden", "nombre", "ext")
        tree = ttk.Treeview(tabla_frame, columns=cols, show="headings", height=8)
        tree.heading("orden",  text="#")
        tree.heading("nombre", text="Archivo")
        tree.heading("ext",    text="Tipo")
        tree.column("orden",  width=40)
        tree.column("nombre", width=380)
        tree.column("ext",    width=80)
        sb = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        log = self._log_box(parent)
        self._archivos_imp = []

        def listar():
            for row in tree.get_children():
                tree.delete(row)
            self._archivos_imp = []
            try:
                lista = archivos.listar_archivos_imprimibles(carpeta_var.get(), orden_var.get())
                self._archivos_imp = lista
                for i, item in enumerate(lista, 1):
                    tree.insert("", "end", values=(i, item["nombre"], item["extension"]))
                self._log(log, f"{len(lista)} archivos listos para imprimir.")
            except Exception as e:
                self._log(log, f"Error: {e}")

        def imprimir():
            if not self._archivos_imp:
                messagebox.showinfo("Info", "Primero listá los archivos.")
                return
            if not messagebox.askyesno("Imprimir", f"Se imprimirán {len(self._archivos_imp)} archivos. ¿Continuar?"):
                return
            n, err = archivos.imprimir_archivos(self._archivos_imp)
            self._log(log, f"Enviados a imprimir: {n}")
            for e in err:
                self._log(log, f"  ✗ {e}")

        bf = ctk.CTkFrame(parent, fg_color="transparent")
        bf.pack(fill="x", padx=16, pady=(0, 8))
        ctk.CTkButton(bf, text="📋 Listar archivos", command=listar).pack(side="left", padx=4)
        ctk.CTkButton(bf, text="🖨 Imprimir en orden", command=imprimir,
                      fg_color=COLOR_PURPLE, hover_color="#5a52d4").pack(side="left", padx=4)

    # ──────────────────────────────────────────
    # MÓDULO CLIENTES
    # ──────────────────────────────────────────
    def _mostrar_clientes(self):
        self._limpiar_content()
        self._header("👤 Gestión de clientes", "Estructura, nomenclatura y constancias")

        tabs = ctk.CTkTabview(self.content)
        tabs.pack(fill="both", expand=True, padx=20, pady=0)
        for nombre in ["Nuevo cliente", "Nomenclatura", "AFIP / ARCA"]:
            tabs.add(nombre)

        self._tab_nuevo_cliente(tabs.tab("Nuevo cliente"))
        self._tab_nomenclatura(tabs.tab("Nomenclatura"))
        self._tab_afip(tabs.tab("AFIP / ARCA"))

    def _tab_nuevo_cliente(self, parent):
        ruta_base = self.config.get("ruta_base", "")

        ctk.CTkLabel(parent, text="Datos del cliente",
                     font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=16, pady=(12, 4))

        f1 = ctk.CTkFrame(parent, fg_color="transparent")
        f1.pack(fill="x", padx=16, pady=4)
        ctk.CTkLabel(f1, text="Nombre / Razón social:", width=180, anchor="w").pack(side="left")
        nombre_var = ctk.StringVar()
        ctk.CTkEntry(f1, textvariable=nombre_var, width=320).pack(side="left")

        f2 = ctk.CTkFrame(parent, fg_color="transparent")
        f2.pack(fill="x", padx=16, pady=4)
        ctk.CTkLabel(f2, text="CUIT:", width=180, anchor="w").pack(side="left")
        cuit_var = ctk.StringVar()
        ctk.CTkEntry(f2, textvariable=cuit_var, width=180).pack(side="left")

        ctk.CTkLabel(parent, text="Subcarpetas a crear",
                     font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=16, pady=(12, 4))

        # Detectar carpetas existentes como sugerencia
        sugeridas = clientes.detectar_subcarpetas_existentes(ruta_base) or \
                    self.config.get("carpetas_cliente_default", [])

        subcarpetas_vars = []
        frame_subs = ctk.CTkFrame(parent, fg_color="transparent")
        frame_subs.pack(fill="x", padx=16)

        for sub in sugeridas[:8]:
            var = ctk.BooleanVar(value=True)
            ctk.CTkCheckBox(frame_subs, text=sub, variable=var).pack(anchor="w", pady=2)
            subcarpetas_vars.append((sub, var))

        # Carpeta extra manual
        f3 = ctk.CTkFrame(parent, fg_color="transparent")
        f3.pack(fill="x", padx=16, pady=4)
        ctk.CTkLabel(f3, text="Agregar carpeta extra:", width=180, anchor="w").pack(side="left")
        extra_var = ctk.StringVar()
        ctk.CTkEntry(f3, textvariable=extra_var, width=200).pack(side="left")

        log = self._log_box(parent)

        def crear():
            nombre = nombre_var.get().strip()
            cuit = cuit_var.get().strip()
            if not nombre:
                messagebox.showerror("Error", "Ingresá el nombre del cliente.")
                return
            subs = [s for s, v in subcarpetas_vars if v.get()]
            if extra_var.get().strip():
                subs.append(extra_var.get().strip())
            try:
                ruta, creadas = clientes.crear_estructura_cliente(ruta_base, nombre, cuit, subs)
                self._log(log, f"✓ Cliente creado: {ruta}")
                for c in creadas:
                    self._log(log, f"   {c}")
            except FileExistsError as e:
                messagebox.showerror("Ya existe", str(e))
            except Exception as e:
                self._log(log, f"✗ Error: {e}")

        ctk.CTkButton(parent, text="✅ Crear estructura de cliente",
                      command=crear, fg_color=COLOR_TEAL,
                      hover_color="#0b7a5e").pack(anchor="w", padx=16, pady=8)

    def _tab_nomenclatura(self, parent):
        carpeta_var = self._carpeta_row(parent)

        f2 = ctk.CTkFrame(parent, fg_color="transparent")
        f2.pack(fill="x", padx=16, pady=6)
        ctk.CTkLabel(f2, text="Patrón válido (regex):", anchor="w", width=180).pack(side="left")
        patron_var = ctk.StringVar(value=r"^\d{11}_\d{8}_.*")
        ctk.CTkEntry(f2, textvariable=patron_var, width=300).pack(side="left", padx=4)

        ctk.CTkLabel(parent,
                     text="Ejemplo: ^\\d{11}_\\d{8}_.* valida archivos que empiezan con CUIT_FECHA_",
                     font=ctk.CTkFont(size=11), text_color="gray60").pack(anchor="w", padx=16)

        tabla_frame = ctk.CTkFrame(parent)
        tabla_frame.pack(fill="both", expand=True, padx=16, pady=6)
        cols = ("nombre", "carpeta")
        tree = ttk.Treeview(tabla_frame, columns=cols, show="headings", height=10)
        tree.heading("nombre",  text="Archivo con nombre incorrecto")
        tree.heading("carpeta", text="Ubicación")
        tree.column("nombre",  width=260)
        tree.column("carpeta", width=320)
        sb = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        log = self._log_box(parent)

        def escanear():
            for row in tree.get_children():
                tree.delete(row)
            try:
                incorrectos = clientes.detectar_nombres_incorrectos(
                    carpeta_var.get(), patron_var.get())
                for item in incorrectos:
                    tree.insert("", "end", values=(item["nombre"], item["carpeta"]))
                self._log(log, f"Encontrados {len(incorrectos)} archivos con nomenclatura incorrecta.")
            except Exception as e:
                self._log(log, f"Error: {e}")

        ctk.CTkButton(parent, text="🔍 Escanear nomenclatura",
                      command=escanear).pack(anchor="w", padx=16, pady=4)

    def _tab_afip(self, parent):
        ctk.CTkLabel(parent,
                     text="Descargador de Constancias AFIP / ARCA",
                     font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=16, pady=(12, 4))

        info = clientes.obtener_instrucciones_afip()
        ctk.CTkLabel(parent, text=info, justify="left",
                     font=ctk.CTkFont(size=12), text_color="gray60",
                     wraplength=600).pack(anchor="w", padx=16, pady=4)

        ctk.CTkLabel(parent,
                     text="⚠ Esta función requiere Selenium. Se implementará en la próxima etapa.",
                     font=ctk.CTkFont(size=12), text_color=COLOR_AMBER).pack(anchor="w", padx=16, pady=8)

        f1 = ctk.CTkFrame(parent, fg_color="transparent")
        f1.pack(fill="x", padx=16, pady=4)
        ctk.CTkLabel(f1, text="CUIT:", width=120, anchor="w").pack(side="left")
        ctk.CTkEntry(f1, width=180, placeholder_text="20-12345678-9").pack(side="left")

        f2 = ctk.CTkFrame(parent, fg_color="transparent")
        f2.pack(fill="x", padx=16, pady=4)
        ctk.CTkLabel(f2, text="Clave fiscal:", width=120, anchor="w").pack(side="left")
        ctk.CTkEntry(f2, width=180, show="*").pack(side="left")

        ctk.CTkButton(parent, text="⬇ Descargar constancias",
                      state="disabled").pack(anchor="w", padx=16, pady=8)

    # ──────────────────────────────────────────
    # MÓDULO HONORARIOS
    # ──────────────────────────────────────────
    def _mostrar_honorarios(self):
        self._limpiar_content()
        self._header("💰 Honorarios", "Controlador de aumentos con índice INDEC")

        tabs = ctk.CTkTabview(self.content)
        tabs.pack(fill="both", expand=True, padx=20, pady=0)
        tabs.add("Tabla de honorarios")
        tabs.add("Índices INDEC")

        self._tab_tabla_honorarios(tabs.tab("Tabla de honorarios"))
        self._tab_indices(tabs.tab("Índices INDEC"))

    def _tab_tabla_honorarios(self, parent):
        # Controles superiores
        cf = ctk.CTkFrame(parent, fg_color="transparent")
        cf.pack(fill="x", padx=16, pady=(12, 4))

        ctk.CTkLabel(cf, text="Honorario base ($):", anchor="w", width=160).pack(side="left")
        base_var = ctk.DoubleVar(value=self.config.get("honorario_base", 25475.00))
        ctk.CTkEntry(cf, textvariable=base_var, width=120).pack(side="left", padx=(4, 16))

        ctk.CTkLabel(cf, text="Mes base (YYYY-MM):", anchor="w", width=160).pack(side="left")
        mes_var = ctk.StringVar(value=self.config.get("honorario_base_mes", "2025-07"))
        ctk.CTkEntry(cf, textvariable=mes_var, width=100).pack(side="left", padx=4)

        # Tabla
        tabla_frame = ctk.CTkFrame(parent)
        tabla_frame.pack(fill="both", expand=True, padx=16, pady=6)

        cols = ("mes", "inflacion", "honorario", "estado", "nota")
        tree = ttk.Treeview(tabla_frame, columns=cols, show="headings", height=14)
        tree.heading("mes",       text="Mes")
        tree.heading("inflacion", text="Inflación %")
        tree.heading("honorario", text="Honorario $")
        tree.heading("estado",    text="Estado")
        tree.heading("nota",      text="Nota")
        tree.column("mes",       width=150)
        tree.column("inflacion", width=100)
        tree.column("honorario", width=120)
        tree.column("estado",    width=100)
        tree.column("nota",      width=200)
        sb = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        # Colores por estado
        tree.tag_configure("base",      background="#D6E4F0")
        tree.tag_configure("congelado", background="#FFF2CC")
        tree.tag_configure("sin_indice",background="#FCE4D6")
        tree.tag_configure("recupero",  background="#E2EFDA")

        self._tabla_hon = []

        def calcular():
            for row in tree.get_children():
                tree.delete(row)
            try:
                tabla = honorarios.calcular_tabla(
                    honorario_base=base_var.get(),
                    mes_base=mes_var.get()
                )
                self._tabla_hon = tabla
                for item in tabla:
                    inf = f"{item['inflacion']:.2f}%" if item['inflacion'] else "—"
                    hon = f"$ {item['honorario']:,.2f}"
                    tree.insert("", "end",
                                values=(item["mes_nombre"], inf, hon,
                                        item["estado"].replace("_", " ").capitalize(),
                                        item["nota"]),
                                tags=(item["estado"],))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        def exportar():
            if not self._tabla_hon:
                messagebox.showinfo("Info", "Primero calculá la tabla.")
                return
            destino = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel", "*.xlsx")],
                initialfile="honorarios.xlsx")
            if not destino:
                return
            try:
                honorarios.exportar_excel(self._tabla_hon, destino)
                messagebox.showinfo("Exportado", f"Guardado en:\n{destino}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        bf = ctk.CTkFrame(parent, fg_color="transparent")
        bf.pack(fill="x", padx=16, pady=(0, 8))
        ctk.CTkButton(bf, text="📊 Calcular tabla",
                      command=calcular, fg_color=COLOR_TEAL,
                      hover_color="#0b7a5e").pack(side="left", padx=4)
        ctk.CTkButton(bf, text="📥 Exportar a Excel",
                      command=exportar).pack(side="left", padx=4)

    def _tab_indices(self, parent):
        ctk.CTkLabel(parent, text="Gestión de índices de inflación INDEC",
                     font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=16, pady=(12, 4))

        # Sincronizar
        sync_frame = ctk.CTkFrame(parent, corner_radius=8)
        sync_frame.pack(fill="x", padx=16, pady=4)
        ctk.CTkLabel(sync_frame,
                     text="Los índices se cargan manualmente. Podés intentar sincronizar con INDEC (si hay conexión).",
                     font=ctk.CTkFont(size=12), text_color="gray60",
                     wraplength=500).pack(anchor="w", padx=12, pady=8)

        sync_log = ctk.CTkLabel(sync_frame, text="", font=ctk.CTkFont(size=12))
        sync_log.pack(anchor="w", padx=12)

        def sincronizar():
            n, msg = honorarios.sincronizar_indec()
            sync_log.configure(text=msg,
                               text_color=COLOR_TEAL if n > 0 else COLOR_AMBER)
            cargar_tabla()

        ctk.CTkButton(sync_frame, text="🔄 Sincronizar con INDEC",
                      command=sincronizar).pack(anchor="w", padx=12, pady=(4, 12))

        # Carga manual
        ctk.CTkLabel(parent, text="Carga manual de índice",
                     font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=16, pady=(12, 4))

        mf = ctk.CTkFrame(parent, fg_color="transparent")
        mf.pack(fill="x", padx=16, pady=4)
        ctk.CTkLabel(mf, text="Mes (YYYY-MM):", width=130, anchor="w").pack(side="left")
        mes_inp = ctk.StringVar(value=datetime.now().strftime("%Y-%m"))
        ctk.CTkEntry(mf, textvariable=mes_inp, width=100).pack(side="left", padx=4)
        ctk.CTkLabel(mf, text="Inflación (%):", width=110, anchor="w").pack(side="left")
        val_inp = ctk.StringVar()
        ctk.CTkEntry(mf, textvariable=val_inp, width=80).pack(side="left", padx=4)

        def guardar_manual():
            try:
                honorarios.set_inflacion_manual(mes_inp.get(), float(val_inp.get()))
                cargar_tabla()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(parent, text="💾 Guardar índice",
                      command=guardar_manual).pack(anchor="w", padx=16, pady=4)

        # Tabla de índices guardados
        ctk.CTkLabel(parent, text="Índices guardados",
                     font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=16, pady=(12, 4))

        tabla_frame = ctk.CTkFrame(parent)
        tabla_frame.pack(fill="both", expand=True, padx=16, pady=4)
        cols = ("mes", "inflacion")
        tree = ttk.Treeview(tabla_frame, columns=cols, show="headings", height=8)
        tree.heading("mes",       text="Mes")
        tree.heading("inflacion", text="Inflación %")
        tree.column("mes",       width=150)
        tree.column("inflacion", width=120)
        sb = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        def cargar_tabla():
            for row in tree.get_children():
                tree.delete(row)
            indices = honorarios.get_todos_los_indices()
            for ym in sorted(indices.keys(), reverse=True):
                tree.insert("", "end", values=(ym, f"{indices[ym]:.2f}%"))

        cargar_tabla()

    # ──────────────────────────────────────────
    # CONFIGURACIÓN
    # ──────────────────────────────────────────
    def _mostrar_config(self):
        self._limpiar_content()
        self._header("⚙️ Configuración", "Ajustes generales del sistema")

        frame = ctk.CTkFrame(self.content, corner_radius=12)
        frame.pack(fill="x", padx=24, pady=8)

        campos = [
            ("Ruta base de clientes:", "ruta_base", False),
            ("Honorario base ($):",    "honorario_base", False),
            ("Mes base (YYYY-MM):",    "honorario_base_mes", False),
            ("Meses inactividad para histórico:", "meses_inactividad", False),
        ]

        vars_conf = {}
        for label, key, _ in campos:
            f = ctk.CTkFrame(frame, fg_color="transparent")
            f.pack(fill="x", padx=16, pady=6)
            ctk.CTkLabel(f, text=label, width=260, anchor="w").pack(side="left")
            var = ctk.StringVar(value=str(self.config.get(key, "")))
            ctk.CTkEntry(f, textvariable=var, width=340).pack(side="left", padx=4)
            vars_conf[key] = var

        # Carpetas default de cliente
        ctk.CTkLabel(frame, text="Subcarpetas default para cliente nuevo:",
                     font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=16, pady=(12, 4))
        subs_var = ctk.StringVar(
            value=", ".join(self.config.get("carpetas_cliente_default", [])))
        ctk.CTkEntry(frame, textvariable=subs_var, width=600).pack(anchor="w", padx=16, pady=4)
        ctk.CTkLabel(frame, text="Separadas por coma. Ej: Documentos, Facturacion, Constancias",
                     font=ctk.CTkFont(size=11), text_color="gray60").pack(anchor="w", padx=16)

        def guardar():
            for key, var in vars_conf.items():
                val = var.get()
                try:
                    if key in ("honorario_base",):
                        self.config[key] = float(val)
                    elif key in ("meses_inactividad",):
                        self.config[key] = int(val)
                    else:
                        self.config[key] = val
                except ValueError:
                    self.config[key] = val
            self.config["carpetas_cliente_default"] = [
                s.strip() for s in subs_var.get().split(",") if s.strip()
            ]
            settings.guardar(self.config)
            messagebox.showinfo("Guardado", "Configuración guardada correctamente.")

        ctk.CTkButton(frame, text="💾 Guardar configuración",
                      command=guardar, fg_color=COLOR_TEAL,
                      hover_color="#0b7a5e").pack(anchor="w", padx=16, pady=16)


# ══════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.mainloop()
