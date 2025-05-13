# 🗳️ Sistema de Votação com Interface Gráfica (Tkinter)

Este projeto é um sistema de votação simples feito com Python e a biblioteca `tkinter`, onde é possível:

- Cadastrar candidatos
- Registrar votos
- Encerrar a votação e visualizar os resultados

---

## ✨ Melhorias e Personalizações

O sistema original era funcional, mas simples. Ele incluía apenas:

- Cadastro de candidatos
- Registro de votos
- Encerramento da votação com exibição simples dos resultados

### As principais melhorias que **eu adicionei** foram:

#### 🎨 Estilização visual
- Interface redesenhada com **cores personalizadas**:
  - Fundo claro e agradável
  - Botões em tons de verde com efeito hover
- **Fonte personalizada** em toda a interface
- **Botões grandes e amigáveis** com layout consistente
- Elementos alinhados para facilitar a leitura e uso

#### 💬 Pop-ups personalizados
- Substituição dos `messagebox` padrão por **janelas `Toplevel` estilizadas**, com:
  - Mesmas cores da interface principal
  - Títulos personalizados
  - Botões com hover e aparência amigável
  - Opção de confirmação (Sim/Não)

#### 📄 Geração de relatório em `.txt`
- Adicionei uma nova funcionalidade para **gerar um relatório com os resultados** da votação
- O usuário pode **escolher o nome do arquivo**
- Após salvar, é possível **abrir o arquivo automaticamente**
- Exemplo do conteúdo do relatório:
  ```
  ===== RELATÓRIO DE VOTAÇÃO =====

  Fulano (ABC) - 3 voto(s)
  Ciclano (XYZ) - 5 voto(s)

  Total de votos: 8
  ```
