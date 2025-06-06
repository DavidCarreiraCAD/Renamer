# -*- coding: utf-8 -*-
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from tkinter import filedialog, ttk


class RenamerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Renomeador de Ficheiros")
        self.root.geometry("1000x500")
                # Caminho do ícone (compatível com PyInstaller)
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        icon_path = os.path.join(base_path, "COBA_LOGO.ico")
        self.root.iconbitmap(icon_path)

        self.arquivos = []
        self.opcoes_vars = {
            'prefixo': tk.BooleanVar(),
            'sufixo': tk.BooleanVar(),
            'alterar': tk.BooleanVar()
        }

        # Guardar os Entry widgets
        self.entry_widgets = {}

        self._criar_interface()


    def _criar_interface(self):
        # ---------- Janela principal ----------
        self.root.title("Coba Renamer")
        self.root.geometry("800x500")
        self.root.resizable(False, False)  # Impede redimensionamento da janela

        # Estilos ttk
        style = ttk.Style()
        style.configure("BotaoGrande.TButton", padding=(10, 2))   # Alto
        style.configure("BotaoPequeno.TButton", padding=(10, 2))   # Baixo

        # Botões "Adicionar" (mais altos)
        botao_grande = {"width": 20, "style": "BotaoGrande.TButton"}

        # Botões "Preview" e "Renomear" (mais baixos)
        botao_pequeno = {"width": 10, "style": "BotaoPequeno.TButton"}

        # ---------- Frame Top com Botões ----------
        frame_top = tk.Frame(self.root)
        frame_top.pack(fill=tk.X, pady=10, padx=10)

        frame_botoes_esquerda = tk.Frame(frame_top)
        frame_botoes_esquerda.pack(side=tk.RIGHT)

        frame_botoes_direita = tk.Frame(frame_top)
        frame_botoes_direita.pack(side=tk.LEFT)

        # Botões do lado esquerdo (pequenos)
        ttk.Button(frame_botoes_esquerda, text="Preview",
                   command=lambda: self._renomear_ou_preview(aplicar=False), **botao_pequeno).pack(side=tk.LEFT, padx=5)

        ttk.Button(frame_botoes_esquerda, text="Renomear",
                   command=lambda: self._renomear_ou_preview(aplicar=True), **botao_pequeno).pack(side=tk.LEFT, padx=5)

        # Botões do lado direito (grandes)
        ttk.Button(frame_botoes_direita, text="Adicionar Ficheiros",
                   command=self.adicionar_ficheiros, **botao_grande).pack(side=tk.LEFT, padx=5)

        ttk.Button(frame_botoes_direita, text="Adicionar Pasta",
                   command=self.adicionar_pasta, **botao_grande).pack(side=tk.LEFT, padx=5)


               # ---------- Lista de ficheiros com fundo branco dividida em 2 colunas ----------
        self.frame_lista = tk.Frame(self.root, bd=1, relief=tk.SOLID)
        self.frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.canvas = tk.Canvas(self.frame_lista, bg="white")
        self.scrollbar = ttk.Scrollbar(self.frame_lista, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg="white")

        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")


        # ---------- Seleção Geral ----------
        frame_checks_gerais = tk.Frame(self.root)
        frame_checks_gerais.pack(pady=5, anchor="w")  # Alinha o frame à esquerda


        self.var_selecionar_todos = tk.BooleanVar()
        self.var_deselecionar_todos = tk.BooleanVar()

        tk.Checkbutton(frame_checks_gerais, text="Selecionar todos",
                       variable=self.var_selecionar_todos,
                       command=self._checkbox_selecionar_todos).pack(side=tk.LEFT, padx=10)

        tk.Checkbutton(frame_checks_gerais, text="Selecionar nenhum",
                       variable=self.var_deselecionar_todos,
                       command=self._checkbox_deselecionar_todos).pack(side=tk.LEFT, padx=10)

        # ---------- Opções Inferiores ----------
        frame_opcoes = tk.Frame(self.root)
        frame_opcoes.pack(pady=10, padx=10, fill=tk.X)

        frame_check = tk.Frame(frame_opcoes)
        frame_check.grid(row=0, column=0, sticky="nw", padx=(0, 20))

        tk.Checkbutton(frame_check, text="Adicionar prefixo", variable=self.opcoes_vars['prefixo'],
                       command=lambda: self._exclusivo_check('prefixo')).pack(anchor="w")
        tk.Checkbutton(frame_check, text="Adicionar sufixo", variable=self.opcoes_vars['sufixo'],
                       command=lambda: self._exclusivo_check('sufixo')).pack(anchor="w")
        tk.Checkbutton(frame_check, text="Alterar texto", variable=self.opcoes_vars['alterar'],
                       command=lambda: self._exclusivo_check('alterar')).pack(anchor="w")

        ttk.Separator(frame_opcoes, orient="vertical").grid(row=0, column=1, sticky="ns", padx=10)

        frame_campos = ttk.Frame(frame_opcoes)
        frame_campos.grid(row=0, column=2, sticky="n")

        # Linha 1 - Prefixo
        ttk.Label(frame_campos, text="Prefixo:").grid(row=0, column=0, sticky="w", padx=5, pady=(0, 5))
        self.entry_widgets['prefixo'] = ttk.Entry(frame_campos, state="disabled", width=35)
        self.entry_widgets['prefixo'].grid(row=0, column=1, columnspan=2, padx=5, pady=(0, 5))

        # Linha 2 - Sufixo
        ttk.Label(frame_campos, text="Sufixo:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_widgets['sufixo'] = ttk.Entry(frame_campos, state="disabled", width=35)
        self.entry_widgets['sufixo'].grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        # Linha 3 - Procurar por e Substituir por
        ttk.Label(frame_campos, text="Procurar por:").grid(row=2, column=0, sticky="w", padx=5, pady=(10, 5))
        self.entry_widgets['procurar'] = ttk.Entry(frame_campos, state="disabled", width=15)
        self.entry_widgets['procurar'].grid(row=2, column=1, padx=5, pady=(10, 5), sticky="w")

        ttk.Label(frame_campos, text="Substituir por:").grid(row=2, column=2, sticky="w", padx=5, pady=(10, 5))
        self.entry_widgets['substituir'] = ttk.Entry(frame_campos, state="disabled", width=15)
        self.entry_widgets['substituir'].grid(row=2, column=3, padx=5, pady=(10, 5), sticky="w")



    def _checkbox_selecionar_todos(self):
        for widget in self.scroll_frame.winfo_children():
            for child in widget.winfo_children():
                if isinstance(child, tk.Checkbutton):
                    child.var.set(True)
        self._atualizar_checkbox_geral()

    def _checkbox_deselecionar_todos(self):
        for widget in self.scroll_frame.winfo_children():
            for child in widget.winfo_children():
                if isinstance(child, tk.Checkbutton):
                    child.var.set(False)
        self._atualizar_checkbox_geral()
    def _atualizar_checkbox_geral(self):
        total = 0
        selecionados = 0

        for widget in self.scroll_frame.winfo_children():
            for child in widget.winfo_children():
                if isinstance(child, tk.Checkbutton):
                    total += 1
                    if child.var.get():
                        selecionados += 1

        if selecionados == total and total > 0:
            self.var_selecionar_todos.set(True)
            self.var_deselecionar_todos.set(False)
        elif selecionados == 0:
            self.var_selecionar_todos.set(False)
            self.var_deselecionar_todos.set(True)
        else:
            self.var_selecionar_todos.set(False)
            self.var_deselecionar_todos.set(False)


    def _exclusivo_check(self, selected):
        for key in self.opcoes_vars:
            self.opcoes_vars[key].set(False)
        self.opcoes_vars[selected].set(True)

        for entry in self.entry_widgets.values():
            entry.configure(state="disabled")

        if selected == 'prefixo':
            self.entry_widgets['prefixo'].configure(state="normal")
        elif selected == 'sufixo':
            self.entry_widgets['sufixo'].configure(state="normal")
        elif selected == 'alterar':
            self.entry_widgets['procurar'].configure(state="normal")
            self.entry_widgets['substituir'].configure(state="normal")

    def _renomear_ou_preview(self, aplicar=False):
        for widget in self.scroll_frame.winfo_children():  # widget = frame
            if isinstance(widget, tk.Frame):
                checkbutton = None
                # Encontrar o Checkbutton selecionado nesse frame
                for child in widget.winfo_children():
                    if isinstance(child, tk.Checkbutton) and child.var.get():
                        checkbutton = child
                        break
                if checkbutton is None:
                    continue

                file_path = checkbutton.file_path
                dir_nome, nome_arquivo = os.path.split(file_path)
                nome_base, extensao = os.path.splitext(nome_arquivo)
                novo_nome = nome_base

                if self.opcoes_vars['prefixo'].get():
                    prefixo = self.entry_widgets['prefixo'].get()
                    novo_nome = prefixo + novo_nome
                elif self.opcoes_vars['sufixo'].get():
                    sufixo = self.entry_widgets['sufixo'].get()
                    novo_nome = novo_nome + sufixo
                elif self.opcoes_vars['alterar'].get():
                    procurar = self.entry_widgets['procurar'].get()
                    substituir = self.entry_widgets['substituir'].get()
                    novo_nome = novo_nome.replace(procurar, substituir)

                novo_caminho = os.path.join(dir_nome, novo_nome + extensao)

                if aplicar:
                    try:
                        os.rename(file_path, novo_caminho)
                        checkbutton.file_path = novo_caminho
                    except Exception as e:
                        messagebox.showerror("Erro", f"Erro ao renomear {file_path}:\n{e}")
                        continue

                # Atualizar labels no frame
                label_preview = widget.children.get("label_preview")
                label_nome = widget.children.get("label_nome")
                if label_preview:
                    label_preview.config(text=os.path.basename(novo_caminho) if not aplicar else "")
                if label_nome:
                    label_nome.config(text=os.path.basename(novo_caminho) if aplicar else os.path.basename(checkbutton.file_path))

        if aplicar:
            messagebox.showinfo("Concluído", "Renomeação finalizada!")

    def adicionar_ficheiros(self):
        caminhos = filedialog.askopenfilenames(title="Selecionar ficheiros")
        self._atualizar_lista(caminhos)

    def adicionar_pasta(self):
        pasta = filedialog.askdirectory(title="Selecionar pasta")
        if pasta:
            caminhos = [os.path.join(pasta, f) for f in os.listdir(pasta) if os.path.isfile(os.path.join(pasta, f))]
            self._atualizar_lista(caminhos)

    def _atualizar_lista(self, caminhos):
        # Caminhos absolutos originais (mantêm capitalização correta)
        caminhos_abs = [os.path.abspath(c) for c in caminhos]

        # Caminhos normalizados para comparação de duplicados (sem afetar nomes reais)
        caminhos_norm = [os.path.normcase(c) for c in caminhos_abs]
        arquivos_norm = set(os.path.normcase(a) for a in self.arquivos)

        # Eliminar duplicados com base na versão normalizada
        novos = [c for c, norm in zip(caminhos_abs, caminhos_norm) if norm not in arquivos_norm]
        self.arquivos.extend(novos)

        # Criar entradas na interface
        for caminho in novos:
            frame = tk.Frame(self.scroll_frame, bg="white")
            frame.pack(fill=tk.X, pady=1)

            var = tk.BooleanVar()
            chk = tk.Checkbutton(frame, variable=var, anchor="w", justify="left", bg="white")
            chk.var = var
            chk.file_path = caminho
            chk.pack(side=tk.LEFT, padx=(5, 5))

            label_nome = tk.Label(frame, text=os.path.basename(caminho), name="label_nome", bg="white", width=50, anchor="w")
            label_nome.pack(side=tk.LEFT, padx=(0, 10))

            label_preview = tk.Label(frame, text="", name="label_preview", bg="white", fg="gray", width=50, anchor="w")
            label_preview.pack(side=tk.LEFT)

            def toggle_check(event, var=var):
                var.set(not var.get())
                self._atualizar_checkbox_geral()

            frame.bind("<Button-1>", toggle_check)



# Inicialização
if __name__ == "__main__":
    root = tk.Tk()
    app = RenamerGUI(root)
    root.mainloop()