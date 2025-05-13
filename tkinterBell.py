import tkinter as tk
from tkinter import messagebox
import os

candidatos = []
votacao_ativa = False

janela = tk.Tk()
janela.title("Sistema de Votação")

# Estilo
COR_FUNDO = "#f3f3c9"
COR_TEXTO = "#3f7a36"
COR_BOTAO = "#3f7a36"
COR_HOVER = "#88be4e"
COR_ENTRADA = "#eeeeee"
COR_TEXTO_BOTAO = "white"

def on_enter(e):
    e.widget.config(bg=COR_HOVER)
def on_leave(e):
    e.widget.config(bg=COR_BOTAO)

def popup_personalizado(titulo, mensagem, tipo="info", confirmar_callback=None):
    popup = tk.Toplevel(janela)
    popup.title(titulo)
    popup.geometry("400x200")
    popup.configure(bg=COR_FUNDO, padx=20, pady=20)

    tk.Label(popup, text=mensagem, font=("Arial", 14), fg=COR_TEXTO, bg=COR_FUNDO, wraplength=360).pack(pady=20)

    if tipo == "ask":
        def confirmar():
            popup.destroy()
            if confirmar_callback:
                confirmar_callback(True)

        def cancelar():
            popup.destroy()
            if confirmar_callback:
                confirmar_callback(False)

        botao_sim = tk.Button(popup, text="Sim", bg=COR_BOTAO, fg=COR_TEXTO_BOTAO, font=("Helvetica", 12, "bold"), width=10, command=confirmar)
        botao_sim.pack(side="left", expand=True, padx=20)
        botao_sim.bind("<Enter>", on_enter)
        botao_sim.bind("<Leave>", on_leave)

        botao_nao = tk.Button(popup, text="Não", bg=COR_BOTAO, fg=COR_TEXTO_BOTAO, font=("Helvetica", 12, "bold"), width=10, command=cancelar)
        botao_nao.pack(side="right", expand=True, padx=20)
        botao_nao.bind("<Enter>", on_enter)
        botao_nao.bind("<Leave>", on_leave)
    else:
        botao_ok = tk.Button(popup, text="OK", bg=COR_BOTAO, fg=COR_TEXTO_BOTAO, font=("Helvetica", 12, "bold"), command=popup.destroy)
        botao_ok.pack(pady=10)
        botao_ok.bind("<Enter>", on_enter)
        botao_ok.bind("<Leave>", on_leave)

def mostra_menu():
    janela.geometry("500x400")
    janela.configure(padx=20, pady=20, bg=COR_FUNDO)

    label_menu = tk.Label(janela, text="Escolha uma opção:", font=("Arial", 17, "bold"), fg=COR_TEXTO, bg=COR_FUNDO)
    label_menu.pack(pady=30)

    botoes = [
        ("Cadastro de Candidato", cadastra_candidato),
        ("Iniciar Votação", iniciar_votacao),
        ("Encerrar Votação", encerrar_votacao),
    ]

    for texto, comando in botoes:
        botao = tk.Button(janela, text=texto, command=comando)
        botao.pack(pady=15)
        botao.config(font=("Helvetica", 12, "bold"), fg="white", bg=COR_BOTAO, width=18, height=2)
        botao.bind("<Enter>", on_enter)
        botao.bind("<Leave>", on_leave)

def cadastra_candidato():
    janela_cadastro = tk.Toplevel(janela)
    janela_cadastro.title("Cadastro de Candidato")
    janela_cadastro.geometry("550x500")
    janela_cadastro.configure(padx=20, pady=20, bg=COR_FUNDO)

    campos = [
        ("Número do Candidato:", "numero"),
        ("Nome do Candidato:", "nome"),
        ("Partido do Candidato:", "partido")
    ]

    entradas = {}

    for texto, chave in campos:
        tk.Label(janela_cadastro, text=texto, font=("Arial", 14, "bold"), fg=COR_TEXTO, bg=COR_FUNDO).pack(pady=5)
        entrada = tk.Entry(janela_cadastro, font=("Courier", 12), fg="black", bg=COR_ENTRADA, width=30)
        entrada.pack(pady=10)
        entradas[chave] = entrada

    def salvar_candidato():
        candidato = {chave: entradas[chave].get() for chave in entradas}
        candidato["votos"] = 0
        candidatos.append(candidato)
        popup_personalizado("Sucesso", "Candidato cadastrado com sucesso!")
        janela_cadastro.destroy()

    botao_salvar = tk.Button(janela_cadastro, text="Salvar", command=salvar_candidato)
    botao_salvar.pack(pady=20)
    botao_salvar.config(font=("Helvetica", 12, "bold"), fg="white", bg=COR_BOTAO, width=14, height=2)
    botao_salvar.bind("<Enter>", on_enter)
    botao_salvar.bind("<Leave>", on_leave)

    botao_fechar = tk.Button(janela_cadastro, text="Fechar", command=janela_cadastro.destroy)
    botao_fechar.pack(pady=20)
    botao_fechar.config(font=("Helvetica", 12,"bold"), fg="white", bg="#3f7a36", width=14, height=2)
    botao_fechar.bind("<Enter>", on_enter)
    botao_fechar.bind("<Leave>", on_leave)

