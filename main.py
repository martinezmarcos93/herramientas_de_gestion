"""
Tablero de Control — Herramientas de Gestión de Oficina
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

sys.path.insert(0, os.path.dirname(__file__))
from config import settings
from modulos import archivos, clientes, honorarios

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

COLOR_PURPLE = "#6C63FF"
COLOR_TEAL   = "#0F9E7B"
COLOR_AMBER  = "#BA7517"
COLOR_DANGER = "#C0392B"


# ══════════════════════════════════════════════
# VENTANA PRINCIPAL
# ══════════════════════════════════════════════
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.config_data = settings.cargar()
        self.title("Tablero de Control — Gestión de Oficina")

        # CORRECCIÓN 1: centrar ventana en pantalla
        ancho, alto = 1100, 700
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - ancho) // 2
        y = (sh - alto) // 2
        self.geometry(f"{ancho}x{alto}+{x}+{y}")
        self.minsize(900, 600)
        self._build_layout()

    def _build_layout(self):
        self.sidebar = ctk.CTkFrame(self, width=210, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        self.content = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content.pack(side="left", fill="both", expand=True)
        self._build_sidebar()
        self._mostrar_inicio()

    def _build_sidebar(self):
        # CORRECCIÓN 2: texto genérico, sin "Estudio Contable"
        ctk.CTkLabel(
            self.sidebar, text="⚙️ Gestión\nde Oficina",
            font=ctk.CTkFont(size=16, weight="bold"), justify="center"
        ).pack(pady=(24, 20), padx=12)
        ctk.CTkFrame(self.sidebar, height=1, fg_color="gray70").pack(fill="x", padx=16)

        modulos_menu = [
            ("🏠  Inicio",              self._mostrar_inicio),
            ("📁  Archivos y carpetas", self._mostrar_archivos),
            ("👤  Clientes",            self._mostrar_clientes),
            ("💰  Honorarios",          self._mostrar_honorarios),
            ("⚙️   Configuración",      self._mostrar_config),
        ]
        self.btns_menu = {}
        for label, cmd in modulos_menu:
            btn = ctk.CTkButton(
                self.sidebar, text=label, anchor="w",
                fg_color="transparent", text_color=("gray10","gray90"),
                hover_color=("gray85","gray25"),
                font=ctk.CTkFont(size=13),
                command=lambda c=cmd, l=label: self._nav(c, l)
            )
            btn.pack(fill="x", padx=8, pady=2)
            self.btns_menu[label] = btn

        ctk.CTkLabel(self.sidebar, text="v1.1  |  Python",
                     font=ctk.CTkFont(size=10), text_color="gray60").pack(side="bottom", pady=12)

    def _nav(self, cmd, label):
        for b in self.btns_menu.values():
            b.configure(fg_color="transparent")
        self.btns_menu[label].configure(fg_color=("gray80","gray30"))
        cmd()

    def _limpiar_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _header(self, titulo, subtitulo=""):
        f = ctk.CTkFrame(self.content, fg_color="transparent")
        f.pack(fill="x", padx=28, pady=(20,4))
        ctk.CTkLabel(f, text=titulo,
                     font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w")
        if subtitulo:
            ctk.CTkLabel(f, text=subtitulo, font=ctk.CTkFont(size=12),
                         text_color="gray60").pack(anchor="w")
        ctk.CTkFrame(self.content, height=1, fg_color="gray80").pack(
            fill="x", padx=28, pady=(6,12))

    # ──────────────────────────────────────────
    # INICIO
    # ──────────────────────────────────────────
    def _mostrar_inicio(self):
        self._limpiar_content()
        self._header("Tablero de Control", "Herramientas de gestión de oficina")

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
            card = ctk.CTkFrame(grid, corner_radius=12, border_width=1, border_color="gray75")
            card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
            grid.columnconfigure(i, weight=1)
            ctk.CTkLabel(card, text=ico, font=ctk.CTkFont(size=28)).pack(pady=(20,4))
            ctk.CTkLabel(card, text=titulo,
                         font=ctk.CTkFont(size=14, weight="bold")).pack()
            ctk.CTkLabel(card, text=badge, font=ctk.CTkFont(size=11),
                         text_color="gray60").pack(pady=2)
            ctk.CTkLabel(card, text=desc, font=ctk.CTkFont(size=11),
                         text_color="gray55", wraplength=200, justify="center").pack(pady=4)
            ctk.CTkButton(card, text="Abrir módulo →", command=cmd, height=30,
                          font=ctk.CTkFont(size=12)).pack(pady=(8,18), padx=20, fill="x")

        # CORRECCIÓN 3: aviso si ruta no configurada, no imponer ruta por defecto
        ruta = self.config_data.get("ruta_base","")
        ruta_frame = ctk.CTkFrame(self.content, corner_radius=8)
        ruta_frame.pack(fill="x", padx=24, pady=(4,16))
        if ruta:
            ctk.CTkLabel(ruta_frame, text="📂 Carpeta de clientes: ",
                         font=ctk.CTkFont(size=12, weight="bold")
                         ).pack(side="left", padx=12, pady=8)
            ctk.CTkLabel(ruta_frame, text=ruta,
                         font=ctk.CTkFont(size=12), text_color="gray60"
                         ).pack(side="left", pady=8)
        else:
            ctk.CTkLabel(ruta_frame,
                text="⚠  No hay carpeta de clientes configurada — ir a Configuración para definirla",
                font=ctk.CTkFont(size=12), text_color=COLOR_AMBER
            ).pack(padx=12, pady=8)

    # ──────────────────────────────────────────
    # HELPERS COMUNES
    # ──────────────────────────────────────────
    def _carpeta_row(self, parent, label="Carpeta:", var=None, default_ruta=False):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(fill="x", padx=16, pady=(10,0))
        ctk.CTkLabel(f, text=label, width=130, anchor="w").pack(side="left")
        if var is None:
            # CORRECCIÓN 3: solo usar ruta base si se pide explícitamente
            valor = self.config_data.get("ruta_base","") if default_ruta else ""
            var = ctk.StringVar(value=valor)
        entry = ctk.CTkEntry(f, textvariable=var, width=350)
        entry.pack(side="left", padx=(4,4))
        ctk.CTkButton(f, text="...", width=36,
                      command=lambda: var.set(filedialog.askdirectory() or var.get())
                      ).pack(side="left")
        return var

    def _log_box(self, parent, height=100):
        box = ctk.CTkTextbox(parent, height=height,
                             font=ctk.CTkFont(family="Courier", size=11))
        box.pack(fill="x", padx=16, pady=6)
        return box

    def _log(self, box, msg):
        box.insert("end", f"{datetime.now().strftime('%H:%M:%S')}  {msg}\n")
        box.see("end")

    def _treeview(self, parent, cols_def, height=8):
        """Helper: crea Treeview + scrollbar con columnas centradas."""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="both", expand=True, padx=16, pady=4)
        cols = tuple(c[0] for c in cols_def)
        tree = ttk.Treeview(frame, columns=cols, show="headings", height=height)
        style = ttk.Style()
        style.configure("Treeview", rowheight=22)
        for col_id, text, width in cols_def:
            tree.heading(col_id, text=text, anchor="center")
            tree.column(col_id, width=width, anchor="center")
        sb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        return tree

    # ──────────────────────────────────────────
    # MÓDULO ARCHIVOS
    # ──────────────────────────────────────────
    def _mostrar_archivos(self):
        self._limpiar_content()
        self._header("📁 Archivos y carpetas", "Gestión masiva del sistema de archivos")
        tabs = ctk.CTkTabview(self.content)
        tabs.pack(fill="both", expand=True, padx=20, pady=0)
        for nombre in ["Renombrado","Lister → TXT","Duplicados","Huérfanos","Histórico","Impresión"]:
            tabs.add(nombre)
        self._tab_renombrado(tabs.tab("Renombrado"))
        self._tab_lister(tabs.tab("Lister → TXT"))
        self._tab_duplicados(tabs.tab("Duplicados"))
        self._tab_huerfanos(tabs.tab("Huérfanos"))
        self._tab_historico(tabs.tab("Histórico"))
        self._tab_impresion(tabs.tab("Impresión"))

    # ── TAB: Renombrado ──
    def _tab_renombrado(self, parent):
        carpeta_var = self._carpeta_row(parent, default_ruta=False)

        f2 = ctk.CTkFrame(parent, fg_color="transparent")
        f2.pack(fill="x", padx=16, pady=(8,0))
        ctk.CTkLabel(f2, text="Extensión:", width=130, anchor="w").pack(side="left")
        ext_var = ctk.StringVar(value=".pdf")
        ctk.CTkEntry(f2, textvariable=ext_var, width=80).pack(side="left", padx=4)

        f3 = ctk.CTkFrame(parent, fg_color="transparent")
        f3.pack(fill="x", padx=16, pady=(6,0))
        ctk.CTkLabel(f3, text="Nuevo nombre:", width=130, anchor="w").pack(side="left")
        patron_var = ctk.StringVar(value="{fecha_mod}_{nombre}{extension}")
        ctk.CTkEntry(f3, textvariable=patron_var, width=360).pack(side="left", padx=4)

        # CORRECCIÓN 9: ayuda clara de variables disponibles
        ayuda = ctk.CTkFrame(parent, fg_color="transparent")
        ayuda.pack(fill="x", padx=16, pady=(4,2))
        ctk.CTkLabel(ayuda,
            text="Variables:  {nombre} = nombre original sin extensión   "
                 "{fecha} = hoy (YYYYMMDD)   {fecha_mod} = fecha modificación (YYYYMMDD)   "
                 "{contador} = 001, 002…   {extension} = .pdf, .xlsx…",
            font=ctk.CTkFont(size=11), text_color="gray55", wraplength=700, justify="left"
        ).pack(anchor="w")
        ctk.CTkLabel(ayuda,
            text="Ejemplo:  GARCIA_{fecha_mod}_{contador}{extension}  →  GARCIA_20240315_001.pdf",
            font=ctk.CTkFont(size=11), text_color="gray55"
        ).pack(anchor="w")

        tree = self._treeview(parent, [
            ("original", "Nombre original", 280),
            ("nuevo",    "Nombre nuevo",    280),
            ("estado",   "Estado",          100),
        ], height=6)

        log = self._log_box(parent, height=80)
        self._previsualizacion_renombrado = []

        def previsualizar():
            for r in tree.get_children(): tree.delete(r)
            self._previsualizacion_renombrado = []
            carpeta = carpeta_var.get()
            if not carpeta or not os.path.isdir(carpeta):
                messagebox.showerror("Error", "Seleccioná una carpeta válida.")
                return
            try:
                prev = archivos.previsualizar_renombrado(
                    carpeta, ext_var.get(), patron_var.get())
                self._previsualizacion_renombrado = prev
                for item in prev:
                    estado = "⚠ Conflicto" if item["conflicto"] else "✓ OK"
                    tree.insert("", "end",
                                values=(item["original"], item["nuevo"], estado))
                self._log(log, f"Previsualización: {len(prev)} archivos.")
            except Exception as e:
                self._log(log, f"Error: {e}")

        def ejecutar():
            if not self._previsualizacion_renombrado:
                messagebox.showwarning("Aviso","Primero hacé la previsualización.")
                return
            if not messagebox.askyesno("Confirmar","¿Renombrar los archivos listados?"):
                return
            n, err = archivos.ejecutar_renombrado(self._previsualizacion_renombrado)
            self._log(log, f"Renombrados: {n}. Errores: {len(err)}")
            for e in err: self._log(log, f"  ✗ {e}")

        bf = ctk.CTkFrame(parent, fg_color="transparent")
        bf.pack(fill="x", padx=16, pady=(0,8))
        ctk.CTkButton(bf, text="👁 Previsualizar",
                      command=previsualizar).pack(side="left", padx=4)
        ctk.CTkButton(bf, text="✅ Ejecutar renombrado", command=ejecutar,
                      fg_color=COLOR_TEAL, hover_color="#0b7a5e").pack(side="left", padx=4)

    # ── TAB: Lister ──
    def _tab_lister(self, parent):
        carpeta_var = self._carpeta_row(parent, default_ruta=False)
        rec_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(parent, text="Incluir subcarpetas (recursivo)",
                        variable=rec_var).pack(anchor="w", padx=16, pady=6)

        # CORRECCIÓN 10: mostrar el contenido generado en pantalla
        ctk.CTkLabel(parent, text="Contenido generado:",
                     font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=16)
        preview = ctk.CTkTextbox(parent,
                                 font=ctk.CTkFont(family="Courier", size=11))
        preview.pack(fill="both", expand=True, padx=16, pady=(4,4))

        log = self._log_box(parent, height=55)

        def ejecutar():
            carpeta = carpeta_var.get()
            if not carpeta or not os.path.isdir(carpeta):
                messagebox.showerror("Error","Carpeta no válida.")
                return
            destino = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Texto","*.txt")],
                initialfile="listado_archivos.txt")
            if not destino: return
            n = archivos.listar_archivos_a_txt(carpeta, destino, rec_var.get())
            # Mostrar contenido en la interfaz
            preview.delete("1.0","end")
            with open(destino, "r", encoding="utf-8") as f:
                preview.insert("end", f.read())
            self._log(log, f"✓ {n} archivos → {destino}")

        ctk.CTkButton(parent, text="📄 Generar listado .txt",
                      command=ejecutar, fg_color=COLOR_TEAL
                      ).pack(anchor="w", padx=16, pady=4)

    # ── TAB: Duplicados ──
    def _tab_duplicados(self, parent):
        carpeta_var = self._carpeta_row(parent, default_ruta=False)
        rec_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(parent, text="Buscar en subcarpetas",
                        variable=rec_var).pack(anchor="w", padx=16, pady=6)

        tree = self._treeview(parent, [
            ("grupo",  "#",          45),
            ("nombre", "Nombre",     200),
            ("ruta",   "Ruta",       310),
            ("fecha",  "Modificado", 130),
        ], height=9)
        log = self._log_box(parent, height=75)
        self._grupos_dup = []

        # CORRECCIÓN 11: escaneo en hilo separado para no bloquear GUI
        def escanear_worker(carpeta, recursivo, btn):
            try:
                grupos = archivos.detectar_duplicados(carpeta, recursivo)
                self._grupos_dup = grupos
                total = sum(len(g) for g in grupos)
                self.after(0, lambda: _poblar_tabla(grupos, total))
            except Exception as e:
                self.after(0, lambda err=e: self._log(log, f"Error: {err}"))
            finally:
                self.after(0, lambda: btn.configure(state="normal", text="🔍 Escanear"))

        def _poblar_tabla(grupos, total):
            for r in tree.get_children(): tree.delete(r)
            for i, grupo in enumerate(grupos, 1):
                for item in grupo:
                    tree.insert("","end", values=(
                        i, item["nombre"], item["path"],
                        item["fecha_mod"].strftime("%d/%m/%Y %H:%M")
                    ))
            self._log(log, f"Listo: {len(grupos)} grupos, {total} archivos duplicados.")

        def escanear():
            carpeta = carpeta_var.get()
            if not carpeta or not os.path.isdir(carpeta):
                messagebox.showerror("Error","Seleccioná una carpeta válida.")
                return
            for r in tree.get_children(): tree.delete(r)
            self._grupos_dup = []
            self._log(log, "Escaneando en segundo plano… la interfaz sigue activa.")
            btn_scan.configure(state="disabled", text="⏳ Escaneando…")
            threading.Thread(
                target=escanear_worker,
                args=(carpeta, rec_var.get(), btn_scan),
                daemon=True
            ).start()

        def eliminar():
            if not self._grupos_dup:
                messagebox.showinfo("Info","Primero escaneá duplicados.")
                return
            if not messagebox.askyesno("Confirmar",
                    "Se eliminará el SEGUNDO archivo de cada grupo (se mantiene el primero). ¿Continuar?"):
                return
            n, err = archivos.eliminar_duplicados(self._grupos_dup, mantener="primero")
            self._log(log, f"Eliminados: {n}. Errores: {len(err)}")

        bf = ctk.CTkFrame(parent, fg_color="transparent")
        bf.pack(fill="x", padx=16, pady=(0,8))
        btn_scan = ctk.CTkButton(bf, text="🔍 Escanear", command=escanear)
        btn_scan.pack(side="left", padx=4)
        ctk.CTkButton(bf, text="🗑 Eliminar duplicados", command=eliminar,
                      fg_color=COLOR_DANGER, hover_color="#a93226").pack(side="left", padx=4)

    # ── TAB: Huérfanos ──
    def _tab_huerfanos(self, parent):
        carpeta_var = self._carpeta_row(parent, default_ruta=False)
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(fill="x", padx=16, pady=6)
        ctk.CTkLabel(f, text="Sin modificar hace más de (años):",
                     anchor="w").pack(side="left")
        años_var = ctk.IntVar(value=3)
        ctk.CTkEntry(f, textvariable=años_var, width=60).pack(side="left", padx=8)

        tree = self._treeview(parent, [
            ("nombre", "Nombre",            200),
            ("años",   "Años inactivo",     110),
            ("ruta",   "Ruta",              270),
            ("fecha",  "Últ. modificación", 130),
        ], height=9)
        log = self._log_box(parent, height=70)

        def escanear():
            for r in tree.get_children(): tree.delete(r)
            carpeta = carpeta_var.get()
            if not carpeta or not os.path.isdir(carpeta):
                messagebox.showerror("Error","Seleccioná una carpeta válida.")
                return
            try:
                años = años_var.get()
            except Exception:
                messagebox.showerror("Error", "Ingresá un número entero de años válido.")
                return
            try:
                res = archivos.detectar_huerfanos(carpeta, años)
                for item in res:
                    tree.insert("","end", values=(
                        item["nombre"], item["años_inactivo"],
                        item["path"], item["fecha_mod"].strftime("%d/%m/%Y")
                    ))
                self._log(log, f"Encontrados {len(res)} archivos huérfanos.")
            except Exception as e:
                self._log(log, f"Error: {e}")

        ctk.CTkButton(parent, text="🔍 Buscar huérfanos",
                      command=escanear).pack(anchor="w", padx=16, pady=4)

    # ── TAB: Histórico ──
    def _tab_historico(self, parent):
        carpeta_var = self._carpeta_row(parent, "Carpeta clientes:", default_ruta=True)
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(fill="x", padx=16, pady=6)
        ctk.CTkLabel(f, text="Meses sin modificar:", anchor="w", width=170).pack(side="left")
        meses_var = ctk.IntVar(value=self.config_data.get("meses_inactividad",12))
        ctk.CTkEntry(f, textvariable=meses_var, width=60).pack(side="left", padx=4)

        tree = self._treeview(parent, [
            ("nombre",  "Archivo",           200),
            ("cliente", "Cliente",           150),
            ("año",     "Año destino",        90),
            ("fecha",   "Últ. modificación", 130),
        ], height=8)
        log = self._log_box(parent, height=70)
        self._candidatos_hist = []

        def escanear():
            for r in tree.get_children(): tree.delete(r)
            self._candidatos_hist = []
            carpeta = carpeta_var.get()
            if not carpeta or not os.path.isdir(carpeta):
                messagebox.showerror("Error","Seleccioná una carpeta válida.")
                return
            try:
                cands = archivos.escanear_para_historico(carpeta, meses_var.get())
                self._candidatos_hist = cands
                for item in cands:
                    tree.insert("","end", values=(
                        item["nombre"], item["cliente"],
                        item["año_destino"], item["fecha_mod"].strftime("%d/%m/%Y")
                    ))
                self._log(log, f"{len(cands)} archivos candidatos al histórico.")
            except Exception as e:
                self._log(log, f"Error: {e}")

        def mover():
            if not self._candidatos_hist:
                messagebox.showinfo("Info","Primero escaneá.")
                return
            dest_info = Path(carpeta_var.get()) / "_HISTORICO" / "{año}" / "{cliente}"
            if not messagebox.askyesno("Confirmar",
                    f"Se moverán los archivos a:\n{dest_info}\n\n¿Continuar?"):
                return
            n, err = archivos.mover_a_historico(self._candidatos_hist, carpeta_var.get())
            self._log(log, f"Movidos: {n}. Errores: {len(err)}")
            for e in err: self._log(log, f"  ✗ {e}")

        bf = ctk.CTkFrame(parent, fg_color="transparent")
        bf.pack(fill="x", padx=16, pady=(0,8))
        ctk.CTkButton(bf, text="🔍 Escanear candidatos",
                      command=escanear).pack(side="left", padx=4)
        ctk.CTkButton(bf, text="📦 Mover al histórico", command=mover,
                      fg_color=COLOR_AMBER, hover_color="#9a5e0e").pack(side="left", padx=4)

    # ── TAB: Impresión ──
    def _tab_impresion(self, parent):
        carpeta_var = self._carpeta_row(parent, default_ruta=False)
        f2 = ctk.CTkFrame(parent, fg_color="transparent")
        f2.pack(fill="x", padx=16, pady=6)
        ctk.CTkLabel(f2, text="Ordenar por:", anchor="w", width=100).pack(side="left")
        orden_var = ctk.StringVar(value="nombre")
        ctk.CTkOptionMenu(f2, values=["nombre","fecha_creacion","fecha_modificacion"],
                          variable=orden_var, width=200).pack(side="left", padx=4)

        tree = self._treeview(parent, [
            ("orden",  "#",       50),
            ("nombre", "Archivo", 370),
            ("ext",    "Tipo",    90),
        ], height=9)
        log = self._log_box(parent, height=70)
        self._archivos_imp = []

        def listar():
            for r in tree.get_children(): tree.delete(r)
            self._archivos_imp = []
            carpeta = carpeta_var.get()
            if not carpeta or not os.path.isdir(carpeta):
                messagebox.showerror("Error","Seleccioná una carpeta válida.")
                return
            try:
                lista = archivos.listar_archivos_imprimibles(carpeta, orden_var.get())
                self._archivos_imp = lista
                for i, item in enumerate(lista, 1):
                    tree.insert("","end", values=(i, item["nombre"], item["extension"]))
                self._log(log, f"{len(lista)} archivos listos para imprimir.")
            except Exception as e:
                self._log(log, f"Error: {e}")

        def imprimir():
            if not self._archivos_imp:
                messagebox.showinfo("Info","Primero listá los archivos.")
                return
            if not messagebox.askyesno("Imprimir",
                    f"Se imprimirán {len(self._archivos_imp)} archivos. ¿Continuar?"):
                return
            n, err = archivos.imprimir_archivos(self._archivos_imp)
            self._log(log, f"Enviados a imprimir: {n}")
            for e in err: self._log(log, f"  ✗ {e}")

        bf = ctk.CTkFrame(parent, fg_color="transparent")
        bf.pack(fill="x", padx=16, pady=(0,8))
        ctk.CTkButton(bf, text="📋 Listar archivos",
                      command=listar).pack(side="left", padx=4)
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
        for nombre in ["Nuevo cliente","Nomenclatura","AFIP / ARCA"]:
            tabs.add(nombre)
        self._tab_nuevo_cliente(tabs.tab("Nuevo cliente"))
        self._tab_nomenclatura(tabs.tab("Nomenclatura"))
        self._tab_afip(tabs.tab("AFIP / ARCA"))

    def _tab_nuevo_cliente(self, parent):
        ruta_base = self.config_data.get("ruta_base","")

        ctk.CTkLabel(parent, text="Datos del cliente",
                     font=ctk.CTkFont(size=13, weight="bold")
                     ).pack(anchor="w", padx=16, pady=(12,4))

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
                     font=ctk.CTkFont(size=13, weight="bold")
                     ).pack(anchor="w", padx=16, pady=(12,4))

        # CORRECCIÓN 6: deduplicar subcarpetas (evitar "Credenciales" y "credenciales")
        sugeridas_raw = (clientes.detectar_subcarpetas_existentes(ruta_base)
                         or self.config_data.get("carpetas_cliente_default",[]))
        vistas, sugeridas = set(), []
        for s in sugeridas_raw:
            key = s.strip().lower()
            if key not in vistas:
                vistas.add(key)
                sugeridas.append(s)

        subcarpetas_vars = []
        frame_subs = ctk.CTkFrame(parent, fg_color="transparent")
        frame_subs.pack(fill="x", padx=16)
        for sub in sugeridas[:8]:
            var = ctk.BooleanVar(value=True)
            ctk.CTkCheckBox(frame_subs, text=sub, variable=var).pack(anchor="w", pady=2)
            subcarpetas_vars.append((sub, var))

        f3 = ctk.CTkFrame(parent, fg_color="transparent")
        f3.pack(fill="x", padx=16, pady=4)
        ctk.CTkLabel(f3, text="Agregar carpeta extra:", width=180, anchor="w").pack(side="left")
        extra_var = ctk.StringVar()
        ctk.CTkEntry(f3, textvariable=extra_var, width=200).pack(side="left")

        log = self._log_box(parent, height=80)

        # CORRECCIÓN 7: botón de confirmación prominente
        def crear():
            nombre = nombre_var.get().strip()
            if not nombre:
                messagebox.showerror("Error","Ingresá el nombre del cliente.")
                return
            if not ruta_base or not os.path.isdir(ruta_base):
                messagebox.showerror("Error",
                    "La carpeta base de clientes no está configurada o no existe.\n"
                    "Configurala en ⚙️ Configuración.")
                return
            subs = [s for s, v in subcarpetas_vars if v.get()]
            if extra_var.get().strip():
                subs.append(extra_var.get().strip())
            if not messagebox.askyesno("Confirmar creación",
                    f"Se creará la carpeta:\n{ruta_base}\\{nombre.upper()}\n\n"
                    f"Subcarpetas: {', '.join(subs) if subs else 'ninguna'}\n\n¿Confirmar?"):
                return
            try:
                ruta, creadas = clientes.crear_estructura_cliente(
                    ruta_base, nombre, cuit_var.get().strip(), subs)
                self._log(log, f"✓ Cliente creado: {ruta}")
                for c in creadas: self._log(log, f"   {c}")
                nombre_var.set("")
                cuit_var.set("")
            except FileExistsError as e:
                messagebox.showerror("Ya existe", str(e))
            except Exception as e:
                self._log(log, f"✗ Error: {e}")

        ctk.CTkButton(parent, text="✅ Crear estructura de cliente",
                      command=crear, fg_color=COLOR_TEAL, hover_color="#0b7a5e",
                      height=36, font=ctk.CTkFont(size=13, weight="bold")
                      ).pack(anchor="w", padx=16, pady=(8,12))

    def _tab_nomenclatura(self, parent):
        # CORRECCIONES 8 y 9: explicar claramente el propósito y la relación con Renombrado
        info_frame = ctk.CTkFrame(parent, corner_radius=8, fg_color=("gray90","gray20"))
        info_frame.pack(fill="x", padx=16, pady=(10,6))
        ctk.CTkLabel(info_frame,
            text="🔍  Este escáner detecta archivos que NO cumplen un formato de nombre que vos definís.\n"
                 "    Usalo para auditar una carpeta. Para renombrar los archivos encontrados, "
                 "copiá la carpeta y usá la pestaña Renombrado en Archivos.",
            font=ctk.CTkFont(size=12), justify="left", wraplength=680
        ).pack(padx=12, pady=8, anchor="w")

        carpeta_var = self._carpeta_row(parent, default_ruta=False)

        f2 = ctk.CTkFrame(parent, fg_color="transparent")
        f2.pack(fill="x", padx=16, pady=6)
        ctk.CTkLabel(f2, text="Patrón válido (regex):", anchor="w", width=200).pack(side="left")
        patron_var = ctk.StringVar(value=r"^\d{11}_\d{8}_.*")
        ctk.CTkEntry(f2, textvariable=patron_var, width=300).pack(side="left", padx=4)

        ctk.CTkLabel(parent,
            text=r"Ejemplos:   ^\d{11}_\d{8}_.* → empieza con CUIT (11 dígitos) _ FECHA (8 dígitos) _"
                 r"   |   ^[A-Z].* → nombre en mayúscula   |   .* → sin filtro (detecta todos)",
            font=ctk.CTkFont(size=11), text_color="gray55", wraplength=700, justify="left"
        ).pack(anchor="w", padx=16, pady=(0,4))

        tree = self._treeview(parent, [
            ("nombre",  "Archivo con nombre incorrecto", 270),
            ("carpeta", "Ubicación",                     330),
        ], height=9)
        log = self._log_box(parent, height=70)

        def escanear():
            for r in tree.get_children(): tree.delete(r)
            carpeta = carpeta_var.get()
            if not carpeta or not os.path.isdir(carpeta):
                messagebox.showerror("Error","Seleccioná una carpeta válida.")
                return
            try:
                inc = clientes.detectar_nombres_incorrectos(carpeta, patron_var.get())
                for item in inc:
                    tree.insert("","end", values=(item["nombre"], item["carpeta"]))
                self._log(log, f"{len(inc)} archivos con nomenclatura incorrecta.")
            except Exception as e:
                self._log(log, f"Error: {e}")

        ctk.CTkButton(parent, text="🔍 Escanear nomenclatura",
                      command=escanear).pack(anchor="w", padx=16, pady=4)

    def _tab_afip(self, parent):
        ctk.CTkLabel(parent, text="Descargador de Constancias AFIP / ARCA",
                     font=ctk.CTkFont(size=13, weight="bold")
                     ).pack(anchor="w", padx=16, pady=(12,4))
        ctk.CTkLabel(parent, text=clientes.obtener_instrucciones_afip(),
                     justify="left", font=ctk.CTkFont(size=12),
                     text_color="gray60", wraplength=600).pack(anchor="w", padx=16, pady=4)
        ctk.CTkLabel(parent,
            text="⚠ Esta función requiere Selenium. Se implementará en la próxima etapa.",
            font=ctk.CTkFont(size=12), text_color=COLOR_AMBER
        ).pack(anchor="w", padx=16, pady=8)
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
        cf = ctk.CTkFrame(parent, fg_color="transparent")
        cf.pack(fill="x", padx=16, pady=(12,4))
        ctk.CTkLabel(cf, text="Honorario base ($):", anchor="w", width=160).pack(side="left")
        base_var = ctk.DoubleVar(value=self.config_data.get("honorario_base", 25475.00))
        ctk.CTkEntry(cf, textvariable=base_var, width=120).pack(side="left", padx=(4,16))
        ctk.CTkLabel(cf, text="Mes base (YYYY-MM):", anchor="w", width=160).pack(side="left")
        mes_var = ctk.StringVar(value=self.config_data.get("honorario_base_mes","2025-07"))
        ctk.CTkEntry(cf, textvariable=mes_var, width=100).pack(side="left", padx=4)

        # CORRECCIÓN 4: columnas centradas, ancho compacto
        tree = self._treeview(parent, [
            ("mes",       "Mes",          160),
            ("inflacion", "Inflación %",  110),
            ("honorario", "Honorario $",  130),
            ("estado",    "Estado",       110),
            ("nota",      "Nota",         180),
        ], height=14)
        tree.tag_configure("base",       background="#D6E4F0")
        tree.tag_configure("congelado",  background="#FFF2CC")
        tree.tag_configure("sin_indice", background="#FCE4D6")
        tree.tag_configure("recupero",   background="#E2EFDA")

        self._tabla_hon = []

        def calcular():
            for r in tree.get_children(): tree.delete(r)
            try:
                tabla = honorarios.calcular_tabla(
                    honorario_base=base_var.get(),
                    mes_base=mes_var.get()
                )
                self._tabla_hon = tabla
                for item in tabla:
                    inf = f"{item['inflacion']:.2f}%" if item['inflacion'] else "—"
                    hon = f"$ {item['honorario']:,.2f}"
                    tree.insert("","end",
                        values=(item["mes_nombre"], inf, hon,
                                item["estado"].replace("_"," ").capitalize(),
                                item["nota"]),
                        tags=(item["estado"],))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        def exportar():
            if not self._tabla_hon:
                messagebox.showinfo("Info","Primero calculá la tabla.")
                return
            destino = filedialog.asksaveasfilename(
                defaultextension=".xlsx", filetypes=[("Excel","*.xlsx")],
                initialfile="honorarios.xlsx")
            if not destino: return
            try:
                honorarios.exportar_excel(self._tabla_hon, destino)
                messagebox.showinfo("Exportado", f"Guardado en:\n{destino}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        bf = ctk.CTkFrame(parent, fg_color="transparent")
        bf.pack(fill="x", padx=16, pady=(0,8))
        ctk.CTkButton(bf, text="📊 Calcular tabla", command=calcular,
                      fg_color=COLOR_TEAL, hover_color="#0b7a5e").pack(side="left", padx=4)
        ctk.CTkButton(bf, text="📥 Exportar a Excel",
                      command=exportar).pack(side="left", padx=4)

    def _tab_indices(self, parent):
        ctk.CTkLabel(parent, text="Gestión de índices de inflación INDEC",
                     font=ctk.CTkFont(size=13, weight="bold")
                     ).pack(anchor="w", padx=16, pady=(12,4))

        sync_frame = ctk.CTkFrame(parent, corner_radius=8)
        sync_frame.pack(fill="x", padx=16, pady=4)
        ctk.CTkLabel(sync_frame,
            text="Cargá los índices manualmente o intentá sincronizar con INDEC (requiere conexión).",
            font=ctk.CTkFont(size=12), text_color="gray60"
        ).pack(anchor="w", padx=12, pady=(8,2))
        sync_log = ctk.CTkLabel(sync_frame, text="", font=ctk.CTkFont(size=12))
        sync_log.pack(anchor="w", padx=12)

        def sincronizar():
            n, msg = honorarios.sincronizar_indec()
            sync_log.configure(text=msg,
                               text_color=COLOR_TEAL if n > 0 else COLOR_AMBER)
            cargar_tabla()

        ctk.CTkButton(sync_frame, text="🔄 Sincronizar con INDEC",
                      command=sincronizar).pack(anchor="w", padx=12, pady=(4,10))

        ctk.CTkLabel(parent, text="Agregar / editar índice",
                     font=ctk.CTkFont(size=13, weight="bold")
                     ).pack(anchor="w", padx=16, pady=(10,4))
        mf = ctk.CTkFrame(parent, fg_color="transparent")
        mf.pack(fill="x", padx=16, pady=2)
        ctk.CTkLabel(mf, text="Mes (YYYY-MM):", width=130, anchor="w").pack(side="left")
        mes_inp = ctk.StringVar(value=datetime.now().strftime("%Y-%m"))
        ctk.CTkEntry(mf, textvariable=mes_inp, width=100).pack(side="left", padx=4)
        ctk.CTkLabel(mf, text="Inflación (%):", width=110, anchor="w").pack(side="left")
        val_inp = ctk.StringVar()
        ctk.CTkEntry(mf, textvariable=val_inp, width=80).pack(side="left", padx=4)

        def guardar_manual():
            try:
                honorarios.set_inflacion_manual(mes_inp.get(), float(val_inp.get()))
                val_inp.set("")
                cargar_tabla()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(parent, text="💾 Guardar índice",
                      command=guardar_manual).pack(anchor="w", padx=16, pady=(4,8))

        # CORRECCIÓN 4: tabla compacta y centrada
        ctk.CTkLabel(parent, text="Índices cargados (desde 2020):",
                     font=ctk.CTkFont(size=12, weight="bold")
                     ).pack(anchor="w", padx=16)

        tabla_frame = ctk.CTkFrame(parent)
        tabla_frame.pack(fill="both", expand=True, padx=16, pady=4)
        cols = ("mes","inflacion")
        tree = ttk.Treeview(tabla_frame, columns=cols, show="headings", height=7)
        ttk.Style().configure("Treeview", rowheight=20)
        tree.heading("mes",       text="Mes",         anchor="center")
        tree.heading("inflacion", text="Inflación %", anchor="center")
        tree.column("mes",       width=160, anchor="center")
        tree.column("inflacion", width=120, anchor="center")
        sb = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        def cargar_tabla():
            for r in tree.get_children(): tree.delete(r)
            indices = honorarios.get_todos_los_indices()
            for ym in sorted(indices.keys(), reverse=True):
                tree.insert("","end", values=(ym, f"{indices[ym]:.2f}%"))

        cargar_tabla()

    # ──────────────────────────────────────────
    # CONFIGURACIÓN
    # ──────────────────────────────────────────
    def _mostrar_config(self):
        self._limpiar_content()
        self._header("⚙️ Configuración", "Ajustes generales")

        frame = ctk.CTkFrame(self.content, corner_radius=12)
        frame.pack(fill="x", padx=24, pady=8)

        # CORRECCIÓN 3: explicar qué es la carpeta de clientes
        ctk.CTkLabel(frame, text="📂  Carpeta de clientes",
                     font=ctk.CTkFont(size=13, weight="bold")
                     ).pack(anchor="w", padx=16, pady=(12,2))
        ctk.CTkLabel(frame,
            text="Es la carpeta raíz donde están las subcarpetas de cada cliente. "
                 "Se usa como punto de partida para crear nuevos clientes, "
                 "escanear históricos y detectar nomenclaturas incorrectas.",
            font=ctk.CTkFont(size=12), text_color="gray60",
            wraplength=600, justify="left"
        ).pack(anchor="w", padx=16, pady=(0,6))

        f_ruta = ctk.CTkFrame(frame, fg_color="transparent")
        f_ruta.pack(fill="x", padx=16, pady=(0,10))
        ruta_var = ctk.StringVar(value=self.config_data.get("ruta_base",""))
        ctk.CTkEntry(f_ruta, textvariable=ruta_var, width=420).pack(side="left", padx=(0,6))
        ctk.CTkButton(f_ruta, text="...", width=36,
                      command=lambda: ruta_var.set(
                          filedialog.askdirectory() or ruta_var.get())
                      ).pack(side="left")

        ctk.CTkFrame(frame, height=1, fg_color="gray75").pack(fill="x", padx=16, pady=6)

        campos = [
            ("Honorario base ($):",               "honorario_base"),
            ("Mes base (YYYY-MM):",               "honorario_base_mes"),
            ("Meses inactividad para histórico:", "meses_inactividad"),
        ]
        vars_conf = {}
        for label, key in campos:
            f = ctk.CTkFrame(frame, fg_color="transparent")
            f.pack(fill="x", padx=16, pady=5)
            ctk.CTkLabel(f, text=label, width=260, anchor="w").pack(side="left")
            var = ctk.StringVar(value=str(self.config_data.get(key,"")))
            ctk.CTkEntry(f, textvariable=var, width=200).pack(side="left", padx=4)
            vars_conf[key] = var

        ctk.CTkFrame(frame, height=1, fg_color="gray75").pack(fill="x", padx=16, pady=6)

        ctk.CTkLabel(frame, text="Subcarpetas default para cliente nuevo:",
                     font=ctk.CTkFont(size=13, weight="bold")
                     ).pack(anchor="w", padx=16, pady=(4,2))
        subs_var = ctk.StringVar(
            value=", ".join(self.config_data.get("carpetas_cliente_default",[])))
        ctk.CTkEntry(frame, textvariable=subs_var, width=600).pack(anchor="w", padx=16, pady=2)
        ctk.CTkLabel(frame,
            text="Separadas por coma.  Ej: Documentos, Facturación, Constancias y credenciales",
            font=ctk.CTkFont(size=11), text_color="gray60"
        ).pack(anchor="w", padx=16)

        def guardar():
            self.config_data["ruta_base"] = ruta_var.get()
            for key, var in vars_conf.items():
                val = var.get()
                try:
                    if key == "honorario_base":
                        self.config_data[key] = float(val)
                    elif key == "meses_inactividad":
                        self.config_data[key] = int(val)
                    else:
                        self.config_data[key] = val
                except ValueError:
                    self.config_data[key] = val
            self.config_data["carpetas_cliente_default"] = [
                s.strip() for s in subs_var.get().split(",") if s.strip()
            ]
            settings.guardar(self.config_data)
            messagebox.showinfo("Guardado","Configuración guardada correctamente.")

        ctk.CTkButton(frame, text="💾 Guardar configuración",
                      command=guardar, fg_color=COLOR_TEAL,
                      hover_color="#0b7a5e", height=36
                      ).pack(anchor="w", padx=16, pady=16)


# ══════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.mainloop()
