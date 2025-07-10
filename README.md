# 🚀 autonotas – Notas Autoadesivas INSS

**Aplicativo desktop de notas rápidas para servidores do INSS** – simples, leve, 100 % offline.

---

## ✨ Visão Geral

Notas Autoadesivas INSS é um utilitário criado para que **servidores do INSS** organizem lembretes, tarefas e anotações pessoais de forma prática, sem depender de conexão com a internet nem de sistemas corporativos pesados.  
A aplicação foi desenvolvida em **Python + Tkinter** e empacotada para Windows com **PyInstaller** e **Inno Setup**. O armazenamento é feito em um único arquivo de texto (`notes.txt`), facilitando backup e migração.

---

## ⚙️ Principais Funcionalidades

| Funcionalidade        | Descrição                                                                 |
|-----------------------|---------------------------------------------------------------------------|
| **Lista de notas**    | Painel lateral mostra todos os títulos; clique para abrir.                |
| **Editor com rolagem**| Área de texto com formatação de parágrafo automática.                     |
| **Adicionar / Excluir**| Botões “+ Adicionar” e “– Excluir” gerenciam notas em 1 clique.           |
| **Salvar alterações** | Botão “Salvar” habilita apenas quando há mudanças.                        |
| **Temas Light & Dark**| Alternância imediata; preferência guardada em `config.json`.              |
| **Portabilidade**     | Todos os dados ficam em `notes.txt`; basta copiar a pasta.                |

---

## 📦 Instalação Rápida (Windows)

1. **Download**  
   - Ainda não há release oficial; clone ou baixe o ZIP deste repositório.

2. **Executar direto do código-fonte**  
   ```bash
   # Requer Python 3.8+
   python sticky_notes_app.py
   ```

3. **Gerar executável**  
   ```bash
   # Instale o PyInstaller
   pip install pyinstaller

   # Crie o executável (usa o arquivo .spec configurado)
   pyinstaller "Notas INSS.spec"
   ```

   O binário será colocado em `dist/Notas INSS/`.

4. **Criar instalador (.exe)**  
   Compile `setup_script.iss` com o **Inno Setup**.  
   O wizard moderno instalará o app, criará atalhos opcionais (desktop/start-up) e poderá executar o programa logo após a conclusão.

---

## 📝 Uso

1. **Abra** o aplicativo – a janela principal exibe a lista de notas à esquerda e o conteúdo à direita.  
2. **Clique em “+ Adicionar”** para criar uma nota: informe um título e confirme.  
3. **Digite** no painel de conteúdo; use **“Salvar alterações”** para gravar.  
4. **Mude o tema** clicando no ícone ☀️/🌙 no canto superior esquerdo.  
5. **Feche** normalmente – todas as notas e configurações são salvas automaticamente.

> **Importante 🔐**: As notas são salvas em texto simples sem criptografia. Guarde a pasta do aplicativo em um local seguro se as informações forem sensíveis.

---

## 🛠️ Estrutura do Projeto

```
autonotas/
├─ build/                  # Artefatos temporários do PyInstaller
├─ dist/                   # Executável final “Notas INSS.exe”
├─ icon.png                # Ícone da aplicação
├─ notes.txt               # Banco de dados de notas (plaintext)
├─ config.json             # Opções do usuário (tema)
├─ sticky_notes_app.py     # Código-fonte principal
├─ Notas INSS.spec         # Script PyInstaller
└─ setup_script.iss        # Script do instalador Inno Setup
```

---


## 📄 Licença

Ainda não definida. Sugere-se MIT ou Apache-2.0; abra uma *issue* para discutir.

---

**Desenvolvido por [Vitor Hugo](https://github.com/Vitorhugofsousa) e [Silas Kenji](https://github.com/Kenjibercysec)**