def iniciar_votacao():
    global votacao_ativa
    votacao_ativa = True
    registrar_voto()

def registrar_voto():
    if votacao_ativa:
        janela_votacao = tk.Toplevel(janela)
        janela_votacao.title("Votação")
        janela_votacao.geometry("500x400")
        janela_votacao.configure(padx=20, pady=20, bg=COR_FUNDO)

        tk.Label(janela_votacao, text="Digite sua matrícula:", font=("Arial", 14, "bold"), fg=COR_TEXTO, bg=COR_FUNDO).pack(pady=5)
        entrada_matricula = tk.Entry(janela_votacao, font=("Courier", 12), bg=COR_ENTRADA, width=30)
        entrada_matricula.pack(pady=10)

        tk.Label(janela_votacao, text="Digite o número do candidato:", font=("Arial", 14, "bold"), fg=COR_TEXTO, bg=COR_FUNDO).pack(pady=5)
        entrada_voto = tk.Entry(janela_votacao, font=("Courier", 12), bg=COR_ENTRADA, width=30)
        entrada_voto.pack(pady=10)

        def confirmar_voto():
            matricula = entrada_matricula.get()
            voto = entrada_voto.get()

            if not matricula:
                popup_personalizado("Erro", "Matrícula não pode ser vazia.", tipo="info")
                return

            candidato = next((c for c in candidatos if c["numero"] == voto), None)

            def voto_confirmado(confirmado):
                if confirmado:
                    if candidato:
                        candidato["votos"] += 1
                    popup_personalizado("Sucesso", "Voto registrado com sucesso!")
                    janela_votacao.destroy()
                    registrar_voto()

            if candidato:
                popup_personalizado(
                    "Confirmação",
                    f"Confirmar voto para {candidato['nome']} ({candidato['partido']})?",
                    tipo="ask",
                    confirmar_callback=voto_confirmado
                )
            else:
                popup_personalizado(
                    "Confirmação",
                    "Candidato inexistente. Confirmar voto nulo?",
                    tipo="ask",
                    confirmar_callback=voto_confirmado
                )

        botao_votar = tk.Button(janela_votacao, text="Votar", command=confirmar_voto)
        botao_votar.pack(pady=20)
        botao_votar.config(font=("Helvetica", 12, "bold"), fg="white", bg=COR_BOTAO, width=14, height=2)
        botao_votar.bind("<Enter>", on_enter)
        botao_votar.bind("<Leave>", on_leave)

        botao_fechar = tk.Button(janela_votacao, text="Fechar", command=janela_votacao.destroy)
        botao_fechar.pack(pady=20)
        botao_fechar.config(font=("Helvetica", 12,"bold"), fg="white", bg="#3f7a36", width=14, height=2)
        botao_fechar.bind("<Enter>", on_enter)
        botao_fechar.bind("<Leave>", on_leave)

