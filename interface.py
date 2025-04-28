import tkinter as tk
from tkinter import messagebox, scrolledtext
import parser  # Certifique-se que o nome do arquivo é exatamente parser.py

class ConsultaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Processador de Consultas SQL")

        # Título
        tk.Label(root, text="Digite sua consulta SQL:", font=("Arial", 12)).pack(pady=5)

        # Campo de entrada da consulta
        self.input_box = scrolledtext.ScrolledText(root, width=80, height=5)
        self.input_box.pack(padx=10, pady=5)

        # Botão para processar consulta
        tk.Button(root, text="Processar Consulta", command=self.processar_consulta).pack(pady=5)

        # Área de resultado
        tk.Label(root, text="Resultado da Análise:", font=("Arial", 12)).pack(pady=5)
        self.result_box = scrolledtext.ScrolledText(root, width=80, height=15, state="disabled")
        self.result_box.pack(padx=10, pady=5)

    def percorrerOperacoes(self,raiz):
        print(raiz.condicao)
        self.result_box.insert(tk.END, f"{type(raiz).__name__}: {raiz.condicao}\n")
        if len(raiz.filhos)>0:
            for filho in raiz.filhos:
                self.percorrerOperacoes(filho)
    def processar_consulta(self):
        sql = self.input_box.get("1.0", tk.END).strip()
        try:
            resultado = parser.processarConsulta(sql)
            self.result_box.config(state="normal")
            self.result_box.delete("1.0", tk.END)
            if resultado:
                self.percorrerOperacoes(resultado)
            else:
                self.result_box.insert(tk.END, "Nenhuma operação reconhecida ou consulta inválida.")
            self.result_box.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar a consulta:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConsultaApp(root)
    root.mainloop()