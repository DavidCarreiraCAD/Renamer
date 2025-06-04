# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import filedialog
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

        self._criar_interface()

    def _criar_interface(self):
        # ---------- Botões ----------
        frame_top = tk.Frame(self.root)
        frame_top.pack(pady=10)

        tk.Button(frame_top, text="adicionar ficheiros", command=self.adicionar_ficheiros).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_top, text="adicionar pasta", command=self.adicionar_pasta).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_top, text="preview").pack(side=tk.LEFT, padx=5)
        tk.Button(frame_top, text="renomear").pack(side=tk.RIGHT, padx=5)

        # ---------- Lista de ficheiros ----------
        self.frame_lista = tk.Frame(self.root, bd=1, relief=tk.SOLID)
        self.frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

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

        # 🔄 Adiciona campos de texto, todos desativados inicialmente
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


    def _exclusivo_check(self, selected):
        # Desativa todos
        for key in self.opcoes_vars:
            self.opcoes_vars[key].set(False)

        # Ativa apenas a opção selecionada
        self.opcoes_vars[selected].set(True)

        # Bloqueia todos os campos de texto
        for entry in self.entry_widgets.values():
            entry.configure(state="disabled")

        # Libera apenas os campos correspondentes
        if selected == 'prefixo':
            self.entry_widgets['prefixo'].configure(state="normal")
        elif selected == 'sufixo':
            self.entry_widgets['sufixo'].configure(state="normal")
        elif selected == 'alterar':
            self.entry_widgets['procurar'].configure(state="normal")
            self.entry_widgets['substituir'].configure(state="normal")


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

        self.arquivos = []
        for caminho in caminhos:
            var = tk.BooleanVar(value=True)
            chk = tk.Checkbutton(self.scroll_frame, text=caminho, variable=var, anchor="w", justify="left")
            chk.pack(fill="x", padx=5, pady=2, anchor="w")
            self.arquivos.append((caminho, var))
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

        # 🔄 Para guardar os Entry widgets
        self.entry_widgets = {}

        self._criar_interface()



# Inicialização
if __name__ == "__main__":
    import os
    root = tk.Tk()
    app = RenamerGUI(root)
    root.mainloop()