def salvar_relatorio_txt_personalizado():
    janela_nome = tk.Toplevel(janela)
    janela_nome.title("Salvar Relatório")
    janela_nome.geometry("450x250")
    janela_nome.configure(bg="#f3f3c9", padx=20, pady=20)

    tk.Label(janela_nome, text="Digite o nome do arquivo:", font=("Arial", 14, "bold"), bg="#f3f3c9", fg="#3f7a36").pack(pady=10)
    entrada_nome = tk.Entry(janela_nome, font=("Courier", 12), fg="black", bg="#eeeeee", width=30)
    entrada_nome.pack(pady=10)

    def salvar_arquivo():
        nome = entrada_nome.get().strip()
        if not nome:
            nome = "relatorio_votacao"
        if not nome.endswith(".txt"):
            nome += ".txt"

        with open(nome, "w", encoding="utf-8") as f:
            f.write("===== RELATÓRIO DE VOTAÇÃO =====\n\n")
            total_votos = sum(c["votos"] for c in candidatos)

            if total_votos > 0:
                for c in candidatos:
                    f.write(f"{c['nome']} ({c['partido']}) - {c['votos']} voto(s)\n")
                f.write(f"\nTotal de votos: {total_votos}\n")
            else:
                f.write("Nenhum voto registrado.\n")

        janela_nome.destroy()

        popup = tk.Toplevel(janela)
        popup.title("Relatório Salvo")
        popup.geometry("400x200")
        popup.configure(bg="#f3f3c9", padx=20, pady=20)

        msg = f"Arquivo '{nome}' salvo com sucesso!\nDeseja abrir agora?"
        tk.Label(popup, text=msg, font=("Arial", 12, "bold"), bg="#f3f3c9", fg="#3f7a36", wraplength=350, justify="center").pack(pady=20)

        def abrir_arquivo():
            popup.destroy()
            try:
                os.startfile(nome)
            except:
                messagebox.showerror("Erro", "Não foi possível abrir o arquivo.")

        botoes = tk.Frame(popup, bg="#f3f3c9")
        botoes.pack(pady=10)

        sim_btn = tk.Button(botoes, text="Sim", command=abrir_arquivo)
        sim_btn.pack(side="left", padx=10)
        sim_btn.config(font=("Helvetica", 12,"bold"), fg="white", bg="#3f7a36", width=10)
        sim_btn.bind("<Enter>", on_enter)
        sim_btn.bind("<Leave>", on_leave)

        nao_btn = tk.Button(botoes, text="Não", command=popup.destroy)
        nao_btn.pack(side="left", padx=10)
        nao_btn.config(font=("Helvetica", 12,"bold"), fg="white", bg="#3f7a36", width=10)
        nao_btn.bind("<Enter>", on_enter)
        nao_btn.bind("<Leave>", on_leave)

    botao_salvar = tk.Button(janela_nome, text="Salvar", command=salvar_arquivo)
    botao_salvar.pack(pady=20)
    botao_salvar.config(font=("Helvetica", 12,"bold"), fg="white", bg="#3f7a36", width=14, height=2)
    botao_salvar.bind("<Enter>", on_enter)
    botao_salvar.bind("<Leave>", on_leave)

def imprime_relatorio():
    janela_relatorio = tk.Toplevel(janela)
    janela_relatorio.title("Resultados")
    janela_relatorio.geometry("500x400")
    janela_relatorio.configure(padx=20, pady=20, bg="#f3f3c9")
    
    total_votos = sum(c["votos"] for c in candidatos)
    if total_votos > 0:
        for candidato in candidatos:
            tk.Label(janela_relatorio, text=f"{candidato['nome']} ({candidato['partido']}): {candidato['votos']} votos", font=("Arial", 14, "bold"), fg="#3f7a36", bg="#f3f3c9").pack(pady=5)
    else:
        tk.Label(janela_relatorio, text="Não houve votos válidos.", font=("Arial", 14, "bold"), fg="#3f7a36", bg="#f3f3c9").pack(pady=5)

    botao_salvar_txt = tk.Button(janela_relatorio, text="Salvar como .txt", command=salvar_relatorio_txt_personalizado)
    botao_salvar_txt.pack(pady=10)
    botao_salvar_txt.config(font=("Helvetica", 12,"bold"), fg="white", bg="#3f7a36", width=18, height=2)
    botao_salvar_txt.bind("<Enter>", on_enter)
    botao_salvar_txt.bind("<Leave>", on_leave)

    botao_fechar = tk.Button(janela_relatorio, text="Fechar", command=janela_relatorio.destroy)
    botao_fechar.pack(pady=10)
    botao_fechar.config(font=("Helvetica", 12,"bold"), fg="white", bg="#3f7a36", width=18, height=2)
    botao_fechar.bind("<Enter>", on_enter)
    botao_fechar.bind("<Leave>", on_leave)


def encerrar_votacao():
    global votacao_ativa
    votacao_ativa = False
    imprime_relatorio()

mostra_menu()
janela.mainloop()