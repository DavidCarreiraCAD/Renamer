# -*- coding: utf-8 -*-
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

class RenamerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Renomeador de Ficheiros")
        self.root.geometry("800x500")

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
        # ---------- Botões ----------
        frame_top = tk.Frame(self.root)
        frame_top.pack(pady=10)

        tk.Button(frame_top, text="adicionar ficheiros", command=self.adicionar_ficheiros).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_top, text="adicionar pasta", command=self.adicionar_pasta).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_top, text="preview", command=lambda: self._renomear_ou_preview(aplicar=False)).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_top, text="renomear", command=lambda: self._renomear_ou_preview(aplicar=True)).pack(side=tk.RIGHT, padx=5)

        # ---------- Lista de ficheiros ----------
        self.frame_lista = tk.Frame(self.root, bd=1, relief=tk.SOLID)
        self.frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Frame das checkboxes "Selecionar todos" e "Deselecionar todos"
        frame_checks_gerais = tk.Frame(self.root)
        frame_checks_gerais.pack(pady=5)

        self.var_selecionar_todos = tk.BooleanVar()
        self.var_deselecionar_todos = tk.BooleanVar()

        tk.Checkbutton(
            frame_checks_gerais, text="Selecionar todos",
            variable=self.var_selecionar_todos,
            command=self._checkbox_selecionar_todos
        ).pack(side=tk.LEFT, padx=10)

        tk.Checkbutton(
            frame_checks_gerais, text="Deselecionar todos",
            variable=self.var_deselecionar_todos,
            command=self._checkbox_deselecionar_todos
        ).pack(side=tk.LEFT, padx=10)

        self.canvas = tk.Canvas(self.frame_lista)
        self.scrollbar = ttk.Scrollbar(self.frame_lista, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas)

        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # ---------- Seção inferior ----------
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

        frame_campos = tk.Frame(frame_opcoes)
        frame_campos.grid(row=0, column=2, sticky="n")

        tk.Label(frame_campos, text="prefixo").grid(row=0, column=0, sticky="w")
        self.entry_widgets['prefixo'] = tk.Entry(frame_campos, state="disabled")
        self.entry_widgets['prefixo'].grid(row=0, column=1, padx=5)

        tk.Label(frame_campos, text="sufixo").grid(row=1, column=0, sticky="w")
        self.entry_widgets['sufixo'] = tk.Entry(frame_campos, state="disabled")
        self.entry_widgets['sufixo'].grid(row=1, column=1, padx=5)

        tk.Label(frame_campos, text="Procurar por").grid(row=2, column=0, sticky="w")
        self.entry_widgets['procurar'] = tk.Entry(frame_campos, state="disabled")
        self.entry_widgets['procurar'].grid(row=2, column=1, padx=5)

        tk.Label(frame_campos, text="Substituir por").grid(row=2, column=2, sticky="w")
        self.entry_widgets['substituir'] = tk.Entry(frame_campos, state="disabled")
        self.entry_widgets['substituir'].grid(row=2, column=3, padx=5)

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
        for widget in self.scroll_frame.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Checkbutton) and child.var.get():
                        file_path = child.file_path
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
                                child.file_path = novo_caminho
                            except Exception as e:
                                messagebox.showerror("Erro", f"Erro ao renomear {file_path}:\n{e}")
                                continue

                        child.master.children["label_nome"].config(
                            text=os.path.basename(novo_caminho) if aplicar else f"{os.path.basename(file_path)} → {os.path.basename(novo_caminho)}"
                        )

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
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        for caminho in caminhos:
            frame = tk.Frame(self.scroll_frame)
            frame.pack(fill=tk.X, pady=1)

            var = tk.BooleanVar()
            chk = tk.Checkbutton(frame, variable=var, anchor="w", justify="left")
            chk.var = var
            chk.file_path = caminho
            chk.pack(side=tk.LEFT, anchor="w", padx=(5, 0))


            label = tk.Label(frame, text=os.path.basename(caminho), name="label_nome")
            label.pack(side=tk.LEFT)


# Inicialização
if __name__ == "__main__":
    root = tk.Tk()
    app = RenamerGUI(root)
    root.mainloop()